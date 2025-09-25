#!/usr/bin/env python3
"""
Test Selector Scale
Find the breaking point when processing more candidates
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

def main():
    training_logger.info("🔍 TESTING SELECTOR SCALE", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")
    
    try:
        from utils.universe_selector import UniverseSelector
        from services.polygon_client import PolygonClient
        from services.quotes_client import QuotesClient
        
        # Initialize
        client = PolygonClient()
        quotes = QuotesClient()
        selector = UniverseSelector(client, quotes)
        
        # Test different scales
        test_sizes = [5, 10, 20, 50, 100]
        
        # Create test candidates
        all_candidates = [
            'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE',
            'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC',
            'BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB',
            'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON',
            'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO',
            'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K',
            'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'LLY',
            'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'ZTS', 'CVS', 'CI',
            'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'ABNB', 'MAR', 'HLT',
            'PG', 'KO', 'PEP', 'WMT', 'COST', 'TGT', 'CL', 'KMB', 'GIS', 'K',
            'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'ES', 'PPL', 'WEC',
            'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'O', 'SPG', 'WELL', 'AVB', 'EQR',
            'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'NEM', 'FCX', 'NUE',
            'BA', 'CAT', 'GE', 'HON', 'MMM', 'UPS', 'FDX', 'LMT', 'RTX', 'NOC'
        ]
        
        # Set analysis period
        end_date = date.today()
        start_date = end_date - timedelta(days=30)
        
        for size in test_sizes:
            training_logger.info(f"\n🧪 Testing with {size} candidates...", operation="enhanced_logging")
            candidates = all_candidates[:size]
            
            try:
                universe = selector.select_universe(
                    candidates=candidates,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    target_size=min(10, size),  # Optimized target size for comprehensive analysis
                    target_max_size=min(15, size),
                    allow_expand_above_target=True,
                    expand_margin=0.9,
                    # Minimal filters
                    min_price=5.0,
                    min_atr_pct=0.005,
                    max_atr_pct=0.10,
                    adv_min_dollar=10_000_000.0,
                    spread_filter_enabled=False,  # Optimized for comprehensive analysis
                    sector_classifier=None,
                    sector_index_weights=None,
                    earnings_exclusion=None,
                    earnings_buffer_days=0,
                )
                
                if universe:
                    training_logger.info(f"✅ SUCCESS: {len(universe, operation="enhanced_logging")} symbols - {universe[:5]}")
                else:
                    training_logger.error(f"❌ FAILED: Empty universe", operation="enhanced_logging")
                    
            except Exception as e:
                training_logger.error(f"❌ FAILED at {size} candidates: {e}", operation="enhanced_logging")
                break
                
    except Exception as e:
        training_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
