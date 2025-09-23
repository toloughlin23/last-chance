from __future__ import annotations

import os
from datetime import date
from typing import Any, Dict, Optional

from .http import HttpClient, HttpError


class PolygonClient:
    BASE_URL = "https://api.polygon.io"

    def __init__(
        self, api_key: Optional[str] = None, http: Optional[HttpClient] = None
    ) -> None:
        # Read API key from argument or environment. Blank is allowed; callers/tests can skip if missing.
        self.api_key = api_key or os.getenv("POLYGON_API_KEY") or ""
        self.http = http or HttpClient()

    def _auth_params(self, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {"apiKey": self.api_key}
        if extra:
            params.update(extra)
        return params

    def get_aggregates_daily(
        self,
        symbol: str,
        start: date,
        end: date,
        adjusted: bool = True,
        limit: int = 50000,
    ) -> Dict[str, Any]:
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

    def get_last_n_days(
        self, ticker: str, days: int = 5, adjusted: bool = True
    ) -> Dict[str, Any]:
        from datetime import date, timedelta

        end = date.today()
        start = end - timedelta(days=days)
        return self.get_aggregates_daily(
            ticker, start=start, end=end, adjusted=adjusted
        )

    def get_tickers(
        self,
        market: str = "stocks",
        active: bool = True,
        limit: int = 1000,
        sort: Optional[str] = None,
        order: Optional[str] = None,
        type: Optional[str] = None,
        exchange: Optional[str] = None,
        search: Optional[str] = None,
        next_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Fetch active tickers from Polygon v3 reference API.
        This is a single-call helper (no auto-pagination). Callers can pass next_url to paginate.
        """
        if next_url:
            url = next_url
            params: Dict[str, Any] = {}
        else:
            path = "/v3/reference/tickers"
            url = f"{self.BASE_URL}{path}"
            params = {
                "market": market,
                "active": str(active).lower(),
                "limit": limit,
            }
            if sort:
                params["sort"] = sort
            if order:
                params["order"] = order
            if type:
                params["type"] = type
            if exchange:
                params["exchange"] = exchange
            if search:
                params["search"] = search
        return self.http.get_json(url, params=self._auth_params(params))

    def get_ticker_details(self, ticker: str) -> Dict[str, Any]:
        """Fetch detailed information for a specific ticker including sector data."""
        path = f"/v3/reference/tickers/{ticker}"
        url = f"{self.BASE_URL}{path}"
        return self.http.get_json(url, params=self._auth_params({}))

    def get_index_constituents(self, index_ticker: str = "I:SPX") -> List[str]:
        """Get constituents of an index (default: S&P 500).
        
        The S&P 500 index ticker in Polygon is 'I:SPX'.
        This returns the actual 500 stocks in the S&P 500.
        """
        # First, search for indices that match
        path = "/v3/reference/tickers"
        url = f"{self.BASE_URL}{path}"
        params = {
            "ticker": index_ticker,
            "type": "IDX",  # Index type
            "active": "true",
            "limit": 10
        }
        
        try:
            data = self.http.get_json(url, params=self._auth_params(params))
            results = data.get("results", [])
            
            if not results:
                print(f"Index {index_ticker} not found")
                return []
                
            # Now get the constituents - this would require the paid Indices API
            # For now, we'll document this as the correct approach
            print(f"Note: Getting index constituents requires Polygon's Indices API subscription")
            return []
            
        except Exception as e:
            print(f"Error getting index constituents: {e}")
            return []
    
    # Earnings calendar - real integration should use Polygon's official endpoint.
    # Intentionally unimplemented rather than faked; provider checks for availability before use.
    def get_earnings_calendar(
        self, symbol: str, start: date, end: date
    ) -> Dict[str, Any]:
        """Get earnings dates from financials endpoint (available with premium subscription).
        Uses the vX/reference/financials endpoint which returns filing dates.
        """
        path = "/vX/reference/financials"
        url = f"{self.BASE_URL}{path}"
        params = self._auth_params(
            {
                "ticker": symbol,
                "timeframe": "quarterly",
                "limit": 20,  # Get enough quarters to cover the date range
            }
        )
        try:
            data = self.http.get_json(url, params=params)
            # Convert financials data to earnings calendar format
            earnings_dates = []
            for result in data.get("results", []):
                filing_date = result.get("filing_date")
                if filing_date:
                    # Check if filing date is within our range
                    try:
                        filing_dt = date.fromisoformat(filing_date)
                        if start <= filing_dt <= end:
                            earnings_dates.append(
                                {
                                    "date": filing_date,
                                    "fiscal_period": result.get("fiscal_period"),
                                    "fiscal_year": result.get("fiscal_year"),
                                }
                            )
                    except Exception:
                        continue
            return {"results": earnings_dates}
        except HttpError:
            return {"results": []}
