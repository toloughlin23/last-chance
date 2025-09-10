import os
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class EarningsClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.http = http or HttpClient()
        self.base = "https://api.polygon.io"

    def _query_one(self, symbol: str, date_iso: str) -> bool:
        # Polygon earnings reference endpoint; checks announcements on the given date
        url = f"{self.base}/vX/reference/earnings"
        params = {
            "ticker": symbol,
            "announced_on.gte": date_iso,
            "announced_on.lte": date_iso,
            "limit": 1,
            "order": "asc",
            "apiKey": self.api_key,
        }
        data = self.http.get_json(url, params=params)
        results = data.get("results") or data.get("earnings") or []
        return bool(results)

    def tickers_with_earnings_on(self, symbols: List[str], date_iso: str, max_workers: int = 8) -> Dict[str, bool]:
        if not symbols:
            return {}
        out: Dict[str, bool] = {}
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futs = {ex.submit(self._query_one, s, date_iso): s for s in symbols}
            for fut in as_completed(futs):
                sym = futs[fut]
                try:
                    out[sym] = bool(fut.result())
                except Exception:
                    out[sym] = False
        return out

