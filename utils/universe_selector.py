from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Tuple

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient


class UniverseSelector:
    """Select a live trading universe (80–150 names) using only real Polygon data.

    Filters:
      - Price floor (median close >= min_price)
      - ATR% floor (avg((high - low) / close) >= min_atr_pct)
      - NBBO spread (median dollar <= spread_max_dollars OR median bps <= spread_max_bps)

    Ranking:
      - By average daily dollar volume (ADV = avg(close * volume))
    """

    def __init__(
        self,
        client: PolygonClient | None = None,
        quotes: QuotesClient | None = None,
    ) -> None:
        self.client = client or PolygonClient()
        self.quotes = quotes or QuotesClient()

    def _fetch_daily_aggs(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> List[Dict[str, Any]]:
        data = self.client.get_aggs(
            symbol,
            1,
            "day",
            start_date,
            end_date,
            limit=150,
            adjusted=True,
            sort="asc",
        )
        results = data.get("results")
        return results if isinstance(results, list) else []

    def _compute_metrics(self, rows: List[Dict[str, Any]]) -> Dict[str, float]:
        if not rows:
            return {
                "adv": 0.0,
                "atr_pct": 0.0,
                "median_close": 0.0,
                "stability": 0.0,
            }
        closes: List[float] = []
        dollar_vols: List[float] = []
        atr_fracs: List[float] = []
        for r in rows:
            c = float(r.get("c", 0.0))
            h = float(r.get("h", 0.0))
            low_price = float(r.get("l", 0.0))
            v = float(r.get("v", 0.0))
            if c > 0:
                closes.append(c)
                dollar_vols.append(c * v)
                atr_fracs.append(max(0.0, (h - low_price) / c))
        if not closes:
            return {
                "adv": 0.0,
                "atr_pct": 0.0,
                "median_close": 0.0,
                "stability": 0.0,
            }
        closes_sorted = sorted(closes)
        mid = len(closes_sorted) // 2
        if len(closes_sorted) % 2 == 0:
            median_close = 0.5 * (closes_sorted[mid - 1] + closes_sorted[mid])
        else:
            median_close = closes_sorted[mid]
        adv = sum(dollar_vols) / max(1, len(dollar_vols))
        atr_pct = sum(atr_fracs) / max(1, len(atr_fracs))
        # Stability: inverse of average absolute daily return
        abs_rets: List[float] = []
        for i in range(1, len(closes)):
            prev = closes[i - 1]
            curr = closes[i]
            if prev > 0:
                abs_rets.append(abs(curr - prev) / prev)
        avg_abs_ret = sum(abs_rets) / len(abs_rets) if abs_rets else 0.0
        stability = 1.0 / (1.0 + avg_abs_ret)
        return {"adv": adv, "atr_pct": atr_pct, "median_close": median_close, "stability": stability}

    def _get_spread_medians(
        self,
        symbol: str,
        spread_days: int,
        core_hours_only: bool,
    ) -> Tuple[float, float]:
        # Retry with light backoff to handle transient failures/rate limits
        for attempt in range(3):
            try:
                med_dollar, med_bps = self.quotes.median_spread_over_days(
                    symbol, days=spread_days, core_hours_only=core_hours_only
                )
                return float(med_dollar), float(med_bps)
            except Exception:
                if attempt < 2:
                    try:
                        import time
                        time.sleep(0.15 * (attempt + 1))
                    except Exception:
                        pass
                else:
                    # Conservative defaults to encourage exclusion when data is missing
                    return 0.05, 10.0

    def _passes_spread_filter(
        self,
        symbol: str,
        spread_max_dollars: float,
        spread_max_bps: float,
        spread_days: int,
        core_hours_only: bool,
    ) -> bool:
        try:
            med_dollar, med_bps = self.quotes.median_spread_over_days(
                symbol,
                days=spread_days,
                core_hours_only=core_hours_only,
            )
            return (med_dollar <= spread_max_dollars) or (med_bps <= spread_max_bps)
        except Exception:
            # If quotes unavailable, be conservative: fail the spread filter
            return False

    def select_universe(
        self,
        candidates: List[str],
        start_date: str,
        end_date: str,
        target_size: int = 120,
        target_max_size: int = 150,
        allow_expand_above_target: bool = True,
        expand_margin: float = 0.9,
        # Filters
        min_price: float = 10.0,
        min_atr_pct: float = 0.01,
        max_atr_pct: float = 0.05,
        adv_min_dollar: float = 50_000_000.0,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 5.0,
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
        # Optional exclusion: earnings within +/- 3 days of end_date
        earnings_exclusion: Optional[Callable[[str, str, str], List[str]]] = None,
        earnings_buffer_days: int = 3,
        # Sector balancing (optional)
        sector_classifier: Optional[Callable[[str], Optional[str]]] = None,
        sector_index_weights: Optional[Dict[str, float]] = None,  # e.g., {"Technology": 0.29, ...}
        sector_cap_bonus: float = 0.10,  # +10pp above index weight
        sector_cap_floor: float = 0.05,  # at least 5%
        sector_cap_hard_ceiling: float = 0.35,  # 35% absolute cap
        # Ranking weights (composite)
        weight_adv: float = 0.4,
        weight_spread: float = 0.3,
        weight_volatility: float = 0.2,
        weight_stability: float = 0.1,
    ) -> List[str]:
        from datetime import datetime as _dt

        metrics_by_symbol: Dict[str, Dict[str, float]] = {}
        for sym in candidates:
            rows = self._fetch_daily_aggs(sym, start_date, end_date)
            metrics = self._compute_metrics(rows)
            metrics_by_symbol[sym] = metrics

        # Price + ATR band + ADV floor
        band_filtered: List[str] = []
        for s, m in metrics_by_symbol.items():
            if m["median_close"] < min_price:
                continue
            if not (min_atr_pct <= m["atr_pct"] <= max_atr_pct):
                continue
            if m["adv"] < adv_min_dollar:
                continue
            band_filtered.append(s)

        # Earnings exclusion (optional)
        if earnings_exclusion and band_filtered:
            end_dt = _dt.fromisoformat(end_date).date()
            kept: List[str] = []
            for s in band_filtered:
                try:
                    events = earnings_exclusion(s, start_date, end_date) or []
                    exclude = False
                    for ed in events:
                        try:
                            e_dt = _dt.fromisoformat(ed).date()
                        except Exception:
                            continue
                        if abs((e_dt - end_dt).days) <= max(0, earnings_buffer_days):
                            exclude = True
                            break
                    if not exclude:
                        kept.append(s)
                except Exception:
                    kept.append(s)  # if calendar fails, keep
            band_filtered = kept

        # Spread filter and capture medians for ranking
        # Shuffle to avoid alphabetical bias if rate limits hit early
        spread_filtered: List[str] = []
        med_spreads: Dict[str, Tuple[float, float]] = {}
        try:
            import random
            order = list(band_filtered)
            random.shuffle(order)
        except Exception:
            order = band_filtered
        for s in order:
            if spread_filter_enabled:
                med_dol, med_bps = self._get_spread_medians(s, spread_lookback_days, spread_core_hours_only)
                med_spreads[s] = (med_dol, med_bps)
                if (med_dol <= spread_max_dollars) or (med_bps <= spread_max_bps):
                    spread_filtered.append(s)
            else:
                med_spreads[s] = (0.0, 0.0)
                spread_filtered.append(s)

        # If too few after spread filter, relax thresholds moderately
        if len(spread_filtered) < min(80, target_size // 2):
            relaxed: List[str] = []
            for s in band_filtered:
                med_dol, med_bps = med_spreads.get(s) or self._get_spread_medians(
                    s, spread_lookback_days, spread_core_hours_only
                )
                if (med_dol <= spread_max_dollars * 1.5) or (med_bps <= spread_max_bps * 1.7):
                    relaxed.append(s)
            spread_filtered = list(dict.fromkeys(relaxed))

        # Composite ranking
        if not spread_filtered:
            return []

        # Normalize ADV for ranking
        adv_values = [metrics_by_symbol[s]["adv"] for s in spread_filtered]
        max_adv = max(adv_values) if adv_values else 1.0

        def composite_score(sym: str) -> float:
            m = metrics_by_symbol[sym]
            # ADV score (0..1)
            adv_score = min(1.0, m["adv"] / max(1.0, max_adv))
            # Spread score: prefer tighter (bps)
            med_dol, med_bps = med_spreads.get(sym, (0.0, 10.0))
            spread_score = max(0.0, 1.0 - (med_bps / 10.0))  # 0 at 10+ bps, ~1 near 0 bps
            # Volatility score: prefer mid of band (3%) within 1–5%
            target = 0.03
            half_range = max(1e-9, (max_atr_pct - min_atr_pct) / 2.0)
            vol_score = max(0.0, 1.0 - (abs(m["atr_pct"] - target) / half_range))
            vol_score = min(1.0, vol_score)
            # Stability (0..1)
            stab_score = max(0.0, min(1.0, m.get("stability", 0.0)))
            return (
                weight_adv * adv_score
                + weight_spread * spread_score
                + weight_volatility * vol_score
                + weight_stability * stab_score
            )

        ranked = sorted(spread_filtered, key=composite_score, reverse=True)

        # If no sector constraints, optionally expand and return
        if sector_classifier is None or sector_index_weights is None:
            if not allow_expand_above_target or target_max_size <= target_size or not ranked:
                base = ranked[:target_size]
            else:
                base_k = min(target_size, len(ranked))
                base_threshold = composite_score(ranked[base_k - 1]) if base_k > 0 else 0.0
                expanded: List[str] = ranked[:base_k]
                for sym in ranked[base_k:]:
                    if len(expanded) >= target_max_size:
                        break
                    if composite_score(sym) >= base_threshold * expand_margin:
                        expanded.append(sym)
                    else:
                        break  # scores only decrease
                base = expanded

            # Robustness backstop: if we still have too few picks, relax modestly and retry once
            if len(base) < target_size:
                relaxed_adv = max(0.0, adv_min_dollar * 0.6)  # e.g., 30M if default is 50M
                relaxed_max_atr = max_atr_pct * 1.2            # widen upper ATR band by 20%
                relaxed_spread_dollars = spread_max_dollars * 1.5
                relaxed_spread_bps = max(spread_max_bps * 1.7, 8.5)

                fallback_band: List[str] = []
                for s, m in metrics_by_symbol.items():
                    if m["median_close"] < min_price:
                        continue
                    if not (min_atr_pct <= m["atr_pct"] <= relaxed_max_atr):
                        continue
                    if m["adv"] < relaxed_adv:
                        continue
                    fallback_band.append(s)

                relaxed_kept: List[str] = []
                for s in fallback_band:
                    med_dol, med_bps = med_spreads.get(s) or self._get_spread_medians(
                        s, spread_lookback_days, spread_core_hours_only
                    )
                    if (med_dol <= relaxed_spread_dollars) or (med_bps <= relaxed_spread_bps):
                        relaxed_kept.append(s)

                if relaxed_kept:
                    relaxed_ranked = sorted(relaxed_kept, key=composite_score, reverse=True)
                    base = relaxed_ranked[:min(target_max_size if allow_expand_above_target else target_size, target_size)]

            return base

        # Sector-aware selection with index-aware caps
        # Compute per-sector cap fractions
        def sector_cap_fraction(sector: str) -> float:
            w = float(sector_index_weights.get(sector, 0.0))
            cap = min(sector_cap_hard_ceiling, w + sector_cap_bonus)
            return max(sector_cap_floor, cap)

        # Allowed counts at target and max sizes
        sector_caps_target: Dict[str, int] = {}
        sector_caps_max: Dict[str, int] = {}
        for sec, w in sector_index_weights.items():
            frac = sector_cap_fraction(sec)
            sector_caps_target[sec] = max(1, int(frac * target_size))
            sector_caps_max[sec] = max(1, int(frac * target_max_size))

        # Fill to target_size enforcing sector caps
        picks: List[str] = []
        counts: Dict[str, int] = {}
        for sym in ranked:
            if len(picks) >= target_size:
                break
            sec = sector_classifier(sym) or "Unknown"
            allowed = sector_caps_target.get(sec, max(1, int(sector_cap_floor * target_size)))
            if counts.get(sec, 0) < allowed:
                picks.append(sym)
                counts[sec] = counts.get(sec, 0) + 1

        # Optional expansion to target_max_size for strong contenders
        if allow_expand_above_target and target_max_size > target_size and len(picks) < target_max_size:
            if picks:
                base_threshold = composite_score(picks[-1])
            else:
                base_threshold = composite_score(ranked[min(target_size, len(ranked)) - 1]) if ranked else 0.0
            for sym in ranked:
                if len(picks) >= target_max_size:
                    break
                if sym in picks:
                    continue
                if composite_score(sym) < base_threshold * expand_margin:
                    break
                sec = sector_classifier(sym) or "Unknown"
                allowed_max = sector_caps_max.get(sec, max(1, int(sector_cap_floor * target_max_size)))
                if counts.get(sec, 0) < allowed_max:
                    picks.append(sym)
                    counts[sec] = counts.get(sec, 0) + 1

        return picks
