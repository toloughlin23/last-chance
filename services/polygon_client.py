from __future__ import annotations

import os
from datetime import date
from typing import Any, Dict, Optional

from .http import HttpClient


class PolygonClient:
    BASE_URL = "https://api.polygon.io"

    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None) -> None:
        # Read API key from argument or environment. Blank is allowed; callers/tests can skip if missing.
        self.api_key = api_key or os.getenv("POLYGON_API_KEY") or ""
        self.http = http or HttpClient()

    def _auth_params(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"apiKey": self.api_key}
        if extra:
            params.update(extra)
        return params

    def get_aggregates_daily(self, symbol: str, start: date, end: date, adjusted: bool = True, limit: int = 50000) -> Dict[str, Any]:
        """Fetch daily aggregate bars for a symbol between two dates (inclusive)."""
        path = f"/v2/aggs/ticker/{symbol}/range/1/day/{start.isoformat()}/{end.isoformat()}"
        url = f"{self.BASE_URL}{path}"
        params = self._auth_params({"adjusted": str(adjusted).lower(), "limit": limit})
        return self.http.get_json(url, params=params)

    # Backwards compatible method used elsewhere in the repo
    def get_aggs(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        from_date: str,
        to_date: str,
        limit: int = 500,
        adjusted: bool = True,
        sort: str = "asc",
    ) -> Dict[str, Any]:
        path = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        url = f"{self.BASE_URL}{path}"
        params = self._auth_params(
            {"adjusted": str(adjusted).lower(), "sort": sort, "limit": limit}
        )
        return self.http.get_json(url, params=params)

    def get_last_n_days(self, ticker: str, days: int = 5, adjusted: bool = True) -> Dict[str, Any]:
        from datetime import date, timedelta

        end = date.today()
        start = end - timedelta(days=days)
        return self.get_aggregates_daily(ticker, start=start, end=end, adjusted=adjusted)

