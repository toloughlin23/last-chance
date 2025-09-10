from __future__ import annotations
from typing import List, Dict, Any

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient


class UniverseSelector:
    """Select a live trading universe (80–150 names) using only real Polygon data.

    Filters:
      - Price floor (median close >= min_price)
      - ATR% floor (average (high-low)/close >= min_atr_pct)
      - NBBO spread (median dollar <= spread_max_dollars OR median bps <= spread_max_bps)
    Ranking:
      - By average daily dollar volume (ADV = avg(close*volume))
    """

    def __init__(self, client: PolygonClient | None = None, quotes: QuotesClient | None = None) -> None:
        self.client = client or PolygonClient()
        self.quotes = quotes or QuotesClient()

    def _fetch_daily_aggs(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        data = self.client.get_aggs(symbol, 1, "day", start_date, end_date, limit=150, adjusted=True, sort="asc")
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
            l = float(r.get("l", 0.0))
            v = float(r.get("v", 0.0))
            if c > 0:
                closes.append(c)
                dollar_vols.append(c * v)
                atr_fracs.append(max(0.0, (h - l) / c))
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

    def _passes_spread_filter(self, symbol: str, spread_max_dollars: float, spread_max_bps: float, spread_days: int, core_hours_only: bool) -> bool:
        try:
            med_dollar, med_bps = self.quotes.median_spread_over_days(symbol, days=spread_days, core_hours_only=core_hours_only)
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
            s for s, m in metrics_by_symbol.items()
            if m["median_close"] >= min_price and m["atr_pct"] >= min_atr_pct
        ]
        # If too few pass, relax ATR% to half
        if len(filtered) < min(80, target_size // 2):
            filtered = [
                s for s, m in metrics_by_symbol.items()
                if m["median_close"] >= min_price and m["atr_pct"] >= (min_atr_pct * 0.5)
            ]
        # Spread filter (NBBO)
        if spread_filter_enabled and filtered:
            sf = [
                s for s in filtered
                if self._passes_spread_filter(s, spread_max_dollars, spread_max_bps, spread_lookback_days, spread_core_hours_only)
            ]
            # If too few after spread filter, relax thresholds moderately
            if len(sf) < min(80, target_size // 2):
                sf = [
                    s for s in filtered
                    if self._passes_spread_filter(s, spread_max_dollars * 1.5, spread_max_bps * 1.7, spread_lookback_days, spread_core_hours_only)
                ]
            filtered = sf
        # Rank by ADV descending
        ranked = sorted(filtered, key=lambda s: metrics_by_symbol[s]["adv"], reverse=True)
        return ranked[:target_size]


