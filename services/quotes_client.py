import os
from datetime import datetime, timedelta
from datetime import timezone as _timezone
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations

UTC = _timezone.utc


class QuotesClient:
    def __init__(
        self, api_key: Optional[str] = None, http: Optional[HttpClient] = None
    ):
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

    def fetch_quotes_window(
        self, ticker: str, start_utc: datetime, end_utc: datetime, limit: int = 50000
    ) -> List[Dict[str, Any]]:
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
        """Return (median_dollar_spread, median_bps_spread).
        Enhanced to handle multiple quote formats from different Polygon API versions.
        """
        spreads: List[float] = []
        bps: List[float] = []

        # Track which format we're seeing for debugging
        format_found = None

        for q in quotes:
            # Try all possible field name formats
            # Polygon v3 uses underscores
            bid = q.get("bid_price")
            ask = q.get("ask_price")
            if bid is not None and ask is not None:
                format_found = "v3_underscore"

            # Polygon v2 might use camelCase
            if bid is None or ask is None:
                bid = q.get("bidPrice")
                ask = q.get("askPrice")
                if bid is not None and ask is not None:
                    format_found = "v2_camelCase"

            # Some feeds use abbreviated names
            if bid is None or ask is None:
                bid = q.get("bp")
                ask = q.get("ap")
                if bid is not None and ask is not None:
                    format_found = "abbreviated"

            # Legacy format with different structure
            if bid is None or ask is None:
                bid = q.get("b")
                ask = q.get("a")
                if bid is not None and ask is not None:
                    format_found = "legacy_single_letter"

            try:
                b = float(cast(Union[str, float, int], bid))
                a = float(cast(Union[str, float, int], ask))
                if b <= 0 or a <= 0 or a < b:
                    continue
                spread = a - b
                mid = 0.5 * (a + b)
                spreads.append(spread)
                if mid > 0:
                    bps.append((spread / mid) * 10000.0)
            except Exception:
                continue

        # Enhanced logging when no valid spreads found
        if not spreads:
            if quotes and format_found is None:
                # Log what fields we actually see for debugging
                sample_fields = list(quotes[0].keys()) if quotes else []
                print(
                    f"⚠️ QuotesClient: No recognized bid/ask fields. Found fields: {sample_fields[:10]}"
                )

            # Return sentinel values that indicate missing data but won't break filtering
            # These are high enough to fail filters but not absurdly high
            return 1e9, 1e9

        # Calculate medians from valid spreads
        spreads_sorted = sorted(spreads)
        bps_sorted = sorted(bps) if bps else [1e9]
        m_idx = len(spreads_sorted) // 2

        # Handle even/odd length arrays properly
        if len(spreads_sorted) % 2 == 0 and m_idx > 0:
            med_spread = (spreads_sorted[m_idx - 1] + spreads_sorted[m_idx]) / 2.0
        else:
            med_spread = spreads_sorted[m_idx]

        if len(bps_sorted) % 2 == 0 and len(bps_sorted) // 2 > 0:
            med_bps = (
                bps_sorted[len(bps_sorted) // 2 - 1] + bps_sorted[len(bps_sorted) // 2]
            ) / 2.0
        else:
            med_bps = bps_sorted[len(bps_sorted) // 2]

        return med_spread, med_bps

    def median_spread_over_days(
        self, ticker: str, days: int = 5, core_hours_only: bool = True
    ) -> Tuple[float, float]:
        """Compute median dollar and bps spread across the last 'days' TRADING sessions.
        core_hours_only: restrict to 14:30–21:00 UTC (9:30–16:00 ET)
        """
        end = datetime.now(UTC)
        medians: List[Tuple[float, float]] = []
        days_checked = 0
        total_days_back = 0

        # Keep going back until we find 'days' trading days
        while len(medians) < days and total_days_back < days * 3:  # Safety limit
            day_to_check = end - timedelta(days=total_days_back)
            day_start = day_to_check.replace(hour=0, minute=0, second=0, microsecond=0)

            # Skip weekends
            if day_start.weekday() >= 5:  # Saturday = 5, Sunday = 6
                total_days_back += 1
                continue

            if core_hours_only:
                # Approx core hours in UTC; DST shifts handled by Polygon timestamps
                start_utc = day_start.replace(hour=13, minute=30)  # 13:30 UTC ≈ 9:30 ET
                end_utc = day_start.replace(hour=20, minute=0)  # 20:00 UTC ≈ 16:00 ET
            else:
                start_utc = day_start.replace(
                    hour=14, minute=0
                )  # Start at 14:00 UTC to ensure market is open
                end_utc = day_start.replace(hour=21, minute=0)  # End at 21:00 UTC

            quotes = self.fetch_quotes_window(ticker, start_utc, end_utc, limit=20000)

            # Only use days with valid quotes
            if quotes:
                day_median = self.compute_median_spreads(quotes)
                # Skip days with sentinel values (no valid spreads found)
                if day_median[0] < 1000:  # Reasonable spread threshold
                    medians.append(day_median)

            total_days_back += 1

        # If we found valid data, compute median of medians
        if medians:
            dollar = sorted([m[0] for m in medians])
            bps = sorted([m[1] for m in medians])
            return dollar[len(dollar) // 2], bps[len(bps) // 2]
        else:
            # No valid trading days found - return sentinel values
            return 1e9, 1e9
