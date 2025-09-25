#!/usr/bin/env python3
"""
Edge Case Testing for Universe Provider & Selector
Tests error handling, rate limits, and edge cases
"""

import time
from datetime import date, timedelta

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector


def test_empty_candidates():
    """Test: What happens with empty candidate list"""
    training_logger.info("🔍 Edge Case 1: Empty Candidates", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    selector = UniverseSelector()

    # Test with empty list
    result = selector.select_universe(
        candidates=[],
        target_size=10,
        analysis_days=30,
    )

    training_logger.info(f"  Empty candidates → {len(result, operation="enhanced_logging")} symbols selected")
    return len(result) == 0


def test_insufficient_candidates():
    """Test: What happens when candidates < target_size"""
    training_logger.warning("\n🔍 Edge Case 2: Insufficient Candidates", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    selector = UniverseSelector()

    # Test with only 3 candidates but target of 10
    result = selector.select_universe(
        candidates=["AAPL", "MSFT", "NVDA"],
        target_size=10,
        analysis_days=30,
    )

    training_logger.info(f"  3 candidates, target 10 → {len(result, operation="enhanced_logging")} symbols selected")
    return len(result) == 3


def test_all_candidates_filtered_out():
    """Test: What happens when all candidates fail filters"""
    training_logger.info("\n🔍 Edge Case 3: All Candidates Filtered Out", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    selector = UniverseSelector()

    # Use very strict filters to eliminate everything
    result = selector.select_universe(
        candidates=["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"],
        target_size=10,
        analysis_days=30,
        min_adv_dollars=1_000_000_000_000,  # $1T ADV (impossible)
        min_price=10000,  # $10k price (impossible)
        min_atr_pct=50,  # 50% ATR (impossible)
        max_spread_dollars=0.001,  # 0.1 cent spread (impossible)
    )

    training_logger.info(f"  Impossible filters → {len(result, operation="enhanced_logging")} symbols selected")
    return len(result) == 0


def test_weekend_data():
    """Test: Behavior on weekends when markets are closed"""
    training_logger.info("\n🔍 Edge Case 4: Weekend Data Handling", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    from services.quotes_client import QuotesClient

    client = QuotesClient()

    # Test spread calculation on weekend
    today = date.today()
    weekend_days = []

    # Find a recent weekend
    for i in range(7):
        test_date = today - timedelta(days=i)
        if test_date.weekday() >= 5:  # Saturday or Sunday
            weekend_days.append(test_date)

    if weekend_days:
        test_date = weekend_days[0]
        training_logger.info(f"  Testing weekend data for {test_date}", operation="enhanced_logging")

        try:
            med_dollar, med_bps = client.median_spread_over_days(
                "AAPL", days=1, end_date=test_date
            )
            training_logger.info(f"    Weekend spread: ${med_dollar:.3f} ({med_bps:.1f} bps, operation="enhanced_logging")")

            # Should handle gracefully (not crash)
            return True
        except Exception as e:
            training_logger.error(f"    Weekend error: {e}", operation="enhanced_logging")
            return False
    else:
        training_logger.info("  No recent weekend found for comprehensive analysis", operation="enhanced_logging")
        return True


def test_api_rate_limits():
    """Test: Behavior under API rate limiting"""
    training_logger.info("\n🔍 Edge Case 5: API Rate Limiting", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Test with very large batch to potentially hit rate limits
    start_time = time.time()

    try:
        universe = provider.get_active_universe(
            target_size=200,  # Large target
            analysis_days=60,
            force_refresh=True,
            batch_size=50,  # Large batches
        )

        elapsed = time.time() - start_time
        training_logger.info(f"  Large batch completed in {elapsed:.1f}s", operation="enhanced_logging")
        training_logger.info(f"  Selected {len(universe, operation="enhanced_logging")} symbols")

        # Check if we got reasonable results despite potential rate limits
        return len(universe) > 0

    except Exception as e:
        training_logger.error(f"  Rate limit error: {e}", operation="enhanced_logging")
        return False


def test_missing_polygon_key():
    """Test: Behavior without POLYGON_API_KEY"""
    training_logger.info("\n🔍 Edge Case 6: Missing API Key", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    import os

    original_key = os.environ.get("POLYGON_API_KEY")

    try:
        # Temporarily remove the key
        if "POLYGON_API_KEY" in os.environ:
            del os.environ["POLYGON_API_KEY"]

        provider = ActiveUniverseProvider()

        # This should fail gracefully
        universe = provider.get_active_universe(
            target_size=10,
            analysis_days=30,
            force_refresh=True,
        )

        training_logger.info(f"  No API key → {len(universe, operation="enhanced_logging")} symbols (should be 0)")
        return len(universe) == 0

    except Exception as e:
        training_logger.error(f"  Expected error without API key: {e}", operation="enhanced_logging")
        return True
    finally:
        # Restore the key
        if original_key:
            os.environ["POLYGON_API_KEY"] = original_key


def test_invalid_symbols():
    """Test: Behavior with invalid/non-existent symbols"""
    training_logger.info("\n🔍 Edge Case 7: Invalid Symbols", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    selector = UniverseSelector()

    # Mix of valid and invalid symbols
    mixed_candidates = ["AAPL", "INVALID123", "MSFT", "FAKESYMBOL", "NVDA"]

    result = selector.select_universe(
        candidates=mixed_candidates,
        target_size=10,
        analysis_days=30,
    )

    training_logger.info(f"  Mixed valid/invalid → {len(result, operation="enhanced_logging")} symbols selected")
    training_logger.info(f"  Selected: {result}", operation="enhanced_logging")

    # Should only return valid symbols
    valid_symbols = ["AAPL", "MSFT", "NVDA"]
    return all(symbol in valid_symbols for symbol in result)


def test_extreme_parameters():
    """Test: Behavior with extreme parameter values"""
    training_logger.info("\n🔍 Edge Case 8: Extreme Parameters", operation="enhanced_logging")
    training_logger.info("-" * 40, operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Test with extreme values
    try:
        universe = provider.get_active_universe(
            target_size=1,  # Very small target
            analysis_days=1,  # Very short analysis
            force_refresh=True,
            batch_size=1,  # Very small batch
        )

        training_logger.info(f"  Extreme params → {len(universe, operation="enhanced_logging")} symbols")
        return True

    except Exception as e:
        training_logger.error(f"  Extreme params error: {e}", operation="enhanced_logging")
        return False


def main():
    load_dotenv()

    training_logger.info("🚀 EDGE CASE TEST SUITE", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    training_logger.error("Testing error handling and edge cases", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    tests = [
        ("Empty Candidates", test_empty_candidates),
        ("Insufficient Candidates", test_insufficient_candidates),
        ("All Filtered Out", test_all_candidates_filtered_out),
        ("Weekend Data", test_weekend_data),
        ("API Rate Limits", test_api_rate_limits),
        ("Missing API Key", test_missing_polygon_key),
        ("Invalid Symbols", test_invalid_symbols),
        ("Extreme Parameters", test_extreme_parameters),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            training_logger.error(f"\n{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}", operation="enhanced_logging")
        except Exception as e:
            results.append((test_name, False))
            training_logger.error(f"\n❌ {test_name}: ERROR - {e}", operation="enhanced_logging")

    # Summary
    training_logger.info("\n" + "=" * 60, operation="enhanced_logging")
    training_logger.info("EDGE CASE SUMMARY", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        training_logger.info(f"  {status}: {test_name}", operation="enhanced_logging")

    training_logger.info(f"\nOverall: {passed}/{total} edge cases handled correctly", operation="enhanced_logging")

    if passed == total:
        training_logger.info("🎉 ALL EDGE CASES HANDLED - System is robust!", operation="enhanced_logging")
    else:
        training_logger.warning("⚠️ Some edge cases need attention", operation="enhanced_logging")


if __name__ == "__main__":
    main()
