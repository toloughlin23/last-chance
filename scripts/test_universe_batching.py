#!/usr/bin/env python3
"""Test universe selection with detailed progress tracking"""

import time

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    universe_logger.info("🔍 Testing Universe Selection with Smart Batching", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Test with smaller parameters to see what's happening
    start_time = time.time()

    try:
        universe = provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,  # Smaller batches
            adv_prefilter_min_dollar=50_000_000,  # Lower threshold to get more results
        )

        elapsed = time.time() - start_time

        universe_logger.info(f"\n✅ Completed in {elapsed:.1f} seconds", operation="enhanced_logging")
        universe_logger.info(f"📊 Selected {len(universe, operation="enhanced_logging")} symbols")

        if universe:
            universe_logger.info(f"\nFirst 20 symbols: {universe[:20]}", operation="enhanced_logging")
        else:
            universe_logger.error("\n❌ No symbols selected - investigating why...", operation="enhanced_logging")

            # Let's trace through the steps manually
            universe_logger.info("\nDiagnosing issue:", operation="enhanced_logging")

            # Step 1: Check candidate discovery
            candidates = provider._discover_candidates()
            universe_logger.info(f"1. Candidates discovered: {len(candidates, operation="enhanced_logging")}")
            if candidates:
                universe_logger.info(f"   First 10: {candidates[:10]}", operation="enhanced_logging")

            # Step 2: Check if prefiltering is too strict
            if candidates:
                from datetime import date, timedelta

                end = date.today()
                start = end - timedelta(days=60)

                universe_logger.info("\n2. Testing ADV prefilter on first 5 candidates...", operation="enhanced_logging")
                prefiltered = provider._prefilter_by_adv_and_price(
                    candidates[:5],
                    start.isoformat(),
                    end.isoformat(),
                    adv_min_dollar=50_000_000,
                    price_min=10.0,
                    max_symbols=5,
                    batch_size=5,
                )
                universe_logger.info(f"   Prefiltered: {len(prefiltered, operation="enhanced_logging")} passed")
                universe_logger.info(f"   Results: {prefiltered}", operation="enhanced_logging")

    except Exception as e:
        universe_logger.error(f"\n❌ Error: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
