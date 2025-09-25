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

# Ensure environment variables are loaded for genuine Polygon integration
load_dotenv()


def compare_providers():
    """Compare different universe providers."""

    universe_logger.info("🔍 COMPARING UNIVERSE PROVIDERS", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    try:
        # Test original provider
        universe_logger.info("\n📊 Testing ORIGINAL ActiveUniverseProvider:", operation="enhanced_logging")
        universe_logger.info("-" * 40, operation="enhanced_logging")

        original_provider = ActiveUniverseProvider()
        original_universe = original_provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,  # Optimized batch size for comprehensive analysis
        )

        universe_logger.info(f"✅ Original Provider: {len(original_universe, operation="enhanced_logging")} symbols")
        if original_universe:
            universe_logger.info(f"   Sample: {original_universe[:10]}", operation="enhanced_logging")

        # Test adaptive provider
        universe_logger.info("\n📊 Testing ADAPTIVE AdaptiveUniverseProvider:", operation="enhanced_logging")
        universe_logger.info("-" * 40, operation="enhanced_logging")

        adaptive_provider = AdaptiveUniverseProvider()
        adaptive_universe = adaptive_provider.get_adaptive_universe(
            target_size=120, target_max_size=150, analysis_days=60, force_refresh=True
        )

        universe_logger.info(f"✅ Adaptive Provider: {len(adaptive_universe, operation="enhanced_logging")} symbols")
        if adaptive_universe:
            universe_logger.info(f"   Sample: {adaptive_universe[:10]}", operation="enhanced_logging")

        # Comparison
        universe_logger.info("\n📈 COMPARISON RESULTS:", operation="enhanced_logging")
        universe_logger.info("=" * 30, operation="enhanced_logging")
        universe_logger.info(f"Original Provider:  {len(original_universe, operation="enhanced_logging"):3d} symbols")
        universe_logger.info(f"Adaptive Provider:  {len(adaptive_universe, operation="enhanced_logging"):3d} symbols")
        universe_logger.info(f"Difference:         {len(adaptive_universe, operation="enhanced_logging") - len(original_universe):+3d} symbols"
        )

        if len(adaptive_universe) > len(original_universe):
            universe_logger.info("🎯 Adaptive provider found MORE symbols!", operation="enhanced_logging")
        elif len(adaptive_universe) == len(original_universe):
            universe_logger.info("🤝 Both providers found the SAME number of symbols", operation="enhanced_logging")
        else:
            universe_logger.warning("⚠️ Original provider found MORE symbols", operation="enhanced_logging")

        # Quality check
        universe_logger.info("\n🔍 QUALITY ANALYSIS:", operation="enhanced_logging")
        universe_logger.info("-" * 20, operation="enhanced_logging")

        if len(original_universe) >= 120:
            universe_logger.info("✅ Original: Meets target (120+, operation="enhanced_logging")")
        else:
            universe_logger.error(f"❌ Original: Below target ({len(original_universe, operation="enhanced_logging")}/120)")

        if len(adaptive_universe) >= 120:
            universe_logger.info("✅ Adaptive: Meets target (120+, operation="enhanced_logging")")
        else:
            universe_logger.error(f"❌ Adaptive: Below target ({len(adaptive_universe, operation="enhanced_logging")}/120)")

        # Recommendation
        universe_logger.info("\n💡 RECOMMENDATION:", operation="enhanced_logging")
        universe_logger.info("-" * 15, operation="enhanced_logging")

        if len(adaptive_universe) >= 120 and len(original_universe) < 120:
            universe_logger.info("🚀 Use ADAPTIVE provider - ensures 120+ symbols", operation="enhanced_logging")
        elif len(original_universe) >= 120 and len(adaptive_universe) < 120:
            universe_logger.info("🎯 Use ORIGINAL provider - already meets target", operation="enhanced_logging")
        elif len(adaptive_universe) >= 120 and len(original_universe) >= 120:
            universe_logger.info("🤔 Both work - choose based on quality preferences", operation="enhanced_logging")
        else:
            universe_logger.warning("⚠️ Both providers need improvement", operation="enhanced_logging")

        return True

    except Exception as e:
        universe_logger.error(f"❌ Comparison failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = compare_providers()
    sys.exit(0 if success else 1)
