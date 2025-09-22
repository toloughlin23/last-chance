#!/usr/bin/env python3
"""Diagnose why universe selection returns 0 symbols"""

from datetime import date, timedelta

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector


def main():
    load_dotenv()

    print("🔍 Diagnosing Universe Selection Issue")
    print("=" * 60)

    # Set up dates
    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    # Step 1: Test with a known good symbol
    print("\n1. Testing with single known symbol (AAPL):")
    selector = UniverseSelector()

    # Test if AAPL passes all filters
    test_symbols = ["AAPL"]

    # Fetch metrics
    rows = selector._fetch_daily_aggs(
        "AAPL", start_date.isoformat(), end_date.isoformat()
    )
    metrics = selector._compute_metrics(rows)
    print(f"   ADV: ${metrics['adv']:,.0f}")
    print(f"   ATR%: {metrics['atr_pct']:.3f}")
    print(f"   Median Close: ${metrics['median_close']:.2f}")

    # Test spread
    med_dollar, med_bps = selector._get_spread_medians("AAPL", 5, True)
    print(f"   Median Spread: ${med_dollar:.3f} ({med_bps:.1f} bps)")

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
    print(f"   Passes all filters: {'YES' if result else 'NO'}")

    # Step 2: Check the provider's candidate discovery
    print("\n2. Testing candidate discovery:")
    provider = ActiveUniverseProvider()
    candidates = provider._discover_candidates(limit=10)  # Just get 10 for testing
    print(f"   Found {len(candidates)} candidates")
    if candidates:
        print(f"   Candidates: {candidates}")

    # Step 3: Test if the issue is in the selector's duplicate fetching
    if candidates:
        print("\n3. Testing if selector duplicates API calls:")
        print("   Running select_universe on first 3 candidates...")

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
            spread_filter_enabled=False,  # Disable spread filter for now
        )
        print(f"   Selected {len(selected)} symbols: {selected}")

        # Now test with spread filter
        print("\n4. Testing with spread filter enabled:")
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
        print(
            f"   Selected {len(selected_with_spread)} symbols: {selected_with_spread}"
        )

        if len(selected) > len(selected_with_spread):
            print("   ⚠️ Spread filter is eliminating symbols!")


if __name__ == "__main__":
    main()
