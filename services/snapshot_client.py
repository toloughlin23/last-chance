import os
from typing import Any, Dict, List, Optional

from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class SnapshotClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.http = http or HttpClient()
        self.base = "https://api.polygon.io"

    def fetch_trading_halts(self, symbols: List[str]) -> Dict[str, bool]:
        """Return {symbol: tradingHalted} for provided symbols using v2 snapshot tickers.
        Note: Polygon enforces limits on tickers per call; we concatenate up to ~50.
        """
        if not symbols:
            return {}
        joined = ",".join(symbols[:50])
        url = f"{self.base}/v2/snapshot/locale/us/markets/stocks/tickers"
        params = {"tickers": joined, "apiKey": self.api_key}
        data = self.http.get_json(url, params=params)
        out: Dict[str, bool] = {}
        tickers = data.get("tickers") or []
        for t in tickers:
            sym = t.get("ticker")
            halted = bool(t.get("tradingHalted") or t.get("trading_halted") or False)
            if sym:
                out[sym] = halted
        return out

