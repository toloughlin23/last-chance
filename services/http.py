from typing import Any, Dict, Optional
import time

import requests


class HttpError(Exception):
    """Raised for HTTP and transport-level failures."""


class HttpClient:
    """Genuine HTTP client with bounded timeouts and exponential backoff.

    - Bounded timeout on every call (no hangs)
    - Retries on transient conditions (429/5xx, transport errors)
    - Stops after a finite number of attempts
    """

    def __init__(self, timeout: float = 30.0, max_retries: int = 3, backoff: float = 0.5) -> None:
        self.timeout: float = timeout
        self.max_retries: int = max(0, max_retries)
        self.backoff: float = max(0.0, backoff)

    def get_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        last_exc: Optional[Exception] = None
        # We make at most max_retries + 1 attempts
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.get(url, params=params, headers=headers, timeout=self.timeout)
                # Successful
                if resp.status_code == 200:
                    return resp.json()  # type: ignore[return-value]

                # Retry on common transient statuses
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise HttpError(f"Transient HTTP {resp.status_code}")

                # Non-transient client/server error
                resp.raise_for_status()
                return resp.json()  # Defensive; raise_for_status above should have thrown for errors

            except Exception as exc:
                last_exc = exc
                if attempt >= self.max_retries:
                    break
                # Exponential backoff with jitter
                sleep_seconds = self.backoff * (2 ** attempt)
                time.sleep(sleep_seconds)

        raise HttpError(str(last_exc) if last_exc else "HTTP request failed")

