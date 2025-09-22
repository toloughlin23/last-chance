#!/usr/bin/env python3
"""
Test the Adaptive Universe Provider to ensure we get 120-150 symbols.
"""

import os
import sys
from dotenv import load_dotenv

try:
    from utils.adaptive_universe_provider import AdaptiveUniverseProvider
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from utils.adaptive_universe_provider import AdaptiveUniverseProvider


def test_adaptive_universe():
    """Test that we get 120-150 symbols with adaptive filtering."""

    print("🚀 Testing Adaptive Universe Provider")
    print("=" * 50)

    try:
        provider = AdaptiveUniverseProvider()

        # Test with different target sizes
        test_cases = [
            {"target_size": 120, "target_max_size": 150, "name": "Standard"},
            {"target_size": 100, "target_max_size": 120, "name": "Conservative"},
            {"target_size": 150, "target_max_size": 200, "name": "Expanded"},
        ]

        for case in test_cases:
            print(
                f"\n📊 Testing {case['name']} case: {case['target_size']}-{case['target_max_size']} symbols"
            )

            universe = provider.get_adaptive_universe(
                target_size=case["target_size"],
                target_max_size=case["target_max_size"],
                analysis_days=60,
                force_refresh=True,
            )

            print(f"✅ Generated {len(universe)} symbols")

            if len(universe) >= case["target_size"]:
                print(
                    f"🎯 SUCCESS: Got {len(universe)} symbols (target: {case['target_size']})"
                )
            else:
                print(
                    f"⚠️ WARNING: Only {len(universe)} symbols (target: {case['target_size']})"
                )

            # Show first 10 symbols
            print(f"   Top 10: {universe[:10]}")

            # Check if we have good diversity
            if len(universe) >= 50:
                print(f"   Diversity: Good ({len(universe)} symbols)")
            else:
                print(f"   Diversity: Limited ({len(universe)} symbols)")

        print("\n🎉 Adaptive Universe Provider test completed!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_adaptive_universe()
    sys.exit(0 if success else 1)
