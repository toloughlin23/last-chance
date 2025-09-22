#!/usr/bin/env python3
"""Test universe selection with detailed progress tracking"""

from dotenv import load_dotenv
from utils.active_universe_provider import ActiveUniverseProvider
import time

def main():
    load_dotenv()
    
    print("🔍 Testing Universe Selection with Smart Batching")
    print("=" * 60)
    
    provider = ActiveUniverseProvider()
    
    # Test with smaller parameters to see what's happening
    start_time = time.time()
    
    try:
        universe = provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,  # Smaller batches
            adv_prefilter_min_dollar=50_000_000,  # Lower threshold to get more results
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Completed in {elapsed:.1f} seconds")
        print(f"📊 Selected {len(universe)} symbols")
        
        if universe:
            print(f"\nFirst 20 symbols: {universe[:20]}")
        else:
            print("\n❌ No symbols selected - investigating why...")
            
            # Let's trace through the steps manually
            print("\nDiagnosing issue:")
            
            # Step 1: Check candidate discovery
            candidates = provider._discover_candidates()
            print(f"1. Candidates discovered: {len(candidates)}")
            if candidates:
                print(f"   First 10: {candidates[:10]}")
            
            # Step 2: Check if prefiltering is too strict
            if candidates:
                from datetime import date, timedelta
                end = date.today()
                start = end - timedelta(days=60)
                
                print("\n2. Testing ADV prefilter on first 5 candidates...")
                prefiltered = provider._prefilter_by_adv_and_price(
                    candidates[:5],
                    start.isoformat(),
                    end.isoformat(),
                    adv_min_dollar=50_000_000,
                    price_min=10.0,
                    max_symbols=5,
                    batch_size=5,
                )
                print(f"   Prefiltered: {len(prefiltered)} passed")
                print(f"   Results: {prefiltered}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()



