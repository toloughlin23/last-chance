import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class NewsClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.http = http or HttpClient()
        self.base = "https://api.polygon.io"

    def _params(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        p = dict(params or {})
        p["apiKey"] = self.api_key
        return p

    def fetch_symbol_news(self, ticker: str, published_gte_utc: Optional[str] = None, limit: int = 50, order: str = "desc") -> List[Dict[str, Any]]:
        """Fetch recent news for a ticker.
        published_gte_utc: ISO8601 UTC string (e.g., 2025-09-01T00:00:00Z)
        Returns list of articles (dicts) from Polygon.
        """
        url = f"{self.base}/v2/reference/news"
        params: Dict[str, Any] = {"ticker": ticker, "limit": limit, "order": order}
        if published_gte_utc:
            params["published_utc.gte"] = published_gte_utc
        data = self.http.get_json(url, params=self._params(params))
        results = data.get("results")
        if isinstance(results, list):
            return results
        return []

