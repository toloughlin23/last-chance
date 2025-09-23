#!/usr/bin/env python3
"""
Use Provider's 200 Candidates Directly
Get the 200 candidates that the provider already found and test enhanced selector
"""

import json
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from utils.universe_selector import UniverseSelector

def main():
    load_dotenv()
    
    print("🚀 USING PROVIDER'S 200 CANDIDATES")
    print("=" * 50)
    print("Getting 200 candidates from provider cache")
    print("=" * 50)
    
    # Get the 200 candidates from provider's cache
    cache_path = "data/cache/active_universe_cache.json"
    
    if not os.path.exists(cache_path):
        print("❌ No provider cache found. Need to run provider first.")
        return
    
    try:
        with open(cache_path, "r") as f:
            cache_data = json.load(f)
        
        # Get the ranked candidates from provider
        candidates = cache_data.get("ranked_candidates", [])
        
        if not candidates:
            print("❌ No ranked candidates in cache")
            return
            
        print(f"📊 Found {len(candidates)} candidates from provider cache")
        print(f"📈 Sample: {candidates[:10]}")
        
        # Initialize enhanced selector
        selector = UniverseSelector()
        
        # Set analysis period
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        
        print(f"\n🎯 Applying ENHANCED GROWTH Algorithm:")
        print("  ✅ Higher volatility preference")
        print("  ✅ Momentum scoring")
        print("  ✅ Growth potential metrics")
        print("  ✅ Sector rotation (Tech=1.0, Financials=0.4)")
        print("  ✅ Breakout detection")
        
        # Apply enhanced selector
        universe = selector.select_universe(
            candidates=candidates,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=120,
            target_max_size=150,
            allow_expand_above_target=True,
            expand_margin=0.9,
            # Enhanced filters for growth trading
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.08,  # Allow higher volatility
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=8.0,  # More lenient for growth
            spread_lookback_days=5,
            spread_core_hours_only=True,
            # Enhanced weights for growth
            weight_adv=0.20,
            weight_spread=0.10,
            weight_volatility=0.25,
            weight_stability=0.05,
            weight_momentum=0.15,
            weight_growth=0.10,
            weight_breakout=0.05,
            weight_sector_rotation=0.10,
            # No sector balancing for now
            sector_classifier=None,
            sector_index_weights=None,
            earnings_exclusion=None,
            earnings_buffer_days=0,
        )
        
        if not universe:
            print("❌ No universe generated")
            return
            
        print(f"\n✅ ENHANCED ALGORITHM SUCCESS!")
        print(f"📊 Generated universe with {len(universe)} symbols")
        print(f"📈 First 20: {universe[:20]}")
        
        # Save results
        os.makedirs("data/training", exist_ok=True)
        training_file = "data/training/enhanced_universe_list.json"
        
        training_data = {
            "generated_date": date.today().isoformat(),
            "symbol_count": len(universe),
            "symbols": universe,
            "description": "Enhanced growth-oriented universe using provider's 200 candidates",
            "algorithm": "Enhanced with momentum, growth, sector rotation, and breakout detection",
            "data_source": "Provider's 200 candidates + enhanced growth algorithm"
        }
        
        with open(training_file, "w") as f:
            json.dump(training_data, f, indent=2)
        
        print(f"\n💾 Saved enhanced universe to: {training_file}")
        print(f"\n🎯 ENHANCED ALGORITHM SUCCESS!")
        print("✅ Growth-oriented selection complete")
        print("✅ Using provider's 200 candidates automatically")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
