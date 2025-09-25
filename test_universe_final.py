#!/usr/bin/env python3
"""
Final test of the universe provider to see the complete results.
"""

import os
import sys

from dotenv import load_dotenv

try:
    from utils.active_universe_provider import ActiveUniverseProvider
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from utils.active_universe_provider import ActiveUniverseProvider

load_dotenv()


def test_final_universe():
    """Test the final universe generation."""

    universe_logger.info("🚀 FINAL UNIVERSE TEST", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")

    try:
        universe_logger.info("📊 Creating provider...", operation="enhanced_logging")
        provider = ActiveUniverseProvider()

        universe_logger.info("🎯 Getting active universe...", operation="enhanced_logging")
        universe = provider.get_active_universe(
            target_size=120, force_refresh=True, batch_size=5
        )

        universe_logger.info("\n🎉 FINAL RESULT:", operation="enhanced_logging")
        universe_logger.info(f"   Generated {len(universe, operation="enhanced_logging")} symbols for active day trading")
        universe_logger.info(f"   Top 20 symbols: {universe[:20]}", operation="enhanced_logging")
        universe_logger.info(f"   Total universe size: {len(universe, operation="enhanced_logging")} symbols")

        if len(universe) >= 120:
            universe_logger.info(f"\n✅ SUCCESS: Got {len(universe, operation="enhanced_logging")} symbols (target: 120)")
        else:
            universe_logger.warning(f"\n⚠️ WARNING: Only got {len(universe, operation="enhanced_logging")} symbols (target: 120)")

        return True

    except Exception as e:
        universe_logger.error(f"❌ Test failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_final_universe()
    sys.exit(0 if success else 1)
