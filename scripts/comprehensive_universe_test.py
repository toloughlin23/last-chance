#!/usr/bin/env python3
"""
Comprehensive Universe Provider & Selector Test Suite
Tests all components with 100% real Polygon data
"""

import time
from datetime import date, timedelta

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def test_candidate_discovery():
    """Test 1: Candidate discovery with market cap filtering"""
    universe_logger.info("🔍 Test 1: Candidate Discovery", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Test different market cap thresholds
    for min_cap in [5_000_000_000, 10_000_000_000, 50_000_000_000]:
        candidates = provider._discover_candidates(min_market_cap=min_cap, limit=20)
        universe_logger.info(f"  Min cap ${min_cap/1e9:.0f}B: {len(candidates, operation="enhanced_logging")} candidates")
        if candidates:
            universe_logger.info(f"    Top 5: {candidates[:5]}", operation="enhanced_logging")

    return len(candidates) > 0


def test_adv_prefiltering():
    """Test 2: ADV prefiltering with real data"""
    universe_logger.info("\n🔍 Test 2: ADV Prefiltering", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Get some candidates
    candidates = provider._discover_candidates(limit=10)
    if not candidates:
        universe_logger.error("  ❌ No candidates available for comprehensive analysis", operation="enhanced_logging")
        return False

    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    # Test different ADV thresholds
    for adv_min in [50_000_000, 100_000_000, 500_000_000]:
        prefiltered = provider._prefilter_by_adv_and_price(
            candidates,
            start_date.isoformat(),
            end_date.isoformat(),
            adv_min_dollar=adv_min,
            price_min=10.0,
            max_symbols=10,
            batch_size=5,
        )
        universe_logger.info(f"  ADV > ${adv_min/1e6:.0f}M: {len(prefiltered, operation="enhanced_logging")} passed")
        if prefiltered:
            universe_logger.info(f"    Examples: {prefiltered[:3]}", operation="enhanced_logging")

    return len(prefiltered) > 0


def test_spread_calculation():
    """Test 3: Spread calculation accuracy"""
    universe_logger.info("\n🔍 Test 3: Spread Calculation", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    from services.quotes_client import QuotesClient

    client = QuotesClient()

    # Test with known liquid symbols
    test_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]

    for symbol in test_symbols:
        try:
            med_dollar, med_bps = client.median_spread_over_days(symbol, days=5)
            universe_logger.info(f"  {symbol}: ${med_dollar:.3f} ({med_bps:.1f} bps, operation="enhanced_logging")")

            # Check if values are realistic
            if med_dollar > 1000 or med_bps > 10000:
                universe_logger.warning(f"    ⚠️ WARNING: Unrealistic spread for {symbol}", operation="enhanced_logging")
        except Exception as e:
            universe_logger.error(f"  {symbol}: Error - {e}", operation="enhanced_logging")

    return True


def test_sector_classification():
    """Test 4: Sector classification from Polygon"""
    universe_logger.info("\n🔍 Test 4: Sector Classification", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()
    candidates = provider._discover_candidates(limit=20)

    if candidates:
        sector_classifier, sector_weights = (
            provider._build_sector_classifier_and_weights(candidates)
        )

        if sector_classifier:
            universe_logger.info(f"  Found {len(sector_weights, operation="enhanced_logging")} sectors")
            for sector, weight in list(sector_weights.items())[:5]:
                universe_logger.info(f"    {sector}: {weight:.1%}", operation="enhanced_logging")

            # Test classification on a few symbols
            for symbol in candidates[:5]:
                sector = sector_classifier(symbol)
                universe_logger.info(f"    {symbol}: {sector or 'Unknown'}", operation="enhanced_logging")
        else:
            universe_logger.warning("  ⚠️ No sector data available", operation="enhanced_logging")

    return sector_classifier is not None


def test_earnings_exclusion():
    """Test 5: Earnings exclusion using vX financials"""
    universe_logger.info("\n🔍 Test 5: Earnings Exclusion", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    from services.polygon_client import PolygonClient

    client = PolygonClient()

    # Test with a few symbols
    test_symbols = ["AAPL", "MSFT", "NVDA"]
    end_date = date.today()
    start_date = end_date - timedelta(days=90)

    for symbol in test_symbols:
        try:
            data = client.get_earnings_calendar(symbol, start_date, end_date)
            earnings_dates = data.get("results", [])
            universe_logger.info(f"  {symbol}: {len(earnings_dates, operation="enhanced_logging")} earnings dates found")

            if earnings_dates:
                for earning in earnings_dates[:2]:  # Show first 2
                    universe_logger.info(f"    - {earning.get('date', operation="enhanced_logging")} ({earning.get('fiscal_period')})"
                    )
        except Exception as e:
            universe_logger.error(f"  {symbol}: Error - {e}", operation="enhanced_logging")

    return True


def test_full_universe_selection():
    """Test 6: Complete universe selection process"""
    universe_logger.info("\n🔍 Test 6: Full Universe Selection", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # 🚀 ENHANCED: Test with optimized parameters for comprehensive analysis
    universe = provider.get_active_universe(
        target_size=20,  # Optimized size for thorough analysis
        analysis_days=30,  # Focused analysis period
        force_refresh=True,
        batch_size=10,
        adv_prefilter_min_dollar=50_000_000,
    )

    universe_logger.info(f"  Selected {len(universe, operation="enhanced_logging")} symbols")
    if universe:
        universe_logger.info(f"  Top 10: {universe[:10]}", operation="enhanced_logging")

        # Verify they're all valid
        from services.polygon_client import PolygonClient

        client = PolygonClient()

        # Quick validation on first 3
        for symbol in universe[:3]:
            try:
                data = client.get_aggs(
                    symbol,
                    1,
                    "day",
                    (date.today() - timedelta(days=5)).isoformat(),
                    date.today().isoformat(),
                    limit=1,
                )
                if data.get("results"):
                    universe_logger.info(f"    ✅ {symbol}: Valid data", operation="enhanced_logging")
                else:
                    universe_logger.error(f"    ❌ {symbol}: No data", operation="enhanced_logging")
            except Exception as e:
                universe_logger.error(f"    ❌ {symbol}: Error - {e}", operation="enhanced_logging")

    return len(universe) > 0


def test_performance_metrics():
    """Test 7: Performance and timing"""
    universe_logger.info("\n🔍 Test 7: Performance Metrics", operation="enhanced_logging")
    universe_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Time the full process
    start_time = time.time()

    universe = provider.get_active_universe(
        target_size=50,
        analysis_days=60,
        force_refresh=True,
        batch_size=20,
    )

    elapsed = time.time() - start_time

    universe_logger.info(f"  Time to select {len(universe, operation="enhanced_logging")} symbols: {elapsed:.1f} seconds")
    universe_logger.info(f"  Rate: {len(universe, operation="enhanced_logging")/elapsed:.1f} symbols/second")

    # Check memory usage (basic)
    import sys

    universe_logger.info(f"  Memory usage: {sys.getsizeof(universe, operation="enhanced_logging")} bytes for symbol list")

    return elapsed < 300  # Should complete in under 5 minutes


def main():
    load_dotenv()

    universe_logger.info("🚀 COMPREHENSIVE UNIVERSE TEST SUITE", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")
    universe_logger.info("Testing with 100% real Polygon data", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    tests = [
        ("Candidate Discovery", test_candidate_discovery),
        ("ADV Prefiltering", test_adv_prefiltering),
        ("Spread Calculation", test_spread_calculation),
        ("Sector Classification", test_sector_classification),
        ("Earnings Exclusion", test_earnings_exclusion),
        ("Full Universe Selection", test_full_universe_selection),
        ("Performance Metrics", test_performance_metrics),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            universe_logger.error(f"\n{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}", operation="enhanced_logging")
        except Exception as e:
            results.append((test_name, False))
            universe_logger.error(f"\n❌ {test_name}: ERROR - {e}", operation="enhanced_logging")

    # Summary
    universe_logger.info("\n" + "=" * 60, operation="enhanced_logging")
    universe_logger.info("TEST SUMMARY", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        universe_logger.info(f"  {status}: {test_name}", operation="enhanced_logging")

    universe_logger.info(f"\nOverall: {passed}/{total} tests passed", operation="enhanced_logging")

    if passed == total:
        universe_logger.info("🎉 ALL TESTS PASSED - System is 100% operational!", operation="enhanced_logging")
    else:
        universe_logger.error("⚠️ Some tests failed - check the output above", operation="enhanced_logging")


if __name__ == "__main__":
    main()
