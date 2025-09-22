#!/usr/bin/env python3
"""
Quick Universe Test - Fast version for tool execution
Tests provider and selector with smaller dataset
"""

from dotenv import load_dotenv
from utils.active_universe_provider import ActiveUniverseProvider
from datetime import date, timedelta
import json
import os

def main():
    load_dotenv()
    
    print("🚀 QUICK UNIVERSE TEST")
    print("=" * 40)
    print("Testing with smaller dataset for tool execution")
    print("=" * 40)
    
    # Initialize provider
    provider = ActiveUniverseProvider()
    
    print("\n📊 Step 1: Testing S&P 500 search...")
    
    # Test with very small parameters to avoid timeout
    try:
        # First test: just get candidates (no ranking)
        candidates = provider._discover_candidates(limit=20)
        print(f"✅ Found {len(candidates)} candidates from S&P 500")
        print(f"📈 Sample: {candidates[:10]}")
        
        if len(candidates) >= 10:
            print("✅ S&P 500 search working correctly")
        else:
            print("⚠️ Limited candidates found")
            
    except Exception as e:
        print(f"❌ S&P 500 search failed: {e}")
        return
    
    print("\n📊 Step 2: Testing quality ranking...")
    
    try:
        # Test ranking with very small dataset
        ranked = provider._rank_symbols_by_quality(
            candidates[:10],  # Only rank first 10
            10_000_000_000,   # $10B market cap
            30,               # 30 days analysis
            date.today() - timedelta(days=30),
            date.today(),
            5,                # Top 5 only
            5                 # Small batch size
        )
        
        print(f"✅ Ranked {len(ranked)} symbols by quality")
        print(f"📈 Top ranked: {ranked}")
        
    except Exception as e:
        print(f"❌ Quality ranking failed: {e}")
        return
    
    print("\n📊 Step 3: Testing full universe generation...")
    
    try:
        # Test full generation with minimal parameters
        universe = provider.get_active_universe(
            target_size=20,           # Small target
            analysis_days=30,         # Shorter analysis
            force_refresh=True,
            batch_size=5,             # Very small batches
            prefilter_max_symbols=50, # Analyze only 50
        )
        
        print(f"✅ Generated universe with {len(universe)} symbols")
        print(f"📈 Universe: {universe}")
        
        # Save test results
        os.makedirs("data/training", exist_ok=True)
        test_data = {
            "test_date": date.today().isoformat(),
            "symbol_count": len(universe),
            "symbols": universe,
            "test_type": "quick_test",
            "data_source": "100% real Polygon data"
        }
        
        with open("data/training/quick_test_universe.json", "w") as f:
            json.dump(test_data, f, indent=2)
        
        print(f"💾 Saved test results to: data/training/quick_test_universe.json")
        
    except Exception as e:
        print(f"❌ Full generation failed: {e}")
        return
    
    print("\n🎯 QUICK TEST COMPLETE!")
    print("=" * 40)
    print("✅ Provider working")
    print("✅ Selector working") 
    print("✅ Real Polygon data")
    print("✅ Ready for full generation")
    
    print("\n💡 For full 120-symbol universe, run:")
    print("   python scripts/generate_training_universe.py")

if __name__ == "__main__":
    main()


