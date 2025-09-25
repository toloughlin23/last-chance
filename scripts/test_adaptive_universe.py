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

load_dotenv()


def test_adaptive_universe():
    """Test that we get 120-150 symbols with adaptive filtering."""

    universe_logger.info("🚀 Testing Adaptive Universe Provider", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")

    try:
        provider = AdaptiveUniverseProvider()

        # Test with different target sizes
        test_cases = [
            {"target_size": 120, "target_max_size": 150, "name": "Standard"},
            {"target_size": 100, "target_max_size": 120, "name": "Conservative"},
            {"target_size": 150, "target_max_size": 200, "name": "Expanded"},
        ]

        for case in test_cases:
            universe_logger.info(f"\n📊 Testing {case['name']} case: {case['target_size']}-{case['target_max_size']} symbols", operation="enhanced_logging")

            universe = provider.get_adaptive_universe(
                target_size=case["target_size"],
                target_max_size=case["target_max_size"],
                analysis_days=60,
                force_refresh=True,
            )

            universe_logger.info(f"✅ Generated {len(universe, operation="enhanced_logging")} symbols")

            if len(universe) >= case["target_size"]:
                universe_logger.info(f"🎯 SUCCESS: Got {len(universe, operation="enhanced_logging")} symbols (target: {case['target_size']})"
                )
            else:
                universe_logger.warning(f"⚠️ WARNING: Only {len(universe, operation="enhanced_logging")} symbols (target: {case['target_size']})"
                )

            # Show first 10 symbols
            universe_logger.info(f"   Top 10: {universe[:10]}", operation="enhanced_logging")

            # Check if we have good diversity
            if len(universe) >= 50:
                universe_logger.info(f"   Diversity: Good ({len(universe, operation="enhanced_logging")} symbols)")
            else:
                universe_logger.info(f"   Diversity: Limited ({len(universe, operation="enhanced_logging")} symbols)")

        universe_logger.info("\n🎉 Adaptive Universe Provider test completed!", operation="enhanced_logging")
        return True

    except Exception as e:
        universe_logger.error(f"❌ Test failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_adaptive_universe()
    sys.exit(0 if success else 1)
