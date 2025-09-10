import os
from datetime import datetime, timedelta, UTC
from typing import Any, Dict, List, Optional, Tuple

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class QuotesClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.http = http or HttpClient(timeout=30, max_retries=3, backoff=0.5)
        self.base = "https://api.polygon.io"

    def _params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        p = dict(params or {})
        p["apiKey"] = self.api_key
        return p

    def fetch_quotes_window(self, ticker: str, start_utc: datetime, end_utc: datetime, limit: int = 50000) -> List[Dict[str, Any]]:
        """Fetch NBBO quotes for a ticker in [start_utc, end_utc]. Uses v3 quotes.
        Note: Results are paginated; this returns up to 'limit' quotes for the window.
        """
        url = f"{self.base}/v3/quotes/{ticker}"
        params = {
            "timestamp.gte": start_utc.isoformat().replace("+00:00", "Z"),
            "timestamp.lte": end_utc.isoformat().replace("+00:00", "Z"),
            "limit": min(limit, 50000),
            "order": "asc",
        }
        data = self.http.get_json(url, params=self._params(params))
        results = data.get("results")
        return results if isinstance(results, list) else []

    @staticmethod
    def compute_median_spreads(quotes: List[Dict[str, Any]]) -> Tuple[float, float]:
        """Return (median_dollar_spread, median_bps_spread)."""
        spreads: List[float] = []
        bps: List[float] = []
        for q in quotes:
            bid = q.get("bidPrice")
            ask = q.get("askPrice")
            if bid is None or ask is None:
                # Some feeds use 'bp'/'ap' for bid/ask
                bid = q.get("bp")
                ask = q.get("ap")
            try:
                b = float(bid)
                a = float(ask)
                if b <= 0 or a <= 0 or a < b:
                    continue
                spread = a - b
                mid = 0.5 * (a + b)
                spreads.append(spread)
                if mid > 0:
                    bps.append((spread / mid) * 10000.0)
            except Exception:
                continue
        if not spreads:
            return 1e9, 1e9
        spreads_sorted = sorted(spreads)
        bps_sorted = sorted(bps) if bps else [1e9]
        m_idx = len(spreads_sorted) // 2
        med_spread = spreads_sorted[m_idx]
        med_bps = bps_sorted[len(bps_sorted) // 2]
        return med_spread, med_bps

    def median_spread_over_days(self, ticker: str, days: int = 5, core_hours_only: bool = True) -> Tuple[float, float]:
        """Compute median dollar and bps spread across the last 'days' trading sessions.
        core_hours_only: restrict to 14:30–21:00 UTC (9:30–16:00 ET)
        """
        end = datetime.now(UTC)
        medians: List[Tuple[float, float]] = []
        for i in range(1, days + 1):
            day_end = end - timedelta(days=i - 1)
            day_start = day_end.replace(hour=0, minute=0, second=0, microsecond=0)
            if core_hours_only:
                # Approx core hours in UTC; DST shifts handled by Polygon timestamps, this is a pragmatic window
                start_utc = day_start.replace(hour=13, minute=30)  # 13:30 UTC ≈ 9:30 ET (non-DST approx)
                end_utc = day_start.replace(hour=20, minute=0)     # 20:00 UTC ≈ 16:00 ET
            else:
                start_utc = day_start
                end_utc = day_start.replace(hour=23, minute=59, second=59)
            quotes = self.fetch_quotes_window(ticker, start_utc, end_utc, limit=20000)
            medians.append(self.compute_median_spreads(quotes))
        # Combine medians across days (median of medians)
        dollar = sorted([m[0] for m in medians])
        bps = sorted([m[1] for m in medians])
        return dollar[len(dollar) // 2], bps[len(bps) // 2]

