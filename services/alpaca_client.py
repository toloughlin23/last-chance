import os
from typing import Any, Dict, Optional, List
import requests

from utils.env_loader import load_env_from_known_locations


class AlpacaClient:
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, paper: bool = True):
        load_env_from_known_locations()
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.secret_key = secret_key or os.getenv("ALPACA_SECRET_KEY")
        self.paper = paper
        # Lazy-enable network usage only when credentials are present
        self.enabled = bool(self.api_key and self.secret_key)
        self.base = "https://paper-api.alpaca.markets" if paper else "https://api.alpaca.markets"
        self.session = None
        if self.enabled:
            self.session = requests.Session()
            self.session.headers.update({
                "APCA-API-KEY-ID": self.api_key,
                "APCA-API-SECRET-KEY": self.secret_key,
                "Content-Type": "application/json"
            })

    def _require_configured(self) -> None:
        """Ensure credentials are configured before making network calls."""
        if not self.enabled:
            raise RuntimeError("Alpaca credentials not set in env")

    def get_account(self) -> Dict[str, Any]:
        self._require_configured()
        resp = self.session.get(f"{self.base}/v2/account", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def place_order(self, symbol: str, qty: int, side: str, type_: str = "market", time_in_force: str = "day", paper_guard: bool = True) -> Dict[str, Any]:
        self._require_configured()
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

    def submit_order(self, symbol: str, qty: str, side: str, type: str, time_in_force: str = "day", 
                    limit_price: Optional[str] = None, stop_price: Optional[str] = None) -> Dict[str, Any]:
        """Submit order with enhanced parameters"""
        self._require_configured()
        order = {
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": type,
            "time_in_force": time_in_force
        }
        
        if limit_price:
            order["limit_price"] = limit_price
        if stop_price:
            order["stop_price"] = stop_price
            
        resp = self.session.post(f"{self.base}/v2/orders", json=order, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all positions"""
        self._require_configured()
        resp = self.session.get(f"{self.base}/v2/positions", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_position(self, symbol: str) -> Dict[str, Any]:
        """Get specific position"""
        self._require_configured()
        resp = self.session.get(f"{self.base}/v2/positions/{symbol}", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_orders(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get orders"""
        self._require_configured()
        params = {"limit": limit}
        if status:
            params["status"] = status
            
        resp = self.session.get(f"{self.base}/v2/orders", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def get_order(self, order_id: str) -> Dict[str, Any]:
        """Get specific order"""
        self._require_configured()
        resp = self.session.get(f"{self.base}/v2/orders/{order_id}", timeout=30)
        resp.raise_for_status()
        return resp.json()

    def cancel_order(self, order_id: str) -> bool:
        """Cancel order"""
        self._require_configured()
        try:
            resp = self.session.delete(f"{self.base}/v2/orders/{order_id}", timeout=30)
            resp.raise_for_status()
            return True
        except Exception:
            return False

    def cancel_all_orders(self) -> bool:
        """Cancel all orders"""
        self._require_configured()
        try:
            resp = self.session.delete(f"{self.base}/v2/orders", timeout=30)
            resp.raise_for_status()
            return True
        except Exception:
            return False

