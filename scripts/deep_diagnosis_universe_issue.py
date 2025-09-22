#!/usr/bin/env python3
"""
Deep diagnosis of why we're only getting 40-45 candidates instead of 200-300.
Let's trace through the entire process step by step.
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv

load_dotenv()

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient


def deep_diagnosis():
    """Deep diagnosis of the universe selection issue."""

    print("🔍 DEEP DIAGNOSIS: Why Only 40-45 Candidates?")
    print("=" * 60)

    try:
        polygon_client = PolygonClient()
        quotes_client = QuotesClient()

        # STEP 1: Check how many symbols we get from get_tickers
        print("\n📊 STEP 1: Getting symbols from get_tickers")
        print("-" * 40)

        data = polygon_client.get_tickers(market="stocks", active=True, limit=1000)
        results = data.get("results", [])
        print(f"Total tickers from get_tickers: {len(results)}")

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

        print(f"Valid symbols after filtering: {len(valid_symbols)}")
        print(f"First 10 valid symbols: {valid_symbols[:10]}")

        # STEP 2: Check market cap data availability
        print("\n📊 STEP 2: Market cap data availability")
        print("-" * 40)

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
                            print(f"  {symbol}: ${market_cap:,.0f}")
            except Exception as e:
                if i < 10:
                    print(f"  {symbol}: ERROR - {e}")

        print(f"\nMarket cap statistics (from {len(test_symbols)} symbols):")
        print(f"  Symbols with market cap data: {market_cap_available}")
        print(f"  Market cap > $1B: {market_cap_over_1b}")
        print(f"  Market cap > $5B: {market_cap_over_5b}")
        print(f"  Market cap > $10B: {market_cap_over_10b}")

        # STEP 3: Test the quality analysis filters
        print("\n📊 STEP 3: Quality analysis filters")
        print("-" * 40)

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

        print(f"Large cap symbols (>$10B): {len(large_cap_symbols)}")
        print(f"Testing quality filters on: {large_cap_symbols[:10]}")

        for symbol in large_cap_symbols[:20]:  # Test first 20 large caps
            print(f"\n🔍 Testing {symbol}:")

            # Test market cap (already passed)
            passed_market_cap += 1
            print("   ✅ Market Cap: PASS")

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
                    print("   ❌ ADV: No price data")
                    continue

                total_volume = sum(float(r.get("v", 0)) for r in results)
                avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
                adv = total_volume * avg_price / len(results)

                print(f"   ADV: ${adv:,.0f}")

                if adv >= 5_000_000:  # Current filter
                    passed_adv += 1
                    print("   ✅ ADV: PASS")
                else:
                    print("   ❌ ADV: FAIL (< $5M)")
                    continue

            except Exception as e:
                print(f"   ❌ ADV: ERROR - {e}")
                continue

            # Test spreads
            try:
                med_dollar, med_bps = quotes_client.median_spread_over_days(
                    symbol, days=5
                )
                print(f"   Spread: ${med_dollar:.4f} / {med_bps:.1f} bps")

                if med_dollar <= 5.0 and med_bps <= 5000:  # Current filter
                    passed_spreads += 1
                    print("   ✅ Spreads: PASS")
                else:
                    print("   ❌ Spreads: FAIL (too wide)")
                    continue

            except Exception as e:
                print(f"   ❌ Spreads: ERROR - {e}")
                continue

            # Test ATR
            try:
                prices = [float(r.get("c", 0)) for r in results if r.get("c")]
                if len(prices) < 5:
                    print("   ❌ ATR: Not enough price data")
                    continue

                # Calculate ATR%
                true_ranges = []
                for i in range(1, len(prices)):
                    high = max(prices[i], prices[i - 1])
                    low = min(prices[i], prices[i - 1])
                    true_ranges.append(high - low)

                if not true_ranges:
                    print("   ❌ ATR: No true ranges")
                    continue

                atr = sum(true_ranges) / len(true_ranges)
                avg_price = sum(prices) / len(prices)
                atr_pct = (atr / avg_price) * 100 if avg_price > 0 else 0

                print(f"   ATR%: {atr_pct:.2f}%")

                if 0.5 <= atr_pct <= 8.0:  # Reasonable ATR range
                    passed_atr += 1
                    print("   ✅ ATR: PASS")
                else:
                    print("   ❌ ATR: FAIL (outside 0.5-8.0%)")
                    continue

            except Exception as e:
                print(f"   ❌ ATR: ERROR - {e}")
                continue

            # If we get here, symbol passed all tests
            total_passed += 1
            print(f"   🎯 OVERALL: PASS - {symbol} qualifies!")

        # STEP 4: Summary and recommendations
        print("\n📊 STEP 4: SUMMARY AND DIAGNOSIS")
        print("=" * 40)

        print("Symbol discovery:")
        print(f"  Total tickers from Polygon: {len(results)}")
        print(f"  Valid symbols after filtering: {len(valid_symbols)}")
        print(f"  Symbols with market cap data: {market_cap_available}")
        print(f"  Large cap symbols (>$10B): {len(large_cap_symbols)}")

        print(
            f"\nQuality filtering (from {len(large_cap_symbols[:20])} large caps tested):"
        )
        print(f"  Passed Market Cap: {passed_market_cap}")
        print(f"  Passed ADV: {passed_adv}")
        print(f"  Passed Spreads: {passed_spreads}")
        print(f"  Passed ATR: {passed_atr}")
        print(f"  Total Passed: {total_passed}")

        # DIAGNOSIS
        print("\n🎯 DIAGNOSIS:")
        print("=" * 20)

        if total_passed < 10:
            print("❌ PROBLEM IDENTIFIED: Quality filters are too strict!")
            print("   The filters are eliminating too many good symbols.")
            print("   Recommendations:")
            print("   1. Relax ADV filter (currently $5M minimum)")
            print("   2. Relax spread filter (currently 50 bps maximum)")
            print("   3. Relax ATR filter (currently 0.5-8.0% range)")
            print("   4. Provider should be generous, selector should be strict")
        else:
            print("✅ Quality filters seem reasonable")
            print("   The issue might be in the batch processing or API limits")

        return True

    except Exception as e:
        print(f"❌ Deep diagnosis failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = deep_diagnosis()
    sys.exit(0 if success else 1)
