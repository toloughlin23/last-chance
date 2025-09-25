#!/usr/bin/env python3
"""
Deep diagnosis of why we're only getting 40-45 candidates instead of 200-300.
Let's trace through the entire process step by step.
"""

import os
import sys
from datetime import date, timedelta

from dotenv import load_dotenv

try:
    from services.polygon_client import PolygonClient
    from services.quotes_client import QuotesClient
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from services.polygon_client import PolygonClient
    from services.quotes_client import QuotesClient

load_dotenv()


def deep_diagnosis():
    """Deep diagnosis of the universe selection issue."""

    universe_logger.info("🔍 DEEP DIAGNOSIS: Why Only 40-45 Candidates?", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")

    try:
        polygon_client = PolygonClient()
        quotes_client = QuotesClient()

        # STEP 1: Check how many symbols we get from get_tickers
        universe_logger.info("\n📊 STEP 1: Getting symbols from get_tickers", operation="enhanced_logging")
        universe_logger.info("-" * 40, operation="enhanced_logging")

        data = polygon_client.get_tickers(market="stocks", active=True, limit=1000)
        results = data.get("results", [])
        universe_logger.info(f"Total tickers from get_tickers: {len(results, operation="enhanced_logging")}")

        # Filter valid symbols
        valid_symbols = []
        for ticker in results:
            symbol = ticker.get("ticker")
            if (
                isinstance(symbol, str)
                and len(symbol) <= 5
                and symbol.isalpha()
                and not symbol.endswith(".U")
                and not symbol.endswith(".WS")
                and not symbol.endswith(".RT")
                and not symbol.endswith(".WT")
            ):
                valid_symbols.append(symbol)

        universe_logger.info(f"Valid symbols after filtering: {len(valid_symbols, operation="enhanced_logging")}")
        universe_logger.info(f"First 10 valid symbols: {valid_symbols[:10]}", operation="enhanced_logging")

        # STEP 2: Check market cap data availability
        universe_logger.info("\n📊 STEP 2: Market cap data availability", operation="enhanced_logging")
        universe_logger.info("-" * 40, operation="enhanced_logging")

        market_cap_available = 0
        market_cap_over_10b = 0
        market_cap_over_5b = 0
        market_cap_over_1b = 0

        # Test first 50 symbols for market cap
        test_symbols = valid_symbols[:50]

        for i, symbol in enumerate(test_symbols):
            try:
                details = polygon_client.get_ticker_details(symbol)
                if details and details.get("results"):
                    market_cap = details["results"].get("market_cap", 0)
                    if market_cap > 0:
                        market_cap_available += 1
                        if market_cap >= 1_000_000_000:
                            market_cap_over_1b += 1
                        if market_cap >= 5_000_000_000:
                            market_cap_over_5b += 1
                        if market_cap >= 10_000_000_000:
                            market_cap_over_10b += 1

                        if i < 10:  # Show first 10
                            universe_logger.info(f"  {symbol}: ${market_cap:,.0f}", operation="enhanced_logging")
            except Exception as e:
                if i < 10:
                    universe_logger.error(f"  {symbol}: ERROR - {e}", operation="enhanced_logging")

        universe_logger.info(f"\nMarket cap statistics (from {len(test_symbols, operation="enhanced_logging")} symbols):")
        universe_logger.info(f"  Symbols with market cap data: {market_cap_available}", operation="enhanced_logging")
        universe_logger.info(f"  Market cap > $1B: {market_cap_over_1b}", operation="enhanced_logging")
        universe_logger.info(f"  Market cap > $5B: {market_cap_over_5b}", operation="enhanced_logging")
        universe_logger.info(f"  Market cap > $10B: {market_cap_over_10b}", operation="enhanced_logging")

        # STEP 3: Test the quality analysis filters
        universe_logger.info("\n📊 STEP 3: Quality analysis filters", operation="enhanced_logging")
        universe_logger.info("-" * 40, operation="enhanced_logging")

        start_date = date.today() - timedelta(days=60)
        end_date = date.today()

        passed_market_cap = 0
        passed_adv = 0
        passed_spreads = 0
        passed_atr = 0
        total_passed = 0

        # Test symbols that have market cap > $10B
        large_cap_symbols = []
        for symbol in test_symbols:
            try:
                details = polygon_client.get_ticker_details(symbol)
                if details and details.get("results"):
                    market_cap = details["results"].get("market_cap", 0)
                    if market_cap >= 10_000_000_000:
                        large_cap_symbols.append(symbol)
            except Exception:
                continue

        universe_logger.info(f"Large cap symbols (>$10B, operation="enhanced_logging"): {len(large_cap_symbols)}")
        universe_logger.info(f"Testing quality filters on: {large_cap_symbols[:10]}", operation="enhanced_logging")

        for symbol in large_cap_symbols[:20]:  # Test first 20 large caps
            universe_logger.info(f"\n🔍 Testing {symbol}:", operation="enhanced_logging")

            # Test market cap (already passed)
            passed_market_cap += 1
            universe_logger.info("   ✅ Market Cap: PASS", operation="enhanced_logging")

            # Test ADV
            try:
                price_data = polygon_client.get_aggs(
                    symbol,
                    1,
                    "day",
                    start_date.isoformat(),
                    end_date.isoformat(),
                    limit=60,
                    adjusted=True,
                )

                results = price_data.get("results", [])
                if not results:
                    universe_logger.error("   ❌ ADV: No price data", operation="enhanced_logging")
                    continue

                total_volume = sum(float(r.get("v", 0)) for r in results)
                avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
                adv = total_volume * avg_price / len(results)

                universe_logger.info(f"   ADV: ${adv:,.0f}", operation="enhanced_logging")

                if adv >= 5_000_000:  # Current filter
                    passed_adv += 1
                    universe_logger.info("   ✅ ADV: PASS", operation="enhanced_logging")
                else:
                    universe_logger.error("   ❌ ADV: FAIL (< $5M, operation="enhanced_logging")")
                    continue

            except Exception as e:
                universe_logger.error(f"   ❌ ADV: ERROR - {e}", operation="enhanced_logging")
                continue

            # Test spreads
            try:
                med_dollar, med_bps = quotes_client.median_spread_over_days(
                    symbol, days=5
                )
                universe_logger.info(f"   Spread: ${med_dollar:.4f} / {med_bps:.1f} bps", operation="enhanced_logging")

                if med_dollar <= 5.0 and med_bps <= 5000:  # Current filter
                    passed_spreads += 1
                    universe_logger.info("   ✅ Spreads: PASS", operation="enhanced_logging")
                else:
                    universe_logger.error("   ❌ Spreads: FAIL (too wide, operation="enhanced_logging")")
                    continue

            except Exception as e:
                universe_logger.error(f"   ❌ Spreads: ERROR - {e}", operation="enhanced_logging")
                continue

            # Test ATR
            try:
                prices = [float(r.get("c", 0)) for r in results if r.get("c")]
                if len(prices) < 5:
                    universe_logger.error("   ❌ ATR: Not enough price data", operation="enhanced_logging")
                    continue

                # Calculate ATR%
                true_ranges = []
                for i in range(1, len(prices)):
                    high = max(prices[i], prices[i - 1])
                    low = min(prices[i], prices[i - 1])
                    true_ranges.append(high - low)

                if not true_ranges:
                    universe_logger.error("   ❌ ATR: No true ranges", operation="enhanced_logging")
                    continue

                atr = sum(true_ranges) / len(true_ranges)
                avg_price = sum(prices) / len(prices)
                atr_pct = (atr / avg_price) * 100 if avg_price > 0 else 0

                universe_logger.info(f"   ATR%: {atr_pct:.2f}%", operation="enhanced_logging")

                if 0.5 <= atr_pct <= 8.0:  # Reasonable ATR range
                    passed_atr += 1
                    universe_logger.info("   ✅ ATR: PASS", operation="enhanced_logging")
                else:
                    universe_logger.error("   ❌ ATR: FAIL (outside 0.5-8.0%, operation="enhanced_logging")")
                    continue

            except Exception as e:
                universe_logger.error(f"   ❌ ATR: ERROR - {e}", operation="enhanced_logging")
                continue

            # If we get here, symbol passed all tests
            total_passed += 1
            universe_logger.info(f"   🎯 OVERALL: PASS - {symbol} qualifies!", operation="enhanced_logging")

        # STEP 4: Summary and recommendations
        universe_logger.info("\n📊 STEP 4: SUMMARY AND DIAGNOSIS", operation="enhanced_logging")
        universe_logger.info("=" * 40, operation="enhanced_logging")

        universe_logger.info("Symbol discovery:", operation="enhanced_logging")
        universe_logger.info(f"  Total tickers from Polygon: {len(results, operation="enhanced_logging")}")
        universe_logger.info(f"  Valid symbols after filtering: {len(valid_symbols, operation="enhanced_logging")}")
        universe_logger.info(f"  Symbols with market cap data: {market_cap_available}", operation="enhanced_logging")
        universe_logger.info(f"  Large cap symbols (>$10B, operation="enhanced_logging"): {len(large_cap_symbols)}")

        universe_logger.info(f"\nQuality filtering (from {len(large_cap_symbols[:20], operation="enhanced_logging")} large caps tested):"
        )
        universe_logger.info(f"  Passed Market Cap: {passed_market_cap}", operation="enhanced_logging")
        universe_logger.info(f"  Passed ADV: {passed_adv}", operation="enhanced_logging")
        universe_logger.info(f"  Passed Spreads: {passed_spreads}", operation="enhanced_logging")
        universe_logger.info(f"  Passed ATR: {passed_atr}", operation="enhanced_logging")
        universe_logger.info(f"  Total Passed: {total_passed}", operation="enhanced_logging")

        # DIAGNOSIS
        universe_logger.info("\n🎯 DIAGNOSIS:", operation="enhanced_logging")
        universe_logger.info("=" * 20, operation="enhanced_logging")

        if total_passed < 10:
            universe_logger.error("❌ PROBLEM IDENTIFIED: Quality filters are too strict!", operation="enhanced_logging")
            universe_logger.info("   The filters are eliminating too many good symbols.", operation="enhanced_logging")
            universe_logger.info("   Recommendations:", operation="enhanced_logging")
            universe_logger.info("   1. Relax ADV filter (currently $5M minimum, operation="enhanced_logging")")
            universe_logger.info("   2. Relax spread filter (currently 50 bps maximum, operation="enhanced_logging")")
            universe_logger.info("   3. Relax ATR filter (currently 0.5-8.0% range, operation="enhanced_logging")")
            universe_logger.info("   4. Provider should be generous, selector should be strict", operation="enhanced_logging")
        else:
            universe_logger.info("✅ Quality filters seem reasonable", operation="enhanced_logging")
            universe_logger.info("   The issue might be in the batch processing or API limits", operation="enhanced_logging")

        return True

    except Exception as e:
        universe_logger.error(f"❌ Deep diagnosis failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = deep_diagnosis()
    sys.exit(0 if success else 1)
