#!/usr/bin/env python3
"""
Test Provider Step by Step
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

def main():
    universe_logger.info("🔍 TESTING PROVIDER STEP BY STEP", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")
    
    try:
        from utils.active_universe_provider import ActiveUniverseProvider
        
        provider = ActiveUniverseProvider()
        
        universe_logger.info("✅ Provider initialized", operation="enhanced_logging")
        
        # Test step 1: Discover candidates
        universe_logger.info("\n📊 Step 1: Testing candidate discovery...", operation="enhanced_logging")
        try:
            candidates = provider._discover_candidates(min_market_cap=10_000_000_000, limit=50)
            universe_logger.info(f"✅ Found {len(candidates, operation="enhanced_logging")} candidates: {candidates[:10]}")
        except Exception as e:
            universe_logger.error(f"❌ Candidate discovery failed: {e}", operation="enhanced_logging")
            return
        
        # Test step 2: Rank candidates
        universe_logger.info("\n📈 Step 2: Testing candidate ranking...", operation="enhanced_logging")
        try:
            end_date = date.today()
            start_date = end_date - timedelta(days=60)
            
            ranked_candidates = provider._discover_and_rank_candidates(
                min_market_cap=10_000_000_000,
                analysis_days=60,
                start_date=start_date,
                end_date=end_date,
                max_candidates=50,
                batch_size=10
            )
            universe_logger.info(f"✅ Ranked {len(ranked_candidates, operation="enhanced_logging")} candidates: {ranked_candidates[:10]}")
        except Exception as e:
            universe_logger.error(f"❌ Candidate ranking failed: {e}", operation="enhanced_logging")
            return
        
        # Test step 3: Sector classifier
        universe_logger.info("\n🏢 Step 3: Testing sector classifier...", operation="enhanced_logging")
        try:
            sector_classifier, sector_weights = provider._build_sector_classifier_and_weights(ranked_candidates[:20])
            universe_logger.info(f"✅ Sector classifier: {bool(sector_classifier, operation="enhanced_logging")}")
            universe_logger.info(f"✅ Sector weights: {bool(sector_weights, operation="enhanced_logging")}")
        except Exception as e:
            universe_logger.error(f"❌ Sector classifier failed: {e}", operation="enhanced_logging")
            return
        
        # Test step 4: Earnings exclusion
        universe_logger.info("\n📅 Step 4: Testing earnings exclusion...", operation="enhanced_logging")
        try:
            earnings_calendar_data = provider.polygon_client.get_earnings_calendar("AAPL", start_date, end_date)
            earnings_available = earnings_calendar_data.get("status") == "OK" or earnings_calendar_data.get("results")
            universe_logger.info(f"✅ Earnings available: {earnings_available}", operation="enhanced_logging")
        except Exception as e:
            universe_logger.error(f"❌ Earnings test failed: {e}", operation="enhanced_logging")
            return
        
        # Test step 5: Full universe generation
        universe_logger.info("\n🎯 Step 5: Testing full universe generation...", operation="enhanced_logging")
        try:
            universe = provider.get_active_universe(
                target_size=50,
                analysis_days=60,
                force_refresh=True,
                batch_size=10,
                prefilter_max_symbols=50
            )
            
            if universe:
                universe_logger.info(f"✅ SUCCESS: Generated {len(universe, operation="enhanced_logging")} symbols")
                universe_logger.info(f"📈 First 10: {universe[:10]}", operation="enhanced_logging")
            else:
                universe_logger.error("❌ FAILED: No universe generated", operation="enhanced_logging")
                
        except Exception as e:
            universe_logger.error(f"❌ Universe generation failed: {e}", operation="enhanced_logging")
            import traceback
            traceback.print_exc()
                
    except Exception as e:
        universe_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
