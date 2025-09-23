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
    print("🔍 TESTING PROVIDER STEP BY STEP")
    print("=" * 50)
    
    try:
        from utils.active_universe_provider import ActiveUniverseProvider
        
        provider = ActiveUniverseProvider()
        
        print("✅ Provider initialized")
        
        # Test step 1: Discover candidates
        print("\n📊 Step 1: Testing candidate discovery...")
        try:
            candidates = provider._discover_candidates(min_market_cap=10_000_000_000, limit=50)
            print(f"✅ Found {len(candidates)} candidates: {candidates[:10]}")
        except Exception as e:
            print(f"❌ Candidate discovery failed: {e}")
            return
        
        # Test step 2: Rank candidates
        print("\n📈 Step 2: Testing candidate ranking...")
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
            print(f"✅ Ranked {len(ranked_candidates)} candidates: {ranked_candidates[:10]}")
        except Exception as e:
            print(f"❌ Candidate ranking failed: {e}")
            return
        
        # Test step 3: Sector classifier
        print("\n🏢 Step 3: Testing sector classifier...")
        try:
            sector_classifier, sector_weights = provider._build_sector_classifier_and_weights(ranked_candidates[:20])
            print(f"✅ Sector classifier: {bool(sector_classifier)}")
            print(f"✅ Sector weights: {bool(sector_weights)}")
        except Exception as e:
            print(f"❌ Sector classifier failed: {e}")
            return
        
        # Test step 4: Earnings exclusion
        print("\n📅 Step 4: Testing earnings exclusion...")
        try:
            test_data = provider.polygon_client.get_earnings_calendar("AAPL", start_date, end_date)
            earnings_available = test_data.get("status") == "OK" or test_data.get("results")
            print(f"✅ Earnings available: {earnings_available}")
        except Exception as e:
            print(f"❌ Earnings test failed: {e}")
            return
        
        # Test step 5: Full universe generation
        print("\n🎯 Step 5: Testing full universe generation...")
        try:
            universe = provider.get_active_universe(
                target_size=50,
                analysis_days=60,
                force_refresh=True,
                batch_size=10,
                prefilter_max_symbols=50
            )
            
            if universe:
                print(f"✅ SUCCESS: Generated {len(universe)} symbols")
                print(f"📈 First 10: {universe[:10]}")
            else:
                print("❌ FAILED: No universe generated")
                
        except Exception as e:
            print(f"❌ Universe generation failed: {e}")
            import traceback
            traceback.print_exc()
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
