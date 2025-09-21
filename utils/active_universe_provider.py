"""
Active Universe Provider - 100% GENUINE (Polygon-first)
- Discovers large-cap candidates (Polygon if available; conservative fallback otherwise)
- Builds a 120-symbol active universe using UniverseSelector
- Caches to disk and refreshes when stale
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from typing import List, Optional

from services.polygon_client import PolygonClient
from utils.universe_selector import UniverseSelector


class ActiveUniverseProvider:
    def __init__(self, polygon_client: Optional[PolygonClient] = None) -> None:
        self.polygon_client = polygon_client or PolygonClient()

    def _discover_candidates(self) -> List[str]:
        candidates: List[str] = []
        try:
            if hasattr(self.polygon_client, "get_tickers"):
                data = self.polygon_client.get_tickers(market="stocks", active=True, limit=1000)
                results = data.get("results") if isinstance(data, dict) else None
                if results:
                    for t in results:
                        sym = t.get("ticker")
                        mcap = t.get("market_cap", 0)
                        if isinstance(sym, str) and sym and isinstance(mcap, (int, float)) and mcap > 8_000_000_000:
                            candidates.append(sym)
        except Exception:
            candidates = []

        if not candidates:
            candidates = [
                "AAPL","MSFT","GOOGL","AMZN","NVDA","TSLA","META","NFLX","ADBE","CRM",
                "ORCL","INTC","AMD","QCOM","AVGO","TXN","AMAT","LRCX","KLAC","MCHP",
                "JPM","BAC","WFC","GS","MS","C","AXP","V","MA","PYPL",
                "COF","USB","PNC","TFC","BK","SCHW","BLK","SPGI","ICE","CME",
                "JNJ","UNH","PFE","ABT","TMO","DHR","BMY","LLY","MRK","AMGN",
                "GILD","BIIB","VRTX","REGN","ISRG","SYK","BDX","EW","A","CI",
                "WMT","PG","HD","DIS","NKE","MCD","SBUX","TGT","LOW","COST",
                "TJX","ROST","ULTA","LULU","CMG","BKNG",
                "BA","CAT","MMM","GE","HON","UPS","RTX","LMT","NOC","GD",
                "EMR","ETN","ITW","PH","DE","CMI","FDX","CSX","NSC","UNP",
                "XOM","CVX","COP","EOG","SLB","OXY","PXD","KMI","WMB","PSX",
                "NEE","DUK","SO","D","EXC","AEP","XEL","SRE","PEG","WEC",
                "AMT","PLD","CCI","EQIX","PSA","EXR","AVB","EQR","MAA","UDR",
                "VZ","T","CMCSA","LIN","APD","SHW","ECL","DD","DOW","PPG","NEM","FCX","VALE",
                "BRK.B","ABBV","PEP","INTU","IBM",
            ]

        # Deduplicate while preserving order
        seen: set[str] = set()
        deduped: List[str] = []
        for s in candidates:
            if s not in seen:
                seen.add(s)
                deduped.append(s)
        return deduped

    def get_active_universe(
        self,
        target_size: int = 120,
        analysis_days: int = 180,
        cache_path: str = "data/active_universe_120.json",
        max_age_days: int = 1,
        force_refresh: bool = False,
        min_price: float = 5.0,
        min_atr_pct: float = 0.01,
        spread_filter_enabled: bool = True,
        spread_max_dollars: float = 0.02,
        spread_max_bps: float = 3.0,
        spread_lookback_days: int = 5,
        spread_core_hours_only: bool = True,
        end_date: Optional[date] = None,
    ) -> List[str]:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        if not force_refresh and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                analysis_iso = payload.get("analysis_date")
                if analysis_iso:
                    analysis_dt = datetime.fromisoformat(analysis_iso)
                    age_days = (datetime.now() - analysis_dt).days
                    if age_days <= max_age_days:
                        syms = payload.get("symbols") or []
                        if isinstance(syms, list) and syms:
                            return [str(s) for s in syms][:target_size]
            except Exception:
                pass

        ed: date = end_date or date.today()
        sd: date = ed - timedelta(days=analysis_days)

        candidates = self._discover_candidates()
        selector = UniverseSelector()
        symbols = selector.select_universe(
            candidates=candidates,
            start_date=sd.isoformat(),
            end_date=ed.isoformat(),
            target_size=target_size,
            min_price=min_price,
            min_atr_pct=min_atr_pct,
            spread_filter_enabled=spread_filter_enabled,
            spread_max_dollars=spread_max_dollars,
            spread_max_bps=spread_max_bps,
            spread_lookback_days=spread_lookback_days,
            spread_core_hours_only=spread_core_hours_only,
        )

        payload = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "target_size": target_size,
            "start_date": sd.isoformat(),
            "end_date": ed.isoformat(),
            "symbols": symbols,
            "criteria": {
                "min_price": min_price,
                "min_atr_pct": min_atr_pct,
                "spread_max_dollars": spread_max_dollars,
                "spread_max_bps": spread_max_bps,
                "spread_lookback_days": spread_lookback_days,
                "spread_core_hours_only": spread_core_hours_only,
            },
        }
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass
        return symbols
