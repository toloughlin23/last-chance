import os
from typing import Any, Dict, Optional
import requests

from utils.env_loader import load_env_from_known_locations


class AlpacaClient:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, paper: bool = True):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.secret_key = secret_key or os.getenv("ALPACA_SECRET_KEY")
        self.paper = paper
        if not self.api_key or not self.secret_key:
            raise RuntimeError("Alpaca credentials not set in env")
        self.base = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        self.session = requests.Session()
        self.session.headers.update({
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key,
            "Content-Type": "application/json"
        })

    def get_account(self) -> Dict[str, Any]:
        resp = self.session.get(f"{self.base}/v2/account", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def place_order(self, symbol: str, qty: int, side: str, type_: str = "market", time_in_force: str = "day", paper_guard: bool = True) -> Dict[str, Any]:
        if paper_guard and not self.paper:
            raise RuntimeError("Safety: live trading blocked without explicit opt-in")
        order = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type_,
            "time_in_force": time_in_force
        }
        resp = self.session.post(f"{self.base}/v2/orders", json=order, timeout=30)
        resp.raise_for_status()
        return resp.json()

