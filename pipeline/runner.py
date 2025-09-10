import os
import csv
import time
from datetime import datetime, UTC
from typing import List, Dict, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.polygon_client import PolygonClient
from services.feature_builder import build_enriched_from_aggs
from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit
from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV
from services.alpaca_client import AlpacaClient
from uk_us_timezone_handler import get_uk_us_handler
from pipeline.news_priority import build_priority, build_scores, save_priority, load_priority, save_priority_bundle, load_priority_bundle
from utils.universe_selector import UniverseSelector
from pipeline.hygiene import Hygiene
from services.sp500_client import SP500Client
from utils.sp500_cache import SP500Cache
from utils.symbols_validator import filter_symbols_present_on_polygon


def run_once_min(symbols: List[str], days: int = 7, log_path: str = "pipeline_min_log.csv") -> None:
    """Minimal additive pipeline step that fetches recent daily bars and logs basic features.

    - Uses PolygonClient.get_last_n_days strictly (real data only)
    - Computes a simple feature: percent change between first and last close
    - Appends CSV rows per symbol without modifying existing pipeline behavior
    """
    client = PolygonClient()
    header = [
        "ts_utc",
        "symbol",
        "days",
        "num_results",
        "start_iso",
        "end_iso",
        "first_close",
        "last_close",
        "pct_change",
    ]

    file_exists = os.path.exists(log_path)
    with open(log_path, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(header)

        for sym in symbols:
            data = client.get_last_n_days(sym, days=days, adjusted=True)
            results = data.get("results") or []
            # Compute simple features if data is present
            if results:
                first_close = float(results[0].get("c", 0.0))
                last_close = float(results[-1].get("c", 0.0))
                pct = ((last_close - first_close) / first_close) if first_close > 0 else 0.0
                start_iso = results[0].get("t")
                end_iso = results[-1].get("t")
            else:
                first_close = 0.0
                last_close = 0.0
                pct = 0.0
                start_iso = ""
                end_iso = ""

            w.writerow([
                datetime.now(UTC).isoformat(),
                sym,
                days,
                len(results),
                start_iso,
                end_iso,
                f"{first_close:.6f}",
                f"{last_close:.6f}",
                f"{pct:.6f}",
            ])

def _chunk(items: List[str], size: int) -> List[List[str]]:
    if size <= 0:
        return [items]
    return [items[i:i + size] for i in range(0, len(items), size)]


def _fetch_with_retries(client: PolygonClient, symbols: List[str], start_date: str, end_date: str,
                         limit: int, adjusted: bool, sort: str, max_workers: int,
                         max_retries: int, backoff: float) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Tuple[str, int]]]:
    """Return (aggs_map, status_map) where status_map[sym] = (status, retries)."""
    remaining = list(symbols)
    aggs_map: Dict[str, Dict[str, Any]] = {}
    status_map: Dict[str, Tuple[str, int]] = {}

    attempt = 0
    while remaining and attempt <= max_retries:
        attempt_syms = list(remaining)
        remaining = []
        # Parallel fetch for this attempt
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(client.get_aggs, sym, 1, "day", start_date, end_date, limit, adjusted, sort): sym
                for sym in attempt_syms
            }
            for fut in as_completed(futures):
                sym = futures[fut]
                try:
                    aggs = fut.result()
                    aggs_map[sym] = aggs
                    status_map[sym] = ("success" if attempt == 0 else "retried_success", attempt)
                except Exception:
                    # queue for next attempt
                    remaining.append(sym)
                    # only set status if first time failing; retries counted by attempt index later
                    if sym not in status_map:
                        status_map[sym] = ("retry_pending", attempt)
        if remaining:
            # Backoff before next wave
            time.sleep(backoff * max(1, attempt + 1))
        attempt += 1

    # Anything still remaining marked as failed
    for sym in remaining:
        status_map[sym] = ("failed", max_retries)
        aggs_map[sym] = {"results": []}

    return aggs_map, status_map


