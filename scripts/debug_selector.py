#!/usr/bin/env python3
"""
Debug Selector Issues
Test the selector step by step to find the exact problem
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

def main():
    print("🔍 DEBUGGING SELECTOR ISSUES")
    print("=" * 50)
    
    try:
        from utils.universe_selector import UniverseSelector
        from services.polygon_client import PolygonClient
        from services.quotes_client import QuotesClient
        
        print("✅ All imports successful")
        
        # Test basic initialization
        client = PolygonClient()
        quotes = QuotesClient()
        selector = UniverseSelector(client, quotes)
        print("✅ Selector initialization successful")
        
        # Test with a small set of candidates
        test_candidates = ['AAPL', 'MSFT', 'GOOGL', 'BAC', 'JPM']
        print(f"📊 Testing with {len(test_candidates)} candidates: {test_candidates}")
        
        # Set analysis period
        end_date = date.today()
        start_date = end_date - timedelta(days=30)  # Shorter period for testing
        
        print(f"📅 Analysis period: {start_date} to {end_date}")
        
        # Test the selector with minimal parameters
        print("\n🎯 Testing selector with minimal parameters...")
        
        universe = selector.select_universe(
            candidates=test_candidates,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=3,
            target_max_size=5,
            allow_expand_above_target=True,
            expand_margin=0.9,
            # Minimal filters
            min_price=5.0,  # Lower threshold
            min_atr_pct=0.005,  # Lower threshold
            max_atr_pct=0.10,  # Higher threshold
            adv_min_dollar=10_000_000.0,  # Lower threshold
            spread_filter_enabled=False,  # Disable spread filter for testing
            # No sector balancing
            sector_classifier=None,
            sector_index_weights=None,
            earnings_exclusion=None,
            earnings_buffer_days=0,
        )
        
        if universe:
            print(f"✅ Selector SUCCESS! Generated {len(universe)} symbols: {universe}")
        else:
            print("❌ Selector returned empty universe")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
