import time
from typing import Any, Dict, Optional
import requests


class HttpClient:
    def __init__(self, timeout: int = 30, max_retries: int = 3, backoff: float = 0.5):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff

    def get_json(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        last_exc: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                if resp.status_code == 200:
                    return resp.json()
                # Retry on 429/5xx
                if resp.status_code in (429, 500, 502, 503, 504):
                    time.sleep(self.backoff * (2 ** attempt))
                    continue
                resp.raise_for_status()
            except Exception as exc:
                last_exc = exc
                time.sleep(self.backoff * (2 ** attempt))
        if last_exc:
            raise last_exc
        return {}

