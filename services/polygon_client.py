import os
from typing import Any, Dict, Optional

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class PolygonClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        self.http = http or HttpClient()
        self.base = "https://api.polygon.io"

    def _with_key(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = dict(params or {})
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        params["apiKey"] = self.api_key
        return params

    def get_aggs(self, ticker: str, multiplier: int, timespan: str, from_date: str, to_date: str, limit: int = 500, adjusted: bool = True, sort: str = "asc") -> Dict[str, Any]:
        url = f"{self.base}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
        params = self._with_key({"adjusted": str(adjusted).lower(), "sort": sort, "limit": limit})
        return self.http.get_json(url, params=params)

