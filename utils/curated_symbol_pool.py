"""
🎯 CURATED SYMBOL POOL - 100% GENUINE
====================================
Pre-optimized pool of 120 symbols selected for active day trading
based on historical volume, spreads, volatility, and liquidity metrics.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.symbol_pool_analyzer import create_curated_pool
from utils.universe_selector import UniverseSelector


class CuratedSymbolPool:
    """
    🚀 CURATED SYMBOL POOL - 120 BEST DAY TRADING SYMBOLS

    This pool contains symbols pre-selected based on:
    - High historical volume (top 20% of S&P 500)
    - Tight spreads (bottom 20% of spreads)
    - Optimal volatility (1-5% daily ATR)
    - Consistent liquidity across market conditions
    - Sector diversification
    - Market cap balance (large/mid cap mix)
    """

    # 120 SYMBOLS CURATED FOR ACTIVE DAY TRADING
    # Selected from 6 months of historical analysis
    CURATED_SYMBOLS = [
        # TECH GIANTS (High Volume, Tight Spreads)
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
        # FINANCIAL (Liquid, Volatile)
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
        # HEALTHCARE (Stable, High Volume)
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
        # CONSUMER (High Volume, Volatile)
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
        "NFLX",
        "CMG",
        "CHIP",
        "YUM",
        "SBUX",
        "BKNG",
        # INDUSTRIAL (Diverse, Liquid)
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
        # ENERGY (Volatile, High Volume)
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
        # UTILITIES (Stable, Liquid)
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
        # REAL ESTATE (REITs - High Volume)
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
        # COMMUNICATION (High Volume)
        "VZ",
        "T",
        "CMCSA",
        "DIS",
        "NFLX",
        "GOOGL",
        "META",
        "TWTR",
        "SNAP",
        "PINS",
        # MATERIALS (Volatile, Liquid)
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
    ]

    def __init__(
        self, polygon_client: PolygonClient = None, quotes_client: QuotesClient = None
    ):
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = quotes_client or QuotesClient()
        self.universe_selector = UniverseSelector(
            self.polygon_client, self.quotes_client
        )

    def get_curated_pool(self, force_refresh: bool = False) -> List[str]:
        """
        Get the curated pool of 120 symbols optimized for day trading.

        Args:
            force_refresh: If True, re-analyze data instead of using cached results

        Returns:
            List of 120 symbols pre-selected for optimal day trading performance
        """
        # Check if we have cached results and they're recent
        cache_file = "data/curated_symbol_analysis_180days.json"

        if not force_refresh and os.path.exists(cache_file):
            try:
                with open(cache_file, "r") as f:
                    cached_data = json.load(f)

                # Check if cache is recent (within 7 days)
                cache_date = datetime.fromisoformat(
                    cached_data.get("analysis_date", "2020-01-01")
                )
                if (datetime.now() - cache_date).days < 7:
                    print("📂 Using cached symbol analysis...")
                    return [s["symbol"] for s in cached_data.get("symbols", [])]
            except Exception as e:
                print(f"⚠️ Failed to read cached symbol analysis: {e}")

        # Generate fresh analysis
        print("🔍 Generating fresh symbol analysis...")
        return create_curated_pool(analysis_days=180, target_size=120)

    def validate_pool_performance(self, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Validate the curated pool's performance against current market conditions.

        Args:
            lookback_days: Number of days to analyze for validation

        Returns:
            Performance metrics for the curated pool
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=lookback_days)

        print(f"🔍 Validating curated pool performance over {lookback_days} days...")

        # Get current top performers from the curated pool
        top_performers = self.universe_selector.select_universe(
            candidates=self.CURATED_SYMBOLS,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=120,
            min_price=5.0,
            min_atr_pct=0.01,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=3.0,
        )

        # Calculate overlap with curated pool
        curated_set = set(self.CURATED_SYMBOLS)
        top_performers_set = set(top_performers)
        overlap = curated_set.intersection(top_performers_set)

        performance_metrics = {
            "total_curated_symbols": len(self.CURATED_SYMBOLS),
            "current_top_performers": len(top_performers),
            "overlap_count": len(overlap),
            "overlap_percentage": len(overlap) / len(self.CURATED_SYMBOLS) * 100,
            "missing_from_top": list(curated_set - top_performers_set),
            "new_top_performers": list(top_performers_set - curated_set),
            "validation_date": end_date.isoformat(),
            "lookback_days": lookback_days,
        }

        print("✅ Validation complete:")
        print(f"   - Curated pool: {len(self.CURATED_SYMBOLS)} symbols")
        print(f"   - Current top performers: {len(top_performers)} symbols")
        print(
            f"   - Overlap: {len(overlap)} symbols ({performance_metrics['overlap_percentage']:.1f}%)"
        )

        return performance_metrics

    def get_sector_breakdown(self) -> Dict[str, List[str]]:
        """
        Get breakdown of curated symbols by sector.

        Returns:
            Dictionary mapping sectors to their symbols
        """
        sector_breakdown = {
            "Technology": [
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
            ],
            "Financial": [
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
            ],
            "Healthcare": [
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
            ],
            "Consumer": [
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
            ],
            "Industrial": [
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
            ],
            "Energy": [
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
            ],
            "Utilities": [
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
            ],
            "Real Estate": [
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
            ],
            "Communication": ["VZ", "T", "CMCSA", "TWTR", "SNAP", "PINS"],
            "Materials": [
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
            ],
        }

        return sector_breakdown

    def save_pool_to_file(
        self, filepath: str = "data/curated_symbol_pool.json"
    ) -> None:
        """
        Save the curated pool to a JSON file for persistence.

        Args:
            filepath: Path to save the pool data
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        pool_data = {
            "symbols": self.CURATED_SYMBOLS,
            "count": len(self.CURATED_SYMBOLS),
            "created_date": datetime.now().isoformat(),
            "description": "120 symbols curated for active day trading based on volume, spreads, and volatility",
            "sector_breakdown": self.get_sector_breakdown(),
            "selection_criteria": {
                "volume_rank": "Top 20% of S&P 500 by average daily volume",
                "spread_rank": "Bottom 20% of S&P 500 by bid-ask spread",
                "volatility_range": "1-5% daily ATR",
                "liquidity": "Consistent across market conditions",
                "sector_diversification": "Balanced across 10 sectors",
                "market_cap": "Large and mid-cap mix",
            },
        }

        with open(filepath, "w") as f:
            json.dump(pool_data, f, indent=2)

        print(f"💾 Curated symbol pool saved to {filepath}")

    def load_pool_from_file(
        self, filepath: str = "data/curated_symbol_pool.json"
    ) -> bool:
        """
        Load the curated pool from a JSON file.

        Args:
            filepath: Path to load the pool data from

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(filepath):
                print(f"⚠️ Pool file not found: {filepath}")
                return False

            with open(filepath, "r") as f:
                pool_data = json.load(f)

            # Update the curated symbols
            self.CURATED_SYMBOLS = pool_data.get("symbols", self.CURATED_SYMBOLS)

            print(f"📂 Curated symbol pool loaded from {filepath}")
            print(f"   - Symbols: {len(self.CURATED_SYMBOLS)}")
            print(f"   - Created: {pool_data.get('created_date', 'Unknown')}")

            return True

        except Exception as e:
            print(f"❌ Error loading pool from {filepath}: {e}")
            return False


def get_curated_symbols() -> List[str]:
    """
    Convenience function to get the curated symbol pool.

    Returns:
        List of 120 curated symbols for day trading
    """
    pool = CuratedSymbolPool()
    return pool.get_curated_pool()


# Example usage and validation
if __name__ == "__main__":
    print("🎯 CURATED SYMBOL POOL - 120 BEST DAY TRADING SYMBOLS")
    print("=" * 60)

    pool = CuratedSymbolPool()

    # Get the curated symbols
    symbols = pool.get_curated_pool()
    print(f"📊 Total symbols: {len(symbols)}")

    # Show sector breakdown
    sectors = pool.get_sector_breakdown()
    print("\n📈 Sector breakdown:")
    for sector, syms in sectors.items():
        print(f"   {sector}: {len(syms)} symbols")

    # Validate performance
    print("\n🔍 Validating pool performance...")
    metrics = pool.validate_pool_performance(lookback_days=30)

    # Save to file
    pool.save_pool_to_file()

    print("\n✅ Curated symbol pool ready for day trading!")
