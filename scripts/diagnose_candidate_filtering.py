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

    training_logger.info("🔍 DIAGNOSING CANDIDATE FILTERING", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    try:
        polygon_client = PolygonClient()
        quotes_client = QuotesClient()

        # Get some S&P 500 symbols
        training_logger.info("📊 Getting S&P 500 symbols...", operation="enhanced_logging")
        data = polygon_client.get_tickers(market="stocks", active=True, limit=100)
        results = data.get("results", [])

        if not results:
            training_logger.error("❌ No symbols found", operation="enhanced_logging")
            return

        symbols = [
            ticker.get("ticker")
            for ticker in results
            if isinstance(ticker.get("ticker"), str)
        ]
        training_logger.info(f"✅ Found {len(symbols, operation="enhanced_logging")} symbols: {symbols[:10]}")

        # Test a few symbols to see what's filtering them out
        test_symbols = symbols[:20]  # Test first 20

        training_logger.info(f"\n🔍 Testing {len(test_symbols, operation="enhanced_logging")} symbols...")

        start_date = date.today() - timedelta(days=60)
        end_date = date.today()

        passed_market_cap = 0
        passed_adv = 0
        passed_spreads = 0
        passed_atr = 0
        total_passed = 0

        for i, symbol in enumerate(test_symbols):
            training_logger.info(f"\n📈 Testing {symbol} ({i+1}/{len(test_symbols, operation="enhanced_logging")})...")

            # Test market cap
            try:
                details = polygon_client.get_ticker_details(symbol)
                market_cap = details.get("results", {}).get("market_cap", 0)
                training_logger.info(f"   Market Cap: ${market_cap:,.0f}", operation="enhanced_logging")

                if market_cap >= 10_000_000_000:
                    passed_market_cap += 1
                    training_logger.info("   ✅ Market Cap: PASS", operation="enhanced_logging")
                else:
                    training_logger.error("   ❌ Market Cap: FAIL (< $10B, operation="enhanced_logging")")
                    continue

            except Exception as e:
                training_logger.error(f"   ❌ Market Cap: ERROR - {e}", operation="enhanced_logging")
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
                    training_logger.error("   ❌ ADV: No price data", operation="enhanced_logging")
                    continue

                total_volume = sum(float(r.get("v", 0)) for r in results)
                avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
                adv = total_volume * avg_price / len(results)

                training_logger.info(f"   ADV: ${adv:,.0f}", operation="enhanced_logging")

                if adv >= 5_000_000:
                    passed_adv += 1
                    training_logger.info("   ✅ ADV: PASS", operation="enhanced_logging")
                else:
                    training_logger.error("   ❌ ADV: FAIL (< $5M, operation="enhanced_logging")")
                    continue

            except Exception as e:
                training_logger.error(f"   ❌ ADV: ERROR - {e}", operation="enhanced_logging")
                continue

            # Test spreads
            try:
                med_dollar, med_bps = quotes_client.median_spread_over_days(
                    symbol, days=5
                )
                training_logger.info(f"   Spread: ${med_dollar:.4f} / {med_bps:.1f} bps", operation="enhanced_logging")

                if med_dollar <= 5.0 and med_bps <= 5000:
                    passed_spreads += 1
                    training_logger.info("   ✅ Spreads: PASS", operation="enhanced_logging")
                else:
                    training_logger.error("   ❌ Spreads: FAIL (too wide, operation="enhanced_logging")")
                    continue

            except Exception as e:
                training_logger.error(f"   ❌ Spreads: ERROR - {e}", operation="enhanced_logging")
                continue

            # Test ATR
            try:
                prices = [float(r.get("c", 0)) for r in results if r.get("c")]
                if len(prices) < 5:
                    training_logger.error("   ❌ ATR: Not enough price data", operation="enhanced_logging")
                    continue

                # Calculate ATR%
                true_ranges = []
                for i in range(1, len(prices)):
                    high = max(prices[i], prices[i - 1])
                    low = min(prices[i], prices[i - 1])
                    true_ranges.append(high - low)

                if not true_ranges:
                    training_logger.error("   ❌ ATR: No true ranges", operation="enhanced_logging")
                    continue

                atr = sum(true_ranges) / len(true_ranges)
                avg_price = sum(prices) / len(prices)
                atr_pct = (atr / avg_price) * 100 if avg_price > 0 else 0

                training_logger.info(f"   ATR%: {atr_pct:.2f}%", operation="enhanced_logging")

                if 0.5 <= atr_pct <= 8.0:  # Reasonable ATR range
                    passed_atr += 1
                    training_logger.info("   ✅ ATR: PASS", operation="enhanced_logging")
                else:
                    training_logger.error("   ❌ ATR: FAIL (outside 0.5-8.0%, operation="enhanced_logging")")
                    continue

            except Exception as e:
                training_logger.error(f"   ❌ ATR: ERROR - {e}", operation="enhanced_logging")
                continue

            # If we get here, symbol passed all tests
            total_passed += 1
            training_logger.info(f"   🎯 OVERALL: PASS - {symbol} qualifies!", operation="enhanced_logging")

        # Summary
        training_logger.info("\n📊 FILTERING SUMMARY:", operation="enhanced_logging")
        training_logger.info("=" * 30, operation="enhanced_logging")
        training_logger.info(f"Total tested:     {len(test_symbols, operation="enhanced_logging")}")
        training_logger.info(f"Passed Market Cap: {passed_market_cap}", operation="enhanced_logging")
        training_logger.info(f"Passed ADV:        {passed_adv}", operation="enhanced_logging")
        training_logger.info(f"Passed Spreads:    {passed_spreads}", operation="enhanced_logging")
        training_logger.info(f"Passed ATR:        {passed_atr}", operation="enhanced_logging")
        training_logger.info(f"Total Passed:      {total_passed}", operation="enhanced_logging")

        if total_passed < 10:
            training_logger.warning(f"\n⚠️ WARNING: Only {total_passed} symbols passed all filters!", operation="enhanced_logging")
            training_logger.info("   This suggests the filters are too strict.", operation="enhanced_logging")
        else:
            training_logger.info(f"\n✅ SUCCESS: {total_passed} symbols passed all filters!", operation="enhanced_logging")

        return True

    except Exception as e:
        training_logger.error(f"❌ Diagnosis failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = diagnose_filtering()
    sys.exit(0 if success else 1)