def run_once(symbols: List[str], start_date: str, end_date: str, execute: bool = False, log_path: str = "pipeline_log.csv",
             batch_size: int = 0, max_retries: int = 2, retry_backoff: float = 0.5, prioritize_by_news: bool = False,
             strategy_profile: str = "mean_reversion", news_booster_enabled: bool = False) -> None:
    client = PolygonClient()
    tz = get_uk_us_handler()

    lin = OptimizedInstitutionalLinUCB()
    neu = OptimizedInstitutionalNeuralBandit()
    ucv = OptimizedInstitutionalUCBV()

    alpaca = None
    if execute:
        alpaca = AlpacaClient(paper=True)

    header = [
        "ts_utc", "ts_uk", "ts_us", "market_session", "symbol",
        "fetch_status", "retries",
        "lin_arm", "lin_conf",
        "neu_conf",
        "ucv_action", "ucv_conf",
        "price", "volatility", "volume_ratio",
        "sentiment", "news_conf",
        "executed"
    ]

    file_exists = os.path.exists(log_path)
    with open(log_path, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(header)

        # Optionally reprioritize symbols by overnight news sentiment (highest first)
        ordered_symbols = build_priority(symbols) if prioritize_by_news else symbols

        # Apply hygiene (halts/earnings/SSR) based on strategy_profile
        hygiene = Hygiene()
        safe_symbols = hygiene.filter_symbols(ordered_symbols, strategy_profile=strategy_profile)

        # Process in batches to respect rate limits and keep latency predictable
        for batch in _chunk(safe_symbols, batch_size) if batch_size else [safe_symbols]:
            max_workers = min(8, max(1, len(batch)))
            aggs_map, status_map = _fetch_with_retries(
                client, batch, start_date, end_date, 10, True, "asc", max_workers, max_retries, retry_backoff
            )

            for sym in batch:
                aggs = aggs_map.get(sym, {"results": []})
                enriched = build_enriched_from_aggs(aggs)

                lin_arm = lin.select_arm(enriched)
                lin_conf = lin.get_confidence_for_context(lin_arm, enriched)

                neu.add_arm("buy_signal")
                neu_conf = neu.get_confidence("buy_signal", enriched)

                polygon_like = {
                    'status': 'OK',
                    'results': {'p': getattr(enriched.market_data, 'price', 100.0), 's': int(getattr(enriched.market_data, 'volume', 1000000)), 't': 0, 'c': [1], 'o': 0, 'h': 0, 'l': 0, 'v': int(getattr(enriched.market_data, 'volume', 1000000)), 'vw': getattr(enriched.market_data, 'price', 100.0)}
                }
                ucv_action, ucv_conf = ucv.select_action(polygon_like)

                executed = False
                if execute and alpaca is not None:
                    side = 'buy' if ucv_action in ("buy", "strong_buy", "add_position", "scalp_long") else 'sell'
                    try:
                        alpaca.place_order(symbol=sym, qty=1, side=side, type_="market", time_in_force="day", paper_guard=True)
                        executed = True
                    except Exception:
                        executed = False

                ts_utc = datetime.now(UTC).isoformat()
                ts_uk = tz.get_uk_time().isoformat()
                ts_us = tz.get_us_market_time().isoformat()
                market_session = "open" if tz.is_us_market_open() else "closed"
                fetch_status, retries = status_map.get(sym, ("unknown", 0))

                w.writerow([
                    ts_utc, ts_uk, ts_us, market_session, sym,
                    fetch_status, retries,
                    lin_arm, f"{lin_conf:.4f}",
                    f"{neu_conf:.4f}",
                    ucv_action, f"{ucv_conf:.4f}",
                    f"{getattr(enriched.market_data, 'price', 0.0):.4f}",
                    f"{getattr(enriched.market_data, 'volatility', 0.0):.4f}",
                    f"{getattr(enriched.market_data, 'volume_ratio', 0.0):.4f}",
                    f"{getattr(enriched.sentiment_analysis, 'overall_sentiment', 0.0):.4f}",
                    f"{getattr(enriched.sentiment_analysis, 'confidence_level', 0.0):.4f}",
                    executed
                ])


def run_loop(symbols: List[str], lookback_days: int, interval_seconds: int, execute: bool = False, log_path: str = "pipeline_log.csv", iterations: int | None = None, market_hours_only: bool = False,
             batch_size: int = 0, max_retries: int = 2, retry_backoff: float = 0.5, prioritize_by_news: bool = False,
             preopen_build_minutes: int = 5, priority_store_path: str = "pipeline/priority_today.json",
             candidate_universe: List[str] | None = None, universe_window_days: int = 20, universe_target_size: int = 120,
             universe_store_path: str = "pipeline/universe_today.json",
             news_booster_enabled: bool = False, news_booster_threshold: float = 0.2,
             strategy_profile: str = "mean_reversion",
             sp500_auto: bool = True,
             # Dual-pass controls
             priority_top_k_open: int = 15,
             booster_warmup_minutes: int = 5,
             priority_top_k_boost: int = 15,
             revisit_cooldown_minutes: int = 15,
             w_news: float = 0.5, w_relvol: float = 0.3, w_gap: float = 0.2) -> None:
    from datetime import date, timedelta

    tz = get_uk_us_handler()
    client = PolygonClient()
    count = 0
    hygiene = Hygiene()
    used_today_priority = False
    booster_pass_done_today = False
    last_us_date = None
    last_processed_utc: Dict[str, datetime] = {}

    def _mark_processed(symbols_run: List[str]) -> None:
        nowu = datetime.now(UTC)
        for s in symbols_run:
            last_processed_utc[s] = nowu

    def _cooldown_ok(sym: str) -> bool:
        ts = last_processed_utc.get(sym)
        if not ts:
            return True
        return (datetime.now(UTC) - ts).total_seconds() >= revisit_cooldown_minutes * 60

    def _elapsed_since_open_min(now_us_local) -> float:
        mo = now_us_local.replace(hour=9, minute=30, second=0, microsecond=0)
        return (now_us_local - mo).total_seconds() / 60.0

    def _compute_booster_scores(sym_list: List[str], prev_day_close_map: Dict[str, float]) -> Dict[str, float]:
        scores: Dict[str, float] = {}
        # Compute UTC window for first 5 minutes after open today
        now_us_local = tz.get_us_market_time()
        open_us = now_us_local.replace(hour=9, minute=30, second=0, microsecond=0)
        start_utc = open_us.astimezone(UTC)
        end_utc = (open_us.replace(minute=35)).astimezone(UTC)
        for sym in sym_list:
            try:
                # Minute bars for first 5 minutes
                data = client.get_aggs(sym, 1, "minute", start_utc.isoformat().replace("+00:00", "Z"), end_utc.isoformat().replace("+00:00", "Z"), limit=10, adjusted=True, sort="asc")
                rows = data.get("results") or []
                vol5 = sum(float(r.get("v", 0.0)) for r in rows)
                open_first = float(rows[0].get("o", 0.0)) if rows else 0.0
                prev_close = prev_day_close_map.get(sym, 0.0)
                gap = abs((open_first - prev_close) / prev_close) if prev_close > 0 else 0.0
                # Simple rel-vol proxy vs previous day first-5-min volume
                # Fetch previous day's first-5-min if not present
                if vol5 > 0:
                    # get previous day window
                    from datetime import timedelta
                    prev_open_us = (open_us - timedelta(days=1))
                    ps_utc = prev_open_us.astimezone(UTC)
                    pe_utc = (prev_open_us.replace(minute=35)).astimezone(UTC)
                    pdata = client.get_aggs(sym, 1, "minute", ps_utc.isoformat().replace("+00:00", "Z"), pe_utc.isoformat().replace("+00:00", "Z"), limit=10, adjusted=True, sort="asc")
                    prows = pdata.get("results") or []
                    pvol5 = sum(float(r.get("v", 0.0)) for r in prows)
                    relvol = (vol5 / pvol5) if pvol5 > 0 else 0.0
                else:
                    relvol = 0.0
                news_score = news_scores.get(sym, 0.0)
                blended = max(0.0, w_news * abs(news_score) + w_relvol * relvol + w_gap * gap)
                scores[sym] = blended
            except Exception:
                continue
        return scores

    while True:
        now_us = tz.get_us_market_time()
        # Determine US date changes
        current_us_date = now_us.date()
        if last_us_date is None or current_us_date != last_us_date:
            used_today_priority = False
            booster_pass_done_today = False
            last_us_date = current_us_date

        # Pre-open: within X minutes before open → build and persist a daily universe and its news-priority list
        market_open_us = now_us.replace(hour=9, minute=30, second=0, microsecond=0)
        minutes_to_open = (market_open_us - now_us).total_seconds() / 60.0
        if 0 < minutes_to_open <= preopen_build_minutes:
            try:
                # Select daily universe from candidates (or from symbols if no candidate list provided)
                end_d = date.today()
                start_d = end_d - timedelta(days=universe_window_days)
                sel_input = candidate_universe if candidate_universe else symbols
                if sp500_auto and not candidate_universe:
                    # Load cached S&P 500 or fetch
                    cache = SP500Cache()
                    sp_syms = cache.load_if_fresh()
                    if not sp_syms:
                        sp_syms = SP500Client().fetch_symbols()
                        if sp_syms:
                            cache.save_today(sp_syms)
                    if sp_syms:
                        # Validate against Polygon snapshot to avoid stale/invalid tickers
                        sel_input = filter_symbols_present_on_polygon(sp_syms)
                selector = UniverseSelector()
                selected_universe = selector.select_universe(sel_input, start_d.isoformat(), end_d.isoformat(), target_size=universe_target_size)
                # Persist selected universe (optional)
                save_priority(selected_universe, universe_store_path)
                # Build news-priority strictly from the selected universe; also persist scores
                news_scores = build_scores(selected_universe)
                ranked = sorted(selected_universe, key=lambda s: news_scores.get(s, 0.0), reverse=True)
                save_priority_bundle(priority_store_path, ranked, news_scores)
                booster_pass_done_today = False
            except Exception:
                pass

        is_open = tz.is_us_market_open()
        if market_hours_only and not is_open:
            time.sleep(interval_seconds)
            count += 1
            if iterations is not None and count >= iterations:
                break
            continue

        end = date.today()
        start = end - timedelta(days=lookback_days)
        # At market open, if a priority list exists and not yet used today, run with it once
        run_symbols = symbols
        use_priority_now = False
        if is_open and not used_today_priority:
            try:
                priority_syms, news_scores = load_priority_bundle(priority_store_path)
                if priority_syms:
                    # If news booster enabled: keep only names with |score| >= threshold from the priority list
                    if news_booster_enabled:
                        filtered = [s for s in priority_syms if abs(news_scores.get(s, 0.0)) >= news_booster_threshold]
                    else:
                        filtered = priority_syms
                    # Dual-pass: run only top-K at open, honoring cooldown
                    open_batch = [s for s in (filtered if filtered else priority_syms) if _cooldown_ok(s)][:max(1, priority_top_k_open)]
                    run_symbols = open_batch
                    use_priority_now = True
            except Exception:
                pass

        run_once(run_symbols, start.isoformat(), end.isoformat(), execute=execute, log_path=log_path,
                 batch_size=batch_size, max_retries=max_retries, retry_backoff=retry_backoff,
                 prioritize_by_news=(prioritize_by_news and not use_priority_now),
                 strategy_profile=strategy_profile, news_booster_enabled=news_booster_enabled)

        if use_priority_now:
            used_today_priority = True
            _mark_processed(run_symbols)

        # After warm-up, blended booster pass over the priority list (remaining), once per day
        if is_open and not booster_pass_done_today:
            try:
                elapsed = _elapsed_since_open_min(now_us)
                if elapsed >= booster_warmup_minutes:
                    priority_syms, news_scores = load_priority_bundle(priority_store_path)
                    if priority_syms:
                        # Build prev day close map
                        from datetime import date, timedelta
                        prev_d = (date.today() - timedelta(days=1)).isoformat()
                        prev_close_map: Dict[str, float] = {}
                        for s in priority_syms:
                            dbar = client.get_aggs(s, 1, "day", prev_d, prev_d, limit=1, adjusted=True, sort="asc").get("results") or []
                            prev_close_map[s] = float(dbar[0].get("c", 0.0)) if dbar else 0.0
                        # Remaining (not on cooldown)
                        remaining = [s for s in priority_syms if _cooldown_ok(s)]
                        booster_scores = _compute_booster_scores(remaining, prev_close_map)
                        # Combine with news for blended ordering
                        def blended(s: str) -> float:
                            return max(0.0, w_news * abs(news_scores.get(s, 0.0)) + w_relvol * booster_scores.get(s, 0.0) + w_gap * 0.0)
                        ordered = sorted(remaining, key=blended, reverse=True)
                        boost_batch = ordered[:max(1, priority_top_k_boost)]
                        if boost_batch:
                            run_once(boost_batch, start.isoformat(), end.isoformat(), execute=execute, log_path=log_path,
                                     batch_size=batch_size, max_retries=max_retries, retry_backoff=retry_backoff,
                                     prioritize_by_news=False, strategy_profile=strategy_profile, news_booster_enabled=news_booster_enabled)
                            _mark_processed(boost_batch)
                    booster_pass_done_today = True
            except Exception:
                booster_pass_done_today = True
        count += 1
        if iterations is not None and count >= iterations:
            break
        time.sleep(interval_seconds)


if __name__ == "__main__":
    # Example: run once for AAPL within a short date range; execution disabled by default
    run_once(["AAPL"], "2023-01-03", "2023-01-10", execute=False)
