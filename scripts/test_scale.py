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
    print("🔍 TESTING SELECTOR SCALE")
    print("=" * 50)
    
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
            print(f"\n🧪 Testing with {size} candidates...")
            candidates = all_candidates[:size]
            
            try:
                universe = selector.select_universe(
                    candidates=candidates,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    target_size=min(10, size),  # Smaller target for testing
                    target_max_size=min(15, size),
                    allow_expand_above_target=True,
                    expand_margin=0.9,
                    # Minimal filters
                    min_price=5.0,
                    min_atr_pct=0.005,
                    max_atr_pct=0.10,
                    adv_min_dollar=10_000_000.0,
                    spread_filter_enabled=False,  # Disable for testing
                    sector_classifier=None,
                    sector_index_weights=None,
                    earnings_exclusion=None,
                    earnings_buffer_days=0,
                )
                
                if universe:
                    print(f"✅ SUCCESS: {len(universe)} symbols - {universe[:5]}")
                else:
                    print(f"❌ FAILED: Empty universe")
                    
            except Exception as e:
                print(f"❌ FAILED at {size} candidates: {e}")
                break
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
