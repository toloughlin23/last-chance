from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

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

    # -------------------------------
    # Dynamic 120-symbol universe API
    # -------------------------------
    def _get_sp500_like_candidates(self) -> List[str]:
        """Fetch a broad large-cap candidate set using Polygon if available, else a conservative fallback.

        Returns a deduplicated list of liquid large-cap symbols.
        """
        candidates: List[str] = []
        try:
            if hasattr(self.client, "get_tickers"):
                data = self.client.get_tickers(market="stocks", active=True, limit=1000)
                results = data.get("results") if isinstance(data, dict) else None
                if results:
                    for t in results:
                        sym = t.get("ticker")
                        mcap = t.get("market_cap", 0)
                        if isinstance(sym, str) and sym and isinstance(mcap, (int, float)) and mcap > 8_000_000_000:
                            candidates.append(sym)
        except Exception:
            # Fall back below
            candidates = []

        if not candidates:
            # Conservative, proven, high-volume large-caps (non-exhaustive)
            candidates = [
                "AAPL","MSFT","GOOGL","AMZN","NVDA","TSLA","META","NFLX","ADBE","CRM",
                "ORCL","INTC","AMD","QCOM","AVGO","TXN","AMAT","LRCX","KLAC","MCHP",
                "JPM","BAC","WFC","GS","MS","C","AXP","V","MA","PYPL",
                "COF","USB","PNC","TFC","BK","SCHW","BLK","SPGI","ICE","CME",
                "JNJ","UNH","PFE","ABT","TMO","DHR","BMY","LLY","MRK","AMGN",
                "GILD","BIIB","VRTX","REGN","ISRG","SYK","BDX","EW","A","CI",
                "WMT","PG","HD","DIS","NKE","MCD","SBUX","TGT","LOW","COST",
                "TJX","ROST","ULTA","LULU","CMG","BKNG",
                "BA","CAT","MMM","GE","HON","UPS","RTX","LMT","NOC","GD",
                "EMR","ETN","ITW","PH","DE","CMI","FDX","CSX","NSC","UNP",
                "XOM","CVX","COP","EOG","SLB","OXY","PXD","KMI","WMB","PSX",
                "NEE","DUK","SO","D","EXC","AEP","XEL","SRE","PEG","WEC",
                "AMT","PLD","CCI","EQIX","PSA","EXR","AVB","EQR","MAA","UDR",
                "VZ","T","CMCSA","LIN","APD","SHW","ECL","DD","DOW","PPG","NEM","FCX","VALE",
                "BRK.B","ABBV","PEP","INTU","IBM",
            ]

        # Deduplicate while preserving order
        seen: set[str] = set()
        deduped: List[str] = []
        for s in candidates:
            if s not in seen:
                seen.add(s)
                deduped.append(s)
        return deduped

    def get_or_build_universe(
        self,
        target_size: int = 120,
        analysis_days: int = 180,
        cache_path: str = "data/active_universe_120.json",
        max_age_days: int = 1,
        force_refresh: bool = False,
        min_price: float = 5.0,
        min_atr_pct: float = 0.01,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 3.0,
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
        end_date: Optional[date] = None,
    ) -> List[str]:
        """Return a cached, auto-refreshed active universe of size `target_size`.

        - Uses Polygon-derived large-cap candidates (or conservative fallback).
        - Computes metrics over the last `analysis_days` ending at `end_date` (default: today),
          with point-in-time boundaries to avoid forward-looking bias.
        - Caches the output to `cache_path` and refreshes if older than `max_age_days` or if forced.
        """
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        # Serve fresh cache if valid
        if not force_refresh and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                analysis_iso = payload.get("analysis_date")
                if analysis_iso:
                    analysis_dt = datetime.fromisoformat(analysis_iso)
                    age_days = (datetime.now() - analysis_dt).days
                    if age_days <= max_age_days:
                        syms = payload.get("symbols") or []
                        if isinstance(syms, list) and syms:
                            return [str(s) for s in syms][:target_size]
            except Exception:
                # proceed to rebuild
                pass

        # Build new universe deterministically from point-in-time window
        ed: date = end_date or date.today()
        sd: date = ed - timedelta(days=analysis_days)
        candidates = self._get_sp500_like_candidates()
        symbols = self.select_universe(
            candidates=candidates,
            start_date=sd.isoformat(),
            end_date=ed.isoformat(),
            target_size=target_size,
            min_price=min_price,
            min_atr_pct=min_atr_pct,
            spread_filter_enabled=spread_filter_enabled,
            spread_max_dollars=spread_max_dollars,
            spread_max_bps=spread_max_bps,
            spread_lookback_days=spread_lookback_days,
            spread_core_hours_only=spread_core_hours_only,
        )

        payload = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "target_size": target_size,
            "start_date": sd.isoformat(),
            "end_date": ed.isoformat(),
            "symbols": symbols,
            "criteria": {
                "min_price": min_price,
                "min_atr_pct": min_atr_pct,
                "spread_max_dollars": spread_max_dollars,
                "spread_max_bps": spread_max_bps,
                "spread_lookback_days": spread_lookback_days,
                "spread_core_hours_only": spread_core_hours_only,
            },
        }
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            # Non-fatal if cache write fails; still return symbols
            pass
        return symbols

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
            return {"adv": 0.0, "atr_pct": 0.0, "median_close": 0.0}
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
            return {"adv": 0.0, "atr_pct": 0.0, "median_close": 0.0}
        closes_sorted = sorted(closes)
        mid = len(closes_sorted) // 2
        if len(closes_sorted) % 2 == 0:
            median_close = 0.5 * (closes_sorted[mid - 1] + closes_sorted[mid])
        else:
            median_close = closes_sorted[mid]
        adv = sum(dollar_vols) / max(1, len(dollar_vols))
        atr_pct = sum(atr_fracs) / max(1, len(atr_fracs))
        return {"adv": adv, "atr_pct": atr_pct, "median_close": median_close}

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
        min_price: float = 5.0,
        min_atr_pct: float = 0.01,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 3.0,
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
    ) -> List[str]:
        metrics_by_symbol: Dict[str, Dict[str, float]] = {}
        for sym in candidates:
            rows = self._fetch_daily_aggs(sym, start_date, end_date)
            metrics = self._compute_metrics(rows)
            metrics_by_symbol[sym] = metrics
        # Price + ATR filters
        filtered = [
            s for s, m in metrics_by_symbol.items() if m["median_close"] >= min_price and m["atr_pct"] >= min_atr_pct
        ]
        # If too few pass, relax ATR% to half
        if len(filtered) < min(80, target_size // 2):
            filtered = [
                s
                for s, m in metrics_by_symbol.items()
                if m["median_close"] >= min_price and m["atr_pct"] >= (min_atr_pct * 0.5)
            ]
        # Spread filter (NBBO)
        if spread_filter_enabled and filtered:
            sf = [
                s
                for s in filtered
                if self._passes_spread_filter(
                    s, spread_max_dollars, spread_max_bps, spread_lookback_days, spread_core_hours_only
                )
            ]
            # If too few after spread filter, relax thresholds moderately
            if len(sf) < min(80, target_size // 2):
                sf = [
                    s
                    for s in filtered
                    if self._passes_spread_filter(
                        s, spread_max_dollars * 1.5, spread_max_bps * 1.7, spread_lookback_days, spread_core_hours_only
                    )
                ]
            filtered = sf
        # Rank by ADV descending
        ranked = sorted(filtered, key=lambda s: metrics_by_symbol[s]["adv"], reverse=True)
        return ranked[:target_size]
