"""
🎯 OPTIMIZED SYMBOL POOL - 100% GENUINE DATA-DRIVEN
==================================================
Uses existing UniverseSelector with Polygon data to find the best 120 symbols
for active day trading based on REAL historical performance.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from services.sp500_client import SP500Client
from utils.universe_selector import UniverseSelector

# 🚀 ENHANCED: Import enhanced logging system
from utils.enhanced_logging_system import get_enhanced_logger, log_performance_metrics, log_error_with_context

# 🚀 ENHANCED: Initialize enhanced logger for optimized symbol pool
pool_logger = get_enhanced_logger('optimized_symbol_pool', 'logs/optimized_pool.log')


class OptimizedSymbolPool:
    """
    🚀 OPTIMIZED SYMBOL POOL - 120 BEST DAY TRADING SYMBOLS

    Uses the proven UniverseSelector to analyze REAL Polygon data and select
    the best 120 symbols based on:
    - High volume (top performers)
    - Tight spreads (bottom 20%)
    - Optimal volatility (1-5% ATR)
    - Consistent liquidity
    """

    def __init__(
        self, polygon_client: PolygonClient = None, quotes_client: QuotesClient = None
    ):
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = quotes_client or QuotesClient()
        self.universe_selector = UniverseSelector(
            self.polygon_client, self.quotes_client
        )
        self.sp500_client = SP500Client()

    def get_optimized_pool(
        self,
        analysis_days: int = 180,
        target_size: int = 120,
        force_refresh: bool = False,
    ) -> List[str]:
        """
        Get the optimized pool of symbols using REAL Polygon data analysis.

        Args:
            analysis_days: Days of historical data to analyze
            target_size: Target number of symbols (default 120)
            force_refresh: Force fresh analysis instead of using cache

        Returns:
            List of optimized symbols for day trading
        """
        # Check for cached results
        cache_file = f"data/optimized_symbol_pool_{analysis_days}days.json"

        if not force_refresh and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)

                # Check if cache is recent (within 7 days)
                cache_date = datetime.fromisoformat(
                    cached_data.get("analysis_date", "2020-01-01")
                )
                if (datetime.now() - cache_date).days < 7:
                    pool_logger.info("Using cached optimized symbol pool", 
                                   cache_used=True, operation="pool_creation")
                    return cached_data.get("symbols", [])
            except Exception as e:
                pool_logger.warning(f"Failed to read optimized symbol pool cache: {e}", 
                                  error_type=type(e).__name__, operation="cache_operations")

        pool_logger.info(f"Analyzing symbols with {analysis_days} days of REAL Polygon data", 
                        analysis_days=analysis_days, operation="pool_creation")

        # Get candidate symbols (S&P 500 or fallback)
        candidates = self._get_candidate_symbols()

        if not candidates:
            pool_logger.error("No candidate symbols available", 
                            operation="pool_creation", status="error")
            return []

        pool_logger.info(f"Analyzing {len(candidates)} candidate symbols", 
                        candidates_count=len(candidates), operation="pool_creation")

        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=analysis_days)

        # Use UniverseSelector to find the best symbols
        optimized_symbols = self.universe_selector.select_universe(
            candidates=candidates,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=target_size,
            min_price=5.0,  # Minimum $5 price
            min_atr_pct=0.01,  # Minimum 1% ATR
            spread_filter_enabled=True,
            spread_max_dollars=0.02,  # Max $0.02 spread
            spread_max_bps=3.0,  # Max 3 bps spread
            spread_lookback_days=5,
            spread_core_hours_only=True,
        )

        pool_logger.info(f"Selected {len(optimized_symbols)} optimized symbols!", 
                        selected_count=len(optimized_symbols), status="success", operation="pool_creation")

        # Save results to cache
        self._save_optimized_pool(optimized_symbols, analysis_days, cache_file)

        return optimized_symbols

    def _get_candidate_symbols(self) -> List[str]:
        """Get candidate symbols for analysis"""
        # Try to get S&P 500 symbols
        try:
            sp500_symbols = self.sp500_client.fetch_symbols()
            if sp500_symbols:
                pool_logger.info(f"Using {len(sp500_symbols)} S&P 500 symbols as candidates", 
                               sp500_count=len(sp500_symbols), operation="candidate_discovery")
                return sp500_symbols
        except Exception as e:
            pool_logger.warning(f"S&P 500 fetch failed: {e}", 
                              error_type=type(e).__name__, operation="candidate_discovery")

        # Fallback to known high-volume S&P 500 symbols
        pool_logger.warning("Using fallback high-volume S&P 500 symbols", 
                          fallback_triggered=True, operation="candidate_discovery")
        return [
            # Tech Giants
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "NVDA",
            "TSLA",
            "META",
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
            "V",
            "MA",
            "PYPL",
            "COF",
            "USB",
            "PNC",
            "TFC",
            "BK",
            "SCHW",
            "BLK",
            "SPGI",
            "ICE",
            "CME",
            # Healthcare
            "JNJ",
            "UNH",
            "PFE",
            "ABT",
            "TMO",
            "DHR",
            "BMY",
            "LLY",
            "MRK",
            "AMGN",
            "GILD",
            "BIIB",
            "VRTX",
            "REGN",
            "ISRG",
            "SYK",
            "BDX",
            "EW",
            "A",
            "CI",
            # Consumer
            "WMT",
            "PG",
            "HD",
            "DIS",
            "NKE",
            "MCD",
            "SBUX",
            "TGT",
            "LOW",
            "COST",
            "TJX",
            "ROST",
            "ULTA",
            "LULU",
            "CMG",
            "CHIP",
            "YUM",
            "BKNG",
            # Industrial
            "BA",
            "CAT",
            "MMM",
            "GE",
            "HON",
            "UPS",
            "RTX",
            "LMT",
            "NOC",
            "GD",
            "EMR",
            "ETN",
            "ITW",
            "PH",
            "DE",
            "CMI",
            "FDX",
            "CSX",
            "NSC",
            "UNP",
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
            "DUK",
            "SO",
            "D",
            "EXC",
            "AEP",
            "XEL",
            "SRE",
            "PEG",
            "WEC",
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
            # Communication
            "VZ",
            "T",
            "CMCSA",
            "TWTR",
            "SNAP",
            "PINS",
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
            "VALE",
            # Additional high-volume stocks
            "BRK.B",
            "ACN",
            "TMO",
            "ABBV",
            "PEP",
            "COST",
            "AVGO",
            "QCOM",
            "COF",
            "DHR",
            "ACN",
            "TXN",
            "CMCSA",
            "LIN",
            "NEE",
            "HON",
            "UNP",
            "LOW",
            "UPS",
            "IBM",
            "AMGN",
            "T",
            "SPGI",
            "INTU",
            "CAT",
            "MMM",
            "BA",
            "GE",
            "HON",
            "UPS",
            "RTX",
            "LMT",
            "NOC",
            "GD",
            "EMR",
            "ETN",
            "ITW",
            "PH",
            "DE",
            "CMI",
            "FDX",
            "CSX",
            "NSC",
            "UNP",
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
            "NEE",
            "DUK",
            "SO",
            "D",
            "EXC",
            "AEP",
            "XEL",
            "SRE",
            "PEG",
            "WEC",
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
            "VZ",
            "T",
            "CMCSA",
            "TWTR",
            "SNAP",
            "PINS",
            "LIN",
            "APD",
            "SHW",
            "ECL",
            "DD",
            "DOW",
            "PPG",
            "NEM",
            "FCX",
            "VALE",
            "BRK.B",
            "ACN",
            "TMO",
            "ABBV",
            "PEP",
            "COST",
            "AVGO",
            "QCOM",
        ]

    def _save_optimized_pool(
        self, symbols: List[str], analysis_days: int, filepath: str
    ) -> None:
        """Save the optimized pool to cache"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        pool_data = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "symbols": symbols,
            "count": len(symbols),
            "description": f"Optimized {len(symbols)} symbols for day trading based on {analysis_days} days of Polygon data",
            "criteria": {
                "min_price": 5.0,
                "min_atr_pct": 0.01,
                "max_spread_dollars": 0.02,
                "max_spread_bps": 3.0,
                "ranking": "Average daily dollar volume",
            },
        }

        with open(filepath, "w") as f:
            json.dump(pool_data, f, indent=2)

        pool_logger.info(f"Optimized pool saved to {filepath}", 
                        filepath=filepath, operation="file_operations")

    def validate_pool_performance(self, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Validate the optimized pool's current performance.

        Args:
            lookback_days: Days to analyze for validation

        Returns:
            Performance validation metrics
        """
        pool_logger.info(f"Validating pool performance over {lookback_days} days", 
                        lookback_days=lookback_days, operation="validation")

        # Get current optimized pool
        current_pool = self.get_optimized_pool(analysis_days=180, target_size=120)

        # Get fresh analysis of current pool
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)

        fresh_analysis = self.universe_selector.select_universe(
            candidates=current_pool,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=120,
            min_price=5.0,
            min_atr_pct=0.01,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=3.0,
        )

        # Calculate overlap
        current_set = set(current_pool)
        fresh_set = set(fresh_analysis)
        overlap = current_set.intersection(fresh_set)

        validation_metrics = {
            "current_pool_size": len(current_pool),
            "fresh_analysis_size": len(fresh_analysis),
            "overlap_count": len(overlap),
            "overlap_percentage": len(overlap) / len(current_pool) * 100,
            "validation_date": end_date.isoformat(),
            "lookback_days": lookback_days,
            "pool_stability": (
                "HIGH"
                if len(overlap) / len(current_pool) > 0.8
                else "MEDIUM" if len(overlap) / len(current_pool) > 0.6 else "LOW"
            ),
        }

        pool_logger.info("Validation complete:", status="success", operation="validation")
        pool_logger.info(f"Pool stability: {validation_metrics['pool_stability']}", 
                        pool_stability=validation_metrics['pool_stability'], operation="validation")
        pool_logger.info(f"Overlap: {len(overlap)}/{len(current_pool)} symbols ({validation_metrics['overlap_percentage']:.1f}%)", 
                        overlap_count=len(overlap), total_count=len(current_pool), 
                        overlap_percentage=validation_metrics['overlap_percentage'], operation="validation")

        return validation_metrics


def get_optimized_symbols(
    analysis_days: int = 180, target_size: int = 120
) -> List[str]:
    """
    Convenience function to get optimized symbols.

    Args:
        analysis_days: Days of historical data to analyze
        target_size: Target number of symbols

    Returns:
        List of optimized symbols for day trading
    """
    pool = OptimizedSymbolPool()
    return pool.get_optimized_pool(analysis_days, target_size)


# Example usage
if __name__ == "__main__":
    pool_logger.info("OPTIMIZED SYMBOL POOL - 100% GENUINE DATA-DRIVEN", operation="main")
    pool_logger.info("=" * 60, operation="main")

    # Create optimized pool
    pool = OptimizedSymbolPool()

    # Get optimized symbols
    symbols = pool.get_optimized_pool(analysis_days=180, target_size=120)

    pool_logger.info(f"Optimized pool created with {len(symbols)} symbols!", 
                    pool_size=len(symbols), status="success", operation="main")
    pool_logger.info(f"Top 10 symbols: {symbols[:10]}", 
                    top_symbols=symbols[:10], operation="main")

    # Validate performance
    validation = pool.validate_pool_performance(lookback_days=30)

    pool_logger.info("Ready for day trading with REAL Polygon data!", 
                    status="ready", operation="main")
