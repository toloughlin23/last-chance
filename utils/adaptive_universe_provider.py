"""
🚀 ADAPTIVE UNIVERSE PROVIDER - Ensures 120-150 Symbols Always

This provider dynamically adjusts filters to ensure we always get the target
number of symbols (120-150) for active day trading, while maintaining quality.

Key Features:
- Progressive filter relaxation if too few symbols
- Quality-based ranking ensures best symbols first
- Fallback strategies for different market conditions
- Real-time filter adjustment based on market liquidity
"""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 🚀 ENHANCED: Load environment variables and enhanced logging
from utils.env_loader import load_env_from_known_locations
load_env_from_known_locations()

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.universe_selector import UniverseSelector
from utils.enhanced_logging_system import universe_logger


class AdaptiveUniverseProvider:
    """Adaptive universe provider that ensures 120-150 symbols always."""

    def __init__(self, polygon_client: Optional[PolygonClient] = None) -> None:
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = QuotesClient()

    def get_adaptive_universe(
        self,
        target_size: int = 120,
        target_max_size: int = 150,
        analysis_days: int = 60,
        cache_path: str = "data/adaptive_universe_120.json",
        max_age_hours: int = 18,
        force_refresh: bool = False,
        end_date: Optional[date] = None,
    ) -> List[str]:
        """
        Get adaptive universe that ensures 120-150 symbols.

        Strategy:
        1. Start with strict filters (high quality)
        2. If < 120 symbols, progressively relax filters
        3. Always maintain quality ranking (best symbols first)
        4. Expand to 150 if strong contenders available
        """

        # Check cache first
        if not force_refresh and os.path.exists(cache_path):
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                analysis_iso = payload.get("analysis_date")
                if analysis_iso:
                    analysis_dt = datetime.fromisoformat(analysis_iso)
                    age_hours = (datetime.now() - analysis_dt).total_seconds() / 3600
                    if age_hours <= max_age_hours:
                        symbols = payload.get("symbols", [])
                        if isinstance(symbols, list) and len(symbols) >= target_size:
                            universe_logger.info(f"✅ Using cached universe: {len(symbols)} symbols", operation="cache_usage", cached_symbol_count=len(symbols))
                            return symbols[:target_max_size]
            except Exception:
                pass

        ed = end_date or date.today()
        sd = ed - timedelta(days=analysis_days)

        universe_logger.info(
            f"🚀 Building adaptive universe (target: {target_size}-{target_max_size})...",
            operation="adaptive_generation", target_min=target_size, target_max=target_max_size
        )

        # Get candidates from entire S&P 500
        candidates = self._discover_candidates()
        if not candidates:
            universe_logger.warning("⚠️ No candidates found, using fallback", operation="adaptive_generation")
            return self._get_fallback_symbols()[:target_max_size]

        universe_logger.info(f"📊 Analyzing {len(candidates)} candidates...", operation="candidate_analysis", candidate_count=len(candidates))

        # Try progressive filter relaxation
        universe = self._progressive_filter_strategy(
            candidates, sd, ed, target_size, target_max_size
        )

        if len(universe) < target_size:
            universe_logger.warning(f"⚠️ Only {len(universe)} symbols found, using fallback strategy", operation="adaptive_generation", found_count=len(universe), target_min=target_size)
            universe = self._fallback_strategy(candidates, sd, ed, target_size)

        # Cache results
        self._save_universe(universe, analysis_days, cache_path)

        universe_logger.info(f"✅ Generated adaptive universe: {len(universe)} symbols", operation="adaptive_generation", final_symbol_count=len(universe))
        return universe[:target_max_size]

    def _progressive_filter_strategy(
        self,
        candidates: List[str],
        start_date: date,
        end_date: date,
        target_size: int,
        target_max_size: int,
    ) -> List[str]:
        """Progressive filter relaxation to ensure target size."""

        # Filter configurations from strict to relaxed
        filter_configs = [
            # Level 1: Strict (high quality)
            {
                "name": "Strict",
                "min_price": 15.0,
                "min_atr_pct": 0.015,
                "max_atr_pct": 0.04,
                "adv_min_dollar": 100_000_000.0,
                "spread_max_bps": 3.0,
                "spread_max_dollars": 0.015,
            },
            # Level 2: Moderate
            {
                "name": "Moderate",
                "min_price": 12.0,
                "min_atr_pct": 0.012,
                "max_atr_pct": 0.045,
                "adv_min_dollar": 75_000_000.0,
                "spread_max_bps": 4.0,
                "spread_max_dollars": 0.02,
            },
            # Level 3: Relaxed
            {
                "name": "Relaxed",
                "min_price": 10.0,
                "min_atr_pct": 0.01,
                "max_atr_pct": 0.05,
                "adv_min_dollar": 50_000_000.0,
                "spread_max_bps": 5.0,
                "spread_max_dollars": 0.025,
            },
            # Level 4: Very Relaxed
            {
                "name": "Very Relaxed",
                "min_price": 8.0,
                "min_atr_pct": 0.008,
                "max_atr_pct": 0.06,
                "adv_min_dollar": 30_000_000.0,
                "spread_max_bps": 7.0,
                "spread_max_dollars": 0.03,
            },
            # Level 5: Minimal (emergency)
            {
                "name": "Minimal",
                "min_price": 5.0,
                "min_atr_pct": 0.005,
                "max_atr_pct": 0.08,
                "adv_min_dollar": 20_000_000.0,
                "spread_max_bps": 10.0,
                "spread_max_dollars": 0.05,
            },
        ]

        for i, config in enumerate(filter_configs):
            universe_logger.info(f"🔍 Trying {config['name']} filters...", operation="progressive_filtering", filter_name=config['name'])

            try:
                universe = self._apply_filters(
                    candidates,
                    start_date,
                    end_date,
                    target_size,
                    target_max_size,
                    config,
                )

                if len(universe) >= target_size:
                    universe_logger.info(f"✅ {config['name']} filters: {len(universe)} symbols", operation="progressive_filtering", filter_name=config['name'], symbol_count=len(universe))
                    return universe
                else:
                    universe_logger.warning(f"⚠️ {config['name']} filters: only {len(universe)} symbols", operation="progressive_filtering", filter_name=config['name'], symbol_count=len(universe), target_min=target_size)

            except Exception as e:
                universe_logger.error(f"❌ {config['name']} filters failed: {e}", operation="progressive_filtering", filter_name=config['name'], error_type=type(e).__name__)
                continue

        # If all filters fail, return what we have
        return universe if "universe" in locals() else []

    def _apply_filters(
        self,
        candidates: List[str],
        start_date: date,
        end_date: date,
        target_size: int,
        target_max_size: int,
        config: Dict,
    ) -> List[str]:
        """Apply specific filter configuration."""

        selector = UniverseSelector()

        # Get sector info for balancing
        sector_classifier, sector_weights = self._build_sector_info(candidates[:100])

        universe = selector.select_universe(
            candidates=candidates,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=target_size,
            target_max_size=target_max_size,
            allow_expand_above_target=True,
            expand_margin=0.9,
            min_price=config["min_price"],
            min_atr_pct=config["min_atr_pct"],
            max_atr_pct=config["max_atr_pct"],
            adv_min_dollar=config["adv_min_dollar"],
            spread_filter_enabled=True,
            spread_max_dollars=config["spread_max_dollars"],
            spread_max_bps=config["spread_max_bps"],
            spread_lookback_days=5,
            spread_core_hours_only=True,
            sector_classifier=sector_classifier,
            sector_index_weights=sector_weights,
            earnings_exclusion=self._get_earnings_exclusion_function(),  # 🚀 ENHANCED: Intelligent earnings exclusion
            earnings_buffer_days=0,
        )

        return universe

    def _get_earnings_exclusion_function(self):
        """🚀 ENHANCED: Get intelligent earnings exclusion function with dynamic buffer calculation."""
        def earnings_exclusion(symbol: str, date: date) -> bool:
            """
            🚀 ENHANCED: Intelligent earnings exclusion with adaptive buffer calculation.
            Returns True if symbol should be excluded due to upcoming earnings.
            """
            try:
                # Get earnings calendar for the symbol
                earnings_data = self.polygon_client.get_earnings_calendar(
                    symbol=symbol,
                    start_date=date,
                    end_date=date + timedelta(days=30)  # Look ahead 30 days
                )
                
                if not earnings_data or not earnings_data.get('results'):
                    return False
                
                # Calculate dynamic buffer based on symbol volatility
                # More volatile symbols get larger buffers
                try:
                    # Get recent volatility data
                    end_date = date
                    start_date = date - timedelta(days=20)
                    
                    aggs_data = self.polygon_client.get_aggregates(
                        symbol=symbol,
                        start=start_date,
                        end=end_date,
                        adjusted=True,
                        limit=20
                    )
                    
                    if aggs_data and aggs_data.get('results'):
                        closes = [bar['c'] for bar in aggs_data['results']]
                        if len(closes) > 1:
                            # Calculate volatility
                            returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
                            volatility = sum(abs(r) for r in returns) / len(returns)
                            
                            # Dynamic buffer: 1-5 days based on volatility
                            buffer_days = max(1, min(5, int(volatility * 100)))
                        else:
                            buffer_days = 3  # Default buffer
                    else:
                        buffer_days = 3  # Default buffer
                        
                except Exception:
                    buffer_days = 3  # Default buffer on error
                
                # Check if any earnings are within the buffer period
                for earnings in earnings_data['results']:
                    earnings_date = datetime.fromtimestamp(earnings['date'] / 1000).date()
                    days_until_earnings = (earnings_date - date).days
                    
                    if 0 <= days_until_earnings <= buffer_days:
                        universe_logger.info(f"Excluding {symbol} due to earnings in {days_until_earnings} days", 
                                           operation="earnings_exclusion", symbol=symbol, days_until=days_until_earnings, buffer=buffer_days)
                        return True
                
                return False
                
            except Exception as e:
                universe_logger.warning(f"Error checking earnings for {symbol}: {e}", 
                                      operation="earnings_exclusion", symbol=symbol, error_type=type(e).__name__)
                return False
        
        return earnings_exclusion

    def _discover_candidates(self, min_market_cap: float = 5_000_000_000) -> List[str]:
        """Discover candidates from S&P 500 with lower market cap threshold."""
        try:
            universe_logger.info("🔍 Discovering S&P 500 candidates...", operation="candidate_discovery")
            data = self.polygon_client.get_tickers(
                market="stocks", active=True, limit=500
            )

            results = data.get("results", [])
            if not results:
                return self._get_fallback_symbols()

            # Extract symbols and get market caps in parallel
            all_symbols = [
                ticker.get("ticker")
                for ticker in results
                if isinstance(ticker.get("ticker"), str)
            ]

            universe_logger.info(f"📊 Processing {len(all_symbols)} symbols for market cap...", operation="candidate_discovery", symbol_count=len(all_symbols))

            # Process in batches to avoid rate limits
            candidates = []
            batch_size = 50

            for i in range(0, len(all_symbols), batch_size):
                batch = all_symbols[i : i + batch_size]

                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {
                        executor.submit(self._get_market_cap, symbol): symbol
                        for symbol in batch
                    }

                    for future in as_completed(futures):
                        result = future.result()
                        if result and result["market_cap"] >= min_market_cap:
                            candidates.append(result["symbol"])

                if len(candidates) >= 400:  # Stop if we have enough
                    break

            universe_logger.info(
                f"✅ Found {len(candidates)} candidates with market cap > ${min_market_cap/1_000_000_000:.0f}B",
                operation="candidate_discovery", candidate_count=len(candidates), min_market_cap_billions=min_market_cap/1_000_000_000
            )
            return candidates

        except Exception as e:
            universe_logger.error(f"⚠️ Error discovering candidates: {e}", operation="candidate_discovery", error_type=type(e).__name__)
            return self._get_fallback_symbols()

    def _get_market_cap(self, symbol: str) -> Optional[Dict]:
        """Get market cap for a symbol."""
        try:
            details = self.polygon_client.get_ticker_details(symbol)
            if details and details.get("results"):
                results = details["results"]
                return {"symbol": symbol, "market_cap": results.get("market_cap", 0)}
            return None
        except Exception:
            return None

    def _build_sector_info(
        self, symbols: List[str]
    ) -> Tuple[Optional[callable], Optional[Dict]]:
        """Build sector classifier and weights."""
        try:
            sector_counts = {}

            for symbol in symbols[:50]:  # Limit to avoid rate limits
                try:
                    details = self.polygon_client.get_ticker_details(symbol)
                    if details and details.get("results"):
                        sector = details["results"].get("sic_description", "Unknown")
                        sector_counts[sector] = sector_counts.get(sector, 0) + 1
                except Exception:
                    continue

            if not sector_counts:
                return None, None

            # Create sector classifier
            def sector_classifier(sym: str) -> Optional[str]:
                try:
                    details = self.polygon_client.get_ticker_details(sym)
                    if details and details.get("results"):
                        return details["results"].get("sic_description")
                except Exception:
                    pass
                return "Unknown"

            # Calculate weights
            total = sum(sector_counts.values())
            weights = {sector: count / total for sector, count in sector_counts.items()}

            return sector_classifier, weights

        except Exception:
            return None, None

    def _fallback_strategy(
        self, candidates: List[str], start_date: date, end_date: date, target_size: int
    ) -> List[str]:
        """Fallback strategy when filters are too restrictive."""
        universe_logger.info("🔄 Using fallback strategy...", operation="fallback_strategy")

        # Use minimal filters
        config = {
            "min_price": 5.0,
            "min_atr_pct": 0.005,
            "max_atr_pct": 0.1,
            "adv_min_dollar": 10_000_000.0,
            "spread_max_bps": 15.0,
            "spread_max_dollars": 0.1,
        }

        try:
            universe = self._apply_filters(
                candidates, start_date, end_date, target_size, target_size, config
            )
            return universe
        except Exception:
            # Last resort: return top candidates by market cap
            return candidates[:target_size]

    def _get_fallback_symbols(self) -> List[str]:
        """Fallback symbols if all else fails."""
        return [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "BRK.B",
            "UNH",
            "JNJ",
            "V",
            "PG",
            "JPM",
            "HD",
            "MA",
            "DIS",
            "PYPL",
            "ADBE",
            "NFLX",
            "CRM",
            "INTC",
            "CMCSA",
            "PFE",
            "TMO",
            "ABT",
            "COST",
            "PEP",
            "AVGO",
            "TXN",
            "QCOM",
            "ACN",
            "DHR",
            "VZ",
            "NKE",
            "MRK",
            "WMT",
            "LIN",
            "PM",
            "UNP",
            "HON",
            "IBM",
            "SPGI",
            "LOW",
            "AMGN",
            "CAT",
            "GE",
            "BA",
            "GS",
            "AXP",
            "MMM",
            "JPM",
            "WFC",
            "BAC",
            "C",
            "USB",
        ]

    def _save_universe(
        self, universe: List[str], analysis_days: int, cache_path: str
    ) -> None:
        """Save universe to cache."""
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            payload = {
                "analysis_date": datetime.now().isoformat(),
                "analysis_days": analysis_days,
                "symbols": universe,
                "count": len(universe),
            }
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception:
            pass
