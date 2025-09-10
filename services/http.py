import time
import json
from typing import Any, Dict, Optional

import requests


class HttpError(Exception):
    pass


class HttpClient:
    def __init__(self, timeout_seconds: float = 15.0, max_retries: int = 3, backoff_base_seconds: float = 0.5) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.backoff_base_seconds = backoff_base_seconds

    def get_json(self, url: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=self.timeout_seconds)
                if resp.status_code >= 500:
                    raise HttpError(f"Server error {resp.status_code}: {resp.text}")
                if resp.status_code >= 400:
                    # Client errors: don't retry
                    raise HttpError(f"Client error {resp.status_code}: {resp.text}")
                return resp.json()  # type: ignore[return-value]
            except Exception as exc:  # requests exceptions or HttpError
                last_error = exc
                if attempt == self.max_retries:
                    break
                sleep_seconds = self.backoff_base_seconds * (2 ** attempt)
                time.sleep(sleep_seconds)
        raise HttpError(str(last_error))

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

