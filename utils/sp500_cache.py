import os
import json
from datetime import datetime
from typing import List


class SP500Cache:
    def __init__(self, path: str = "pipeline/sp500_symbols.json"):
        self.path = path

    def load_if_fresh(self) -> List[str]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r") as f:
                payload = json.load(f)
            date_str = payload.get("date")
            syms = payload.get("symbols") or []
            if not date_str or not syms:
                return []
            if date_str == datetime.utcnow().date().isoformat():
                return syms
        except Exception:
            return []
        return []

    def save_today(self, symbols: List[str]) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        payload = {"date": datetime.utcnow().date().isoformat(), "symbols": symbols}
        with open(self.path, "w") as f:
            json.dump(payload, f)

