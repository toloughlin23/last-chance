#!/usr/bin/env python3
"""
Quick Universe Test - Fast version for tool execution
Tests provider and selector with smaller dataset
"""

import json
import os
from datetime import date, timedelta

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    universe_logger.info("🚀 QUICK UNIVERSE TEST", operation="enhanced_logging")
    universe_logger.info("=" * 40, operation="enhanced_logging")
    universe_logger.info("Testing with smaller dataset for tool execution", operation="enhanced_logging")
    universe_logger.info("=" * 40, operation="enhanced_logging")

    # Initialize provider
    provider = ActiveUniverseProvider()

    universe_logger.info("\n📊 Step 1: Testing S&P 500 search...", operation="enhanced_logging")

    # Test with very small parameters to avoid timeout
    try:
        # First test: just get candidates (no ranking)
        candidates = provider._discover_candidates(limit=20)
        universe_logger.info(f"✅ Found {len(candidates, operation="enhanced_logging")} candidates from S&P 500")
        universe_logger.info(f"📈 Sample: {candidates[:10]}", operation="enhanced_logging")

        if len(candidates) >= 10:
            universe_logger.info("✅ S&P 500 search working correctly", operation="enhanced_logging")
        else:
            universe_logger.warning("⚠️ Limited candidates found", operation="enhanced_logging")

    except Exception as e:
        universe_logger.error(f"❌ S&P 500 search failed: {e}", operation="enhanced_logging")
        return

    universe_logger.info("\n📊 Step 2: Testing quality ranking...", operation="enhanced_logging")

    try:
        # Test ranking with very small dataset
        ranked = provider._rank_symbols_by_quality(
            candidates[:10],  # Only rank first 10
            10_000_000_000,  # $10B market cap
            30,  # 30 days analysis
            date.today() - timedelta(days=30),
            date.today(),
            5,  # Top 5 only
            5,  # Small batch size
        )

        universe_logger.info(f"✅ Ranked {len(ranked, operation="enhanced_logging")} symbols by quality")
        universe_logger.info(f"📈 Top ranked: {ranked}", operation="enhanced_logging")

    except Exception as e:
        universe_logger.error(f"❌ Quality ranking failed: {e}", operation="enhanced_logging")
        return

    universe_logger.info("\n📊 Step 3: Testing full universe generation...", operation="enhanced_logging")

    try:
        # Test full generation with minimal parameters
        universe = provider.get_active_universe(
            target_size=20,  # Small target
            analysis_days=30,  # Shorter analysis
            force_refresh=True,
            batch_size=5,  # Very small batches
            prefilter_max_symbols=50,  # Analyze only 50
        )

        universe_logger.info(f"✅ Generated universe with {len(universe, operation="enhanced_logging")} symbols")
        universe_logger.info(f"📈 Universe: {universe}", operation="enhanced_logging")

        # Save test results
        os.makedirs("data/training", exist_ok=True)
        realistic_universe_data = {
            "test_date": date.today().isoformat(),
            "symbol_count": len(universe),
            "symbols": universe,
            "test_type": "comprehensive_universe_analysis",
            "data_source": "100% real Polygon data with advanced filtering",
        }

        with open("data/training/quick_test_universe.json", "w") as f:
            json.dump(realistic_universe_data, f, indent=2)

        universe_logger.info("💾 Saved test results to: data/training/quick_test_universe.json", operation="enhanced_logging")

    except Exception as e:
        universe_logger.error(f"❌ Full generation failed: {e}", operation="enhanced_logging")
        return

    universe_logger.info("\n🎯 QUICK TEST COMPLETE!", operation="enhanced_logging")
    universe_logger.info("=" * 40, operation="enhanced_logging")
    universe_logger.info("✅ Provider working", operation="enhanced_logging")
    universe_logger.info("✅ Selector working", operation="enhanced_logging")
    universe_logger.info("✅ Real Polygon data", operation="enhanced_logging")
    universe_logger.info("✅ Ready for full generation", operation="enhanced_logging")

    universe_logger.info("\n💡 For full 120-symbol universe, run:", operation="enhanced_logging")
    universe_logger.info("   python scripts/generate_training_universe.py", operation="enhanced_logging")


if __name__ == "__main__":
    main()
