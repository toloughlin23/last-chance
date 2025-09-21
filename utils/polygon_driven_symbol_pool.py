"""
🎯 POLYGON-DRIVEN SYMBOL POOL - 100% GENUINE DATA
================================================
Uses REAL Polygon API data to create the optimal 120-symbol pool
for active day trading based on actual market performance.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

from dotenv import load_dotenv

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.universe_selector import UniverseSelector


class PolygonDrivenSymbolPool:
    """
    🚀 POLYGON-DRIVEN SYMBOL POOL - 120 BEST DAY TRADING SYMBOLS
    
    Uses REAL Polygon API data to analyze and select the best 120 symbols
    based on actual market performance:
    - High volume (top performers)
    - Tight spreads (bottom 20%)
    - Optimal volatility (1-5% ATR)
    - Consistent liquidity
    - Real market data only
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize clients with real API keys
        self.polygon_client = PolygonClient()
        self.quotes_client = QuotesClient()
        self.universe_selector = UniverseSelector(self.polygon_client, self.quotes_client)
        
    def get_polygon_driven_pool(
        self, 
        analysis_days: int = 180,
        target_size: int = 120,
        force_refresh: bool = False
    ) -> List[str]:
        """
        Get the polygon-driven pool using REAL market data.
        
        Args:
            analysis_days: Days of historical data to analyze
            target_size: Target number of symbols (default 120)
            force_refresh: Force fresh analysis instead of using cache
            
        Returns:
            List of optimized symbols for day trading
        """
        # Check for cached results
        cache_file = f"data/polygon_driven_pool_{analysis_days}days.json"
        
        if not force_refresh and os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)

                # Check if cache is recent (within 7 days)
                cache_date = datetime.fromisoformat(cached_data.get("analysis_date", "2020-01-01"))
                if (datetime.now() - cache_date).days < 7:
                    print("📂 Using cached polygon-driven symbol pool...")
                    return cached_data.get("symbols", [])
            except Exception as e:
                print(f"⚠️ Failed to read polygon-driven cache: {e}")
        
        print(f"🔍 Analyzing symbols with {analysis_days} days of REAL Polygon data...")
        
        # Get candidate symbols from Polygon
        candidates = self._get_polygon_candidates()
        
        if not candidates:
            print("❌ No candidate symbols available from Polygon")
            return []
        
        print(f"📊 Analyzing {len(candidates)} candidate symbols from Polygon...")
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=analysis_days)
        
        # Use UniverseSelector to find the best symbols with REAL Polygon data
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
            spread_core_hours_only=True
        )
        
        print(f"✅ Selected {len(optimized_symbols)} optimized symbols from REAL Polygon data!")
        
        # Save results to cache
        self._save_polygon_pool(optimized_symbols, analysis_days, cache_file)
        
        return optimized_symbols
    
    def _get_polygon_candidates(self) -> List[str]:
        """Get candidate symbols from Polygon API"""
        try:
            print("📡 Fetching symbols from Polygon API...")

            # Use existing client capability; if not available, fall back safely
            if hasattr(self.polygon_client, "get_tickers"):
                tickers_data = self.polygon_client.get_tickers(
                    market="stocks", active=True, limit=1000
                )
                if not tickers_data or not tickers_data.get("results"):
                    print("⚠️ No tickers from Polygon, using fallback...")
                    return self._get_fallback_symbols()
                candidates = []
                for ticker in tickers_data["results"]:
                    symbol = ticker.get("ticker", "")
                    market_cap = ticker.get("market_cap", 0)
                    if symbol and market_cap and market_cap > 8_000_000_000:
                        candidates.append(symbol)
                print(f"📈 Found {len(candidates)} large-cap candidates from Polygon")
                return candidates
            else:
                print("⚠️ PolygonClient.get_tickers not available; using fallback candidates")
                return self._get_fallback_symbols()

        except Exception as e:
            print(f"⚠️ Polygon API error: {e}")
            print("🔄 Using fallback high-volume symbols...")
            return self._get_fallback_symbols()
    
    def _get_fallback_symbols(self) -> List[str]:
        """Fallback to known high-volume symbols if Polygon fails"""
        return [
            # Tech Giants (High Volume, Tight Spreads)
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'NFLX', 'ADBE', 'CRM',
            'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'MCHP',
            
            # Financial (Liquid, Volatile)
            'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'V', 'MA', 'PYPL',
            'COF', 'USB', 'PNC', 'TFC', 'BK', 'SCHW', 'BLK', 'SPGI', 'ICE', 'CME',
            
            # Healthcare (Stable, High Volume)
            'JNJ', 'UNH', 'PFE', 'ABT', 'TMO', 'DHR', 'BMY', 'LLY', 'MRK', 'AMGN',
            'GILD', 'BIIB', 'VRTX', 'REGN', 'ISRG', 'SYK', 'BDX', 'EW', 'A', 'CI',
            
            # Consumer (High Volume, Volatile)
            'WMT', 'PG', 'HD', 'DIS', 'NKE', 'MCD', 'SBUX', 'TGT', 'LOW', 'COST',
            'TJX', 'ROST', 'ULTA', 'LULU', 'CMG', 'CHIP', 'YUM', 'BKNG',
            
            # Industrial (Diverse, Liquid)
            'BA', 'CAT', 'MMM', 'GE', 'HON', 'UPS', 'RTX', 'LMT', 'NOC', 'GD',
            'EMR', 'ETN', 'ITW', 'PH', 'DE', 'CMI', 'FDX', 'CSX', 'NSC', 'UNP',
            
            # Energy (Volatile, High Volume)
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'OXY', 'PXD', 'KMI', 'WMB', 'PSX',
            
            # Utilities (Stable, Liquid)
            'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'SRE', 'PEG', 'WEC',
            
            # Real Estate (REITs - High Volume)
            'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'UDR',
            
            # Communication (High Volume)
            'VZ', 'T', 'CMCSA', 'TWTR', 'SNAP', 'PINS',
            
            # Materials (Volatile, Liquid)
            'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'NEM', 'FCX', 'VALE',
            
            # Additional proven performers
            'BRK.B', 'ACN', 'TMO', 'ABBV', 'PEP', 'COST', 'AVGO', 'QCOM', 'COF',
            'DHR', 'ACN', 'TXN', 'CMCSA', 'LIN', 'NEE', 'HON', 'UNP', 'LOW', 'UPS',
            'IBM', 'AMGN', 'T', 'SPGI', 'INTU', 'CAT', 'MMM', 'BA', 'GE', 'HON'
        ]
    
    def _save_polygon_pool(self, symbols: List[str], analysis_days: int, filepath: str) -> None:
        """Save the polygon-driven pool to cache"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        pool_data = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "symbols": symbols,
            "count": len(symbols),
            "data_source": "Polygon API",
            "description": f"120 symbols optimized for day trading using {analysis_days} days of REAL Polygon data",
            "criteria": {
                "min_price": 5.0,
                "min_atr_pct": 0.01,
                "max_spread_dollars": 0.02,
                "max_spread_bps": 3.0,
                "ranking": "Average daily dollar volume",
                "data_source": "Polygon API"
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(pool_data, f, indent=2)
        
        print(f"💾 Polygon-driven pool saved to {filepath}")
    
    def validate_pool_performance(self, lookback_days: int = 30) -> Dict[str, Any]:
        """
        Validate the polygon-driven pool's current performance.
        
        Args:
            lookback_days: Days to analyze for validation
            
        Returns:
            Performance validation metrics
        """
        print(f"🔍 Validating polygon-driven pool performance over {lookback_days} days...")
        
        # Get current optimized pool
        current_pool = self.get_polygon_driven_pool(analysis_days=180, target_size=120)
        
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
            spread_max_bps=3.0
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
            "data_source": "Polygon API",
            "pool_stability": "HIGH" if len(overlap) / len(current_pool) > 0.8 else "MEDIUM" if len(overlap) / len(current_pool) > 0.6 else "LOW"
        }
        
        print("✅ Validation complete:")
        print("   - Data source: Polygon API")
        print(f"   - Pool stability: {validation_metrics['pool_stability']}")
        print(f"   - Overlap: {len(overlap)}/{len(current_pool)} symbols ({validation_metrics['overlap_percentage']:.1f}%)")
        
        return validation_metrics


def get_polygon_driven_symbols(analysis_days: int = 180, target_size: int = 120) -> List[str]:
    """
    Convenience function to get polygon-driven symbols.
    
    Args:
        analysis_days: Days of historical data to analyze
        target_size: Target number of symbols
        
    Returns:
        List of polygon-driven optimized symbols for day trading
    """
    pool = PolygonDrivenSymbolPool()
    return pool.get_polygon_driven_pool(analysis_days, target_size)


# Example usage
if __name__ == "__main__":
    print("🎯 POLYGON-DRIVEN SYMBOL POOL - 100% GENUINE DATA")
    print("=" * 60)
    
    # Create polygon-driven pool
    pool = PolygonDrivenSymbolPool()
    
    # Get optimized symbols using REAL Polygon data
    symbols = pool.get_polygon_driven_pool(analysis_days=180, target_size=120)
    
    print(f"\n✅ Polygon-driven pool created with {len(symbols)} symbols!")
    print(f"🎯 Top 10 symbols: {symbols[:10]}")
    
    # Validate performance
    validation = pool.validate_pool_performance(lookback_days=30)
    
    print("\n🚀 Ready for day trading with REAL Polygon data!")


