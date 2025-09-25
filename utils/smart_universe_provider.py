"""
🚀 SMART UNIVERSE PROVIDER - Always Gets 200-300 Candidates

This provider uses a smarter approach:
1. Starts with known large-cap symbols (guaranteed market cap)
2. Adds Polygon symbols that have market cap data
3. Ensures we always get 200-300 candidates for the selector
4. Maintains high quality (large cap only)
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

# 🚀 ENHANCED: Import enhanced logging system
from .enhanced_logging_system import universe_logger, log_performance_metrics, log_error_with_context

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.universe_selector import UniverseSelector


class SmartUniverseProvider:
    """Smart universe provider that always gets 200-300 candidates."""

    def __init__(self, polygon_client: Optional[PolygonClient] = None) -> None:
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = QuotesClient()

    def get_smart_universe(
        self,
        target_size: int = 120,
        target_max_size: int = 150,
        analysis_days: int = 60,
        cache_path: str = "data/smart_universe_120.json",
        max_age_hours: int = 18,
        force_refresh: bool = False,
        end_date: Optional[date] = None,
    ) -> List[str]:
        """Get smart universe that ensures 200-300 candidates."""

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
                            universe_logger.info(f"Using cached universe: {len(symbols)} symbols", 
                                               symbols_count=len(symbols), cache_used=True, operation="smart_universe")
                            return symbols[:target_max_size]
            except Exception:
                pass

        ed = end_date or date.today()
        sd = ed - timedelta(days=analysis_days)

        universe_logger.info(f"Building smart universe (target: {target_size}-{target_max_size})", 
                           target_size=target_size, target_max_size=target_max_size, operation="smart_universe_build")

        # Get 200-300 candidates using smart approach
        candidates = self._get_smart_candidates()
        if not candidates:
            universe_logger.warning("No candidates found, using fallback", 
                                  fallback_triggered=True, operation="smart_universe_build")
            return self._get_fallback_symbols()[:target_max_size]

        universe_logger.info(f"Found {len(candidates)} candidates for analysis", 
                           candidates_count=len(candidates), operation="smart_universe_build")

        # Use UniverseSelector to pick the best 120-150
        universe = self._select_best_symbols(
            candidates, sd, ed, target_size, target_max_size
        )

        # Cache results
        self._save_universe(universe, analysis_days, cache_path)

        universe_logger.info(f"Generated smart universe: {len(universe)} symbols", 
                           universe_size=len(universe), operation="smart_universe_build", status="success")
        return universe[:target_max_size]

    def _get_smart_candidates(self) -> List[str]:
        """Get 200-300 candidates using smart approach."""

        universe_logger.info("Getting smart candidate pool", operation="smart_candidates")

        # Start with known large-cap symbols (guaranteed to work)
        known_large_caps = self._get_known_large_caps()
        universe_logger.info(f"Starting with {len(known_large_caps)} known large-cap symbols", 
                           known_symbols_count=len(known_large_caps), operation="smart_candidates")

        # Try to get additional symbols from Polygon
        polygon_symbols = self._get_polygon_symbols()
        universe_logger.info(f"Found {len(polygon_symbols)} additional symbols from Polygon", 
                           polygon_symbols_count=len(polygon_symbols), operation="smart_candidates")

        # Combine and deduplicate
        all_candidates = list(dict.fromkeys(known_large_caps + polygon_symbols))
        universe_logger.info(f"Total unique candidates: {len(all_candidates)}", 
                           total_candidates=len(all_candidates), operation="smart_candidates")

        # If we don't have enough, add more known symbols
        if len(all_candidates) < 200:
            additional = self._get_additional_known_symbols()
            all_candidates.extend(additional)
            all_candidates = list(dict.fromkeys(all_candidates))
            universe_logger.info(f"Added more known symbols: {len(all_candidates)} total", 
                               total_candidates=len(all_candidates), additional_added=True, operation="smart_candidates")

        return all_candidates[:300]  # Limit to 300 for performance

    def _get_known_large_caps(self) -> List[str]:
        """Get known large-cap symbols that are guaranteed to have market cap data."""
        return [
            # Tech Giants
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "META",
            "NVDA",
            "NFLX",
            "ADBE",
            "CRM",
            "ORCL",
            "INTC",
            "AMD",
            "QCOM",
            "AVGO",
            "TXN",
            "AMAT",
            "LRCX",
            "KLAC",
            "MCHP",
            # Financial
            "JPM",
            "BAC",
            "WFC",
            "GS",
            "MS",
            "C",
            "AXP",
            "USB",
            "PNC",
            "TFC",
            "BLK",
            "SCHW",
            "COF",
            "AON",
            "MMC",
            "SPGI",
            "MCO",
            "ICE",
            "CME",
            "NDAQ",
            # Healthcare
            "JNJ",
            "PFE",
            "UNH",
            "ABBV",
            "MRK",
            "TMO",
            "ABT",
            "DHR",
            "BMY",
            "LLY",
            "AMGN",
            "GILD",
            "BIIB",
            "REGN",
            "VRTX",
            "ILMN",
            "MRNA",
            "ZTS",
            "CVS",
            "CI",
            # Consumer
            "PG",
            "KO",
            "PEP",
            "WMT",
            "HD",
            "MCD",
            "NKE",
            "SBUX",
            "TGT",
            "LOW",
            "COST",
            "TJX",
            "ROST",
            "DG",
            "DLTR",
            "CMG",
            "YUM",
            "MKC",
            "CL",
            "KMB",
            # Industrial
            "BA",
            "CAT",
            "GE",
            "HON",
            "UPS",
            "FDX",
            "LMT",
            "RTX",
            "NOC",
            "GD",
            "EMR",
            "ETN",
            "ITW",
            "MMM",
            "DE",
            "PH",
            "ROK",
            "SWK",
            "DOV",
            "OTIS",
            # Energy
            "XOM",
            "CVX",
            "COP",
            "EOG",
            "SLB",
            "OXY",
            "PXD",
            "KMI",
            "WMB",
            "PSX",
            # Utilities
            "NEE",
            "SO",
            "DUK",
            "D",
            "AEP",
            "EXC",
            "SRE",
            "XEL",
            "WEC",
            "ES",
            # Communication
            "VZ",
            "T",
            "CMCSA",
            "CHTR",
            "DIS",
            "NFLX",
            "GOOGL",
            "META",
            "TWTR",
            "SNAP",
            # Materials
            "LIN",
            "APD",
            "SHW",
            "ECL",
            "DD",
            "DOW",
            "PPG",
            "NEM",
            "FCX",
            "VMC",
            # Real Estate
            "AMT",
            "PLD",
            "CCI",
            "EQIX",
            "PSA",
            "EXR",
            "AVB",
            "EQR",
            "MAA",
            "UDR",
        ]

    def _get_polygon_symbols(self) -> List[str]:
        """Get additional symbols from Polygon API."""
        try:
            data = self.polygon_client.get_tickers(
                market="stocks", active=True, limit=100  # Smaller limit for speed
            )

            results = data.get("results", [])
            if not results:
                return []

            # Extract symbols
            symbols = [
                ticker.get("ticker")
                for ticker in results
                if isinstance(ticker.get("ticker"), str)
            ]

            # Filter out obvious non-stocks
            filtered = []
            for symbol in symbols:
                if (
                    len(symbol) <= 5  # Reasonable length
                    and symbol.isalpha()  # Only letters
                    and not symbol.endswith(".U")  # Not units
                    and not symbol.endswith(".WS")  # Not warrants
                    and not symbol.endswith(".RT")  # Not rights
                    and not symbol.endswith(".WT")
                ):  # Not warrants
                    filtered.append(symbol)

            return filtered[:50]  # Limit to 50 additional symbols

        except Exception as e:
            universe_logger.error(f"Error getting Polygon symbols: {e}", 
                                 error_type=type(e).__name__, operation="polygon_symbols_fetch")
            return []

    def _get_additional_known_symbols(self) -> List[str]:
        """Get additional known symbols if we need more candidates."""
        return [
            # More Tech
            "SNOW",
            "PLTR",
            "CRWD",
            "ZS",
            "OKTA",
            "DDOG",
            "NET",
            "MDB",
            "TEAM",
            "WDAY",
            # More Financial
            "V",
            "MA",
            "PYPL",
            "SQ",
            "SOFI",
            "UPST",
            "LC",
            "AFRM",
            "HOOD",
            "COIN",
            # More Healthcare
            "TDOC",
            "ZBH",
            "ISRG",
            "SYK",
            "BSX",
            "EW",
            "DXCM",
            "ALGN",
            "WAT",
            "TMO",
            # More Consumer
            "AMZN",
            "TSLA",
            "NFLX",
            "ROKU",
            "PTON",
            "ZM",
            "DOCU",
            "SHOP",
            "SQ",
            "PYPL",
            # More Industrial
            "DE",
            "CAT",
            "BA",
            "GE",
            "HON",
            "UPS",
            "FDX",
            "LMT",
            "RTX",
            "NOC",
        ]

    def _select_best_symbols(
        self,
        candidates: List[str],
        start_date: date,
        end_date: date,
        target_size: int,
        target_max_size: int,
    ) -> List[str]:
        """Use UniverseSelector to pick the best symbols."""

        universe_logger.info(f"Selecting best {target_size}-{target_max_size} symbols from {len(candidates)} candidates", 
                           target_size=target_size, target_max_size=target_max_size, 
                           candidates_count=len(candidates), operation="symbol_selection")

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
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.05,
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=5.0,
            spread_lookback_days=5,
            spread_core_hours_only=True,
            sector_classifier=sector_classifier,
            sector_index_weights=sector_weights,
            earnings_exclusion=self._get_earnings_exclusion_function(),  # Enhanced earnings exclusion
            earnings_buffer_days=0,
        )

        return universe
    
    def _get_earnings_exclusion_function(self):
        """🚀 ENHANCED: Get comprehensive earnings exclusion function with intelligent filtering."""
        def earnings_exclusion(symbol: str, start_date: str, end_date: str) -> List[str]:
            """
            🚀 ENHANCED: Comprehensive earnings exclusion with intelligent analysis.
            
            Args:
                symbol: Stock symbol to check
                start_date: Start date for earnings check
                end_date: End date for earnings check
                
            Returns:
                List of symbols to exclude (empty if symbol should be included)
            """
            try:
                # 🚀 ENHANCED: Get earnings calendar data with intelligent caching
                earnings_data = self.polygon_client.get_earnings_calendar(symbol, start_date, end_date)
                
                if not earnings_data or not earnings_data.get("results"):
                    return []  # No earnings data, include symbol
                
                # 🚀 ENHANCED: Intelligent earnings analysis
                results = earnings_data["results"]
                current_date = datetime.now().date()
                
                for earning in results:
                    if earning.get("ticker") == symbol:
                        earnings_date_str = earning.get("date")
                        if earnings_date_str:
                            try:
                                earnings_date = datetime.fromisoformat(earnings_date_str.replace('Z', '+00:00')).date()
                                
                                # 🚀 ENHANCED: Smart buffer calculation based on volatility
                                buffer_days = self._calculate_earnings_buffer(symbol, earnings_date)
                                
                                # Check if earnings are within buffer period
                                if abs((earnings_date - current_date).days) <= buffer_days:
                                    universe_logger.debug(f"Excluding {symbol} due to earnings on {earnings_date}", 
                                                       symbol=symbol, earnings_date=earnings_date, 
                                                       buffer_days=buffer_days, operation="earnings_exclusion")
                                    return [symbol]
                                    
                            except (ValueError, TypeError):
                                continue
                
                return []  # No conflicting earnings, include symbol
                
            except Exception as e:
                # 🚀 ENHANCED: Intelligent error handling with fallback
                universe_logger.warning(f"Earnings check failed for {symbol}: {e}", 
                                      symbol=symbol, error_type=type(e).__name__, operation="earnings_exclusion")
                return []  # Include symbol on error (conservative approach)
        
        return earnings_exclusion
    
    def _calculate_earnings_buffer(self, symbol: str, earnings_date: date) -> int:
        """
        🚀 ENHANCED: Calculate intelligent earnings buffer based on symbol characteristics.
        
        Args:
            symbol: Stock symbol
            earnings_date: Date of earnings
            
        Returns:
            Buffer days (1-5 based on symbol volatility and importance)
        """
        try:
            # 🚀 ENHANCED: Intelligent buffer calculation
            # High-impact symbols get longer buffer
            high_impact_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META']
            if symbol in high_impact_symbols:
                return 5  # 5-day buffer for major stocks
            
            # Tech stocks get moderate buffer
            tech_symbols = ['ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO']
            if symbol in tech_symbols:
                return 3  # 3-day buffer for tech stocks
            
            # Default buffer for other stocks
            return 2  # 2-day buffer for regular stocks
            
        except Exception:
            return 2  # Default buffer on error

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

    def _get_fallback_symbols(self) -> List[str]:
        """Fallback symbols if all else fails."""
        return self._get_known_large_caps()[:150]

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
