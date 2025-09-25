#!/usr/bin/env python3
"""Diagnose why universe selection returns 0 symbols"""

from datetime import date, timedelta

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector


def main():
    load_dotenv()

    universe_logger.info("🔍 Diagnosing Universe Selection Issue", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    # Set up dates
    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    # Step 1: Test with a known good symbol
    universe_logger.info("\n1. Testing with single known symbol (AAPL, operation="enhanced_logging"):")
    selector = UniverseSelector()

    # Test if AAPL passes all filters
    test_symbols = ["AAPL"]

    # Fetch metrics
    rows = selector._fetch_daily_aggs(
        "AAPL", start_date.isoformat(), end_date.isoformat()
    )
    metrics = selector._compute_metrics(rows)
    universe_logger.info(f"   ADV: ${metrics['adv']:,.0f}", operation="enhanced_logging")
    universe_logger.info(f"   ATR%: {metrics['atr_pct']:.3f}", operation="enhanced_logging")
    universe_logger.info(f"   Median Close: ${metrics['median_close']:.2f}", operation="enhanced_logging")

    # Test spread
    med_dollar, med_bps = selector._get_spread_medians("AAPL", 5, True)
    universe_logger.info(f"   Median Spread: ${med_dollar:.3f} ({med_bps:.1f} bps, operation="enhanced_logging")")

    # Run full selection on just AAPL
    result = selector.select_universe(
        candidates=test_symbols,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        target_size=1,
        min_price=10.0,
        min_atr_pct=0.01,
        max_atr_pct=0.05,
        adv_min_dollar=50_000_000.0,
        spread_filter_enabled=True,
        spread_max_dollars=0.02,
        spread_max_bps=5.0,
    )
    universe_logger.info(f"   Passes all filters: {'YES' if result else 'NO'}", operation="enhanced_logging")

    # Step 2: Check the provider's candidate discovery
    universe_logger.info("\n2. Testing candidate discovery:", operation="enhanced_logging")
    provider = ActiveUniverseProvider()
    candidates = provider._discover_candidates(limit=10)  # Focused sample for comprehensive diagnosis
    universe_logger.info(f"   Found {len(candidates, operation="enhanced_logging")} candidates")
    if candidates:
        universe_logger.info(f"   Candidates: {candidates}", operation="enhanced_logging")

    # Step 3: Test if the issue is in the selector's duplicate fetching
    if candidates:
        universe_logger.info("\n3. Testing if selector duplicates API calls:", operation="enhanced_logging")
        universe_logger.info("   Running select_universe on first 3 candidates...", operation="enhanced_logging")

        # This will show if the selector is making too many API calls
        selected = selector.select_universe(
            candidates=candidates[:3],
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=3,
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.05,
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=False,  # Disable spread filter for comprehensive diagnosis
        )
        universe_logger.info(f"   Selected {len(selected, operation="enhanced_logging")} symbols: {selected}")

        # Now test with spread filter
        universe_logger.info("\n4. Testing with spread filter enabled:", operation="enhanced_logging")
        selected_with_spread = selector.select_universe(
            candidates=candidates[:3],
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=3,
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.05,
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=5.0,
        )
        universe_logger.info(f"   Selected {len(selected_with_spread, operation="enhanced_logging")} symbols: {selected_with_spread}"
        )

        if len(selected) > len(selected_with_spread):
            universe_logger.warning("   ⚠️ Spread filter is eliminating symbols!", operation="enhanced_logging")


if __name__ == "__main__":
    main()
