import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta, UTC
from concurrent.futures import ThreadPoolExecutor, as_completed

from services.http import HttpClient
from services.polygon_client import PolygonClient
from utils.env_loader import load_env_from_known_locations


class SSRClient:
    def __init__(self, api_key: Optional[str] = None, http: Optional[HttpClient] = None, polygon: Optional[PolygonClient] = None):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("POLYGON_API_KEY")
        if not self.api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        self.http = http or HttpClient()
        self.polygon = polygon or PolygonClient(api_key=self.api_key, http=self.http)

    def _prev_close(self, symbol: str, prev_date_iso: str) -> float:
        data = self.polygon.get_aggs(symbol, 1, "day", prev_date_iso, prev_date_iso, limit=1, adjusted=True, sort="asc")
        rows = data.get("results") or []
        return float(rows[0].get("c", 0.0)) if rows else 0.0

    def _intraday_low(self, symbol: str, open_ts_utc: datetime, close_ts_utc: datetime) -> float:
        data = self.polygon.get_aggs(symbol, 1, "minute", open_ts_utc.isoformat().replace("+00:00", "Z"), close_ts_utc.isoformat().replace("+00:00", "Z"), limit=200, adjusted=True, sort="asc")
        rows = data.get("results") or []
        lows = [float(r.get("l", 0.0)) for r in rows if r]
        return min(lows) if lows else 0.0

    def ssr_active_today(self, symbols: List[str], us_open_local: datetime) -> Dict[str, bool]:
        # Determine SSR based on 10% decline from prior close at any time during the day
        from datetime import timedelta
        prev_date = (us_open_local.date() - timedelta(days=1)).isoformat()
        open_utc = us_open_local.astimezone(UTC)
        close_utc = us_open_local.replace(hour=16, minute=0, second=0, microsecond=0).astimezone(UTC)

        out: Dict[str, bool] = {}
        with ThreadPoolExecutor(max_workers=min(12, max(1, len(symbols)))) as ex:
            futs = {}
            for s in symbols:
                futs[ex.submit(self._check_one, s, prev_date, open_utc, close_utc)] = s
            for fut in as_completed(futs):
                sym = futs[fut]
                try:
                    out[sym] = bool(fut.result())
                except Exception:
                    out[sym] = False
        return out

    def _check_one(self, symbol: str, prev_date_iso: str, open_utc: datetime, close_utc: datetime) -> bool:
        prev_close = self._prev_close(symbol, prev_date_iso)
        if prev_close <= 0:
            return False
        intraday_low = self._intraday_low(symbol, open_utc, close_utc)
        if intraday_low <= 0:
            return False
        decline = (prev_close - intraday_low) / prev_close
        return decline >= 0.10

