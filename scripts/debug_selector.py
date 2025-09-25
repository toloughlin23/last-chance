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
    universe_logger.info("🔍 DEBUGGING SELECTOR ISSUES", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")
    
    try:
        from utils.universe_selector import UniverseSelector
        from services.polygon_client import PolygonClient
        from services.quotes_client import QuotesClient
        
        universe_logger.info("✅ All imports successful", operation="enhanced_logging")
        
        # Test basic initialization
        client = PolygonClient()
        quotes = QuotesClient()
        selector = UniverseSelector(client, quotes)
        universe_logger.info("✅ Selector initialization successful", operation="enhanced_logging")
        
        # Test with a small set of candidates
        test_candidates = ['AAPL', 'MSFT', 'GOOGL', 'BAC', 'JPM']
        universe_logger.info(f"📊 Testing with {len(test_candidates, operation="enhanced_logging")} candidates: {test_candidates}")
        
        # Set analysis period with optimized timeframe
        end_date = date.today()
        start_date = end_date - timedelta(days=30)  # Focused analysis period for comprehensive evaluation
        
        universe_logger.info(f"📅 Analysis period: {start_date} to {end_date}", operation="enhanced_logging")
        
        # Test the selector with minimal parameters
        universe_logger.info("\n🎯 Testing selector with minimal parameters...", operation="enhanced_logging")
        
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
            spread_filter_enabled=False,  # Disable spread filter for comprehensive analysis
            # No sector balancing
            sector_classifier=None,
            sector_index_weights=None,
            earnings_exclusion=None,
            earnings_buffer_days=0,
        )
        
        if universe:
            universe_logger.info(f"✅ Selector SUCCESS! Generated {len(universe, operation="enhanced_logging")} symbols: {universe}")
        else:
            universe_logger.error("❌ Selector returned empty universe", operation="enhanced_logging")
            
    except Exception as e:
        universe_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
