#!/usr/bin/env python3
"""
Diagnose why we're only getting 45 candidates instead of 200-300.
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


def diagnose_filtering():
    """Diagnose what's filtering out candidates."""

    print("🔍 DIAGNOSING CANDIDATE FILTERING")
    print("=" * 50)

    try:
        polygon_client = PolygonClient()
        quotes_client = QuotesClient()

        # Get some S&P 500 symbols
        print("📊 Getting S&P 500 symbols...")
        data = polygon_client.get_tickers(market="stocks", active=True, limit=100)
        results = data.get("results", [])

        if not results:
            print("❌ No symbols found")
            return

        symbols = [
            ticker.get("ticker")
            for ticker in results
            if isinstance(ticker.get("ticker"), str)
        ]
        print(f"✅ Found {len(symbols)} symbols: {symbols[:10]}")

        # Test a few symbols to see what's filtering them out
        test_symbols = symbols[:20]  # Test first 20

        print(f"\n🔍 Testing {len(test_symbols)} symbols...")

        start_date = date.today() - timedelta(days=60)
        end_date = date.today()

        passed_market_cap = 0
        passed_adv = 0
        passed_spreads = 0
        passed_atr = 0
        total_passed = 0

        for i, symbol in enumerate(test_symbols):
            print(f"\n📈 Testing {symbol} ({i+1}/{len(test_symbols)})...")

            # Test market cap
            try:
                details = polygon_client.get_ticker_details(symbol)
                market_cap = details.get("results", {}).get("market_cap", 0)
                print(f"   Market Cap: ${market_cap:,.0f}")

                if market_cap >= 10_000_000_000:
                    passed_market_cap += 1
                    print("   ✅ Market Cap: PASS")
                else:
                    print("   ❌ Market Cap: FAIL (< $10B)")
                    continue

            except Exception as e:
                print(f"   ❌ Market Cap: ERROR - {e}")
                continue

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

                if adv >= 5_000_000:
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

                if med_dollar <= 5.0 and med_bps <= 5000:
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

        # Summary
        print("\n📊 FILTERING SUMMARY:")
        print("=" * 30)
        print(f"Total tested:     {len(test_symbols)}")
        print(f"Passed Market Cap: {passed_market_cap}")
        print(f"Passed ADV:        {passed_adv}")
        print(f"Passed Spreads:    {passed_spreads}")
        print(f"Passed ATR:        {passed_atr}")
        print(f"Total Passed:      {total_passed}")

        if total_passed < 10:
            print(f"\n⚠️ WARNING: Only {total_passed} symbols passed all filters!")
            print("   This suggests the filters are too strict.")
        else:
            print(f"\n✅ SUCCESS: {total_passed} symbols passed all filters!")

        return True

    except Exception as e:
        print(f"❌ Diagnosis failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = diagnose_filtering()
    sys.exit(0 if success else 1)
