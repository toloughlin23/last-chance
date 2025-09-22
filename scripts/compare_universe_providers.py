#!/usr/bin/env python3
"""
Compare different universe providers to show the difference in symbol counts.
"""

import os
import sys
from dotenv import load_dotenv

# Prefer top-level imports; if running outside project root, patch sys.path lazily
try:
    from utils.active_universe_provider import ActiveUniverseProvider
    from utils.adaptive_universe_provider import AdaptiveUniverseProvider
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from utils.active_universe_provider import ActiveUniverseProvider
    from utils.adaptive_universe_provider import AdaptiveUniverseProvider


def compare_providers():
    """Compare different universe providers."""

    print("🔍 COMPARING UNIVERSE PROVIDERS")
    print("=" * 60)

    try:
        # Test original provider
        print("\n📊 Testing ORIGINAL ActiveUniverseProvider:")
        print("-" * 40)

        original_provider = ActiveUniverseProvider()
        original_universe = original_provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,  # Smaller batch for testing
        )

        print(f"✅ Original Provider: {len(original_universe)} symbols")
        if original_universe:
            print(f"   Sample: {original_universe[:10]}")

        # Test adaptive provider
        print("\n📊 Testing ADAPTIVE AdaptiveUniverseProvider:")
        print("-" * 40)

        adaptive_provider = AdaptiveUniverseProvider()
        adaptive_universe = adaptive_provider.get_adaptive_universe(
            target_size=120, target_max_size=150, analysis_days=60, force_refresh=True
        )

        print(f"✅ Adaptive Provider: {len(adaptive_universe)} symbols")
        if adaptive_universe:
            print(f"   Sample: {adaptive_universe[:10]}")

        # Comparison
        print("\n📈 COMPARISON RESULTS:")
        print("=" * 30)
        print(f"Original Provider:  {len(original_universe):3d} symbols")
        print(f"Adaptive Provider:  {len(adaptive_universe):3d} symbols")
        print(
            f"Difference:         {len(adaptive_universe) - len(original_universe):+3d} symbols"
        )

        if len(adaptive_universe) > len(original_universe):
            print("🎯 Adaptive provider found MORE symbols!")
        elif len(adaptive_universe) == len(original_universe):
            print("🤝 Both providers found the SAME number of symbols")
        else:
            print("⚠️ Original provider found MORE symbols")

        # Quality check
        print("\n🔍 QUALITY ANALYSIS:")
        print("-" * 20)

        if len(original_universe) >= 120:
            print("✅ Original: Meets target (120+)")
        else:
            print(f"❌ Original: Below target ({len(original_universe)}/120)")

        if len(adaptive_universe) >= 120:
            print("✅ Adaptive: Meets target (120+)")
        else:
            print(f"❌ Adaptive: Below target ({len(adaptive_universe)}/120)")

        # Recommendation
        print("\n💡 RECOMMENDATION:")
        print("-" * 15)

        if len(adaptive_universe) >= 120 and len(original_universe) < 120:
            print("🚀 Use ADAPTIVE provider - ensures 120+ symbols")
        elif len(original_universe) >= 120 and len(adaptive_universe) < 120:
            print("🎯 Use ORIGINAL provider - already meets target")
        elif len(adaptive_universe) >= 120 and len(original_universe) >= 120:
            print("🤔 Both work - choose based on quality preferences")
        else:
            print("⚠️ Both providers need improvement")

        return True

    except Exception as e:
        print(f"❌ Comparison failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = compare_providers()
    sys.exit(0 if success else 1)
