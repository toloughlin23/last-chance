#!/usr/bin/env python3
"""
Final test of the universe provider to see the complete results.
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv

load_dotenv()

from utils.active_universe_provider import ActiveUniverseProvider


def test_final_universe():
    """Test the final universe generation."""

    print("🚀 FINAL UNIVERSE TEST")
    print("=" * 50)

    try:
        print("📊 Creating provider...")
        provider = ActiveUniverseProvider()

        print("🎯 Getting active universe...")
        universe = provider.get_active_universe(
            target_size=120, force_refresh=True, batch_size=5
        )

        print("\n🎉 FINAL RESULT:")
        print(f"   Generated {len(universe)} symbols for active day trading")
        print(f"   Top 20 symbols: {universe[:20]}")
        print(f"   Total universe size: {len(universe)} symbols")

        if len(universe) >= 120:
            print(f"\n✅ SUCCESS: Got {len(universe)} symbols (target: 120)")
        else:
            print(f"\n⚠️ WARNING: Only got {len(universe)} symbols (target: 120)")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_final_universe()
    sys.exit(0 if success else 1)
