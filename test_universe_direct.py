#!/usr/bin/env python3
"""
Direct Universe Test - Bypass terminal tool
"""

import os

from dotenv import load_dotenv

# Set environment
os.environ["PYTHONPATH"] = "."


def main():
    universe_logger.info("🚀 DIRECT UNIVERSE TEST", operation="enhanced_logging")
    universe_logger.info("=" * 40, operation="enhanced_logging")

    try:
        # Load environment
        load_dotenv()
        universe_logger.info("✅ Environment loaded", operation="enhanced_logging")

        # Import modules
        from utils.active_universe_provider import ActiveUniverseProvider

        universe_logger.info("✅ Modules imported", operation="enhanced_logging")

        # Initialize provider
        provider = ActiveUniverseProvider()
        universe_logger.info("✅ Provider initialized", operation="enhanced_logging")

        # Generate universe
        universe_logger.info("🔄 Generating universe...", operation="enhanced_logging")
        universe = provider.get_active_universe(
            target_size=5, force_refresh=True, batch_size=5
        )

        universe_logger.info(f"✅ Generated {len(universe, operation="enhanced_logging")} symbols: {universe}")

    except Exception as e:
        universe_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
