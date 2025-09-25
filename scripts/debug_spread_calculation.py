#!/usr/bin/env python3
"""Debug why spread calculation is still failing"""

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from services.quotes_client import QuotesClient


def main():
    load_dotenv()

    client = QuotesClient()

    # Test the median_spread_over_days method step by step
    symbol = "AAPL"
    days = 5
    core_hours_only = True

    training_logger.info(f"Debugging median_spread_over_days for {symbol}", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    end = datetime.now(timezone.utc)
    medians = []

    for i in range(1, days + 1):
        day_end = end - timedelta(days=i - 1)
        day_start = day_end.replace(hour=0, minute=0, second=0, microsecond=0)

        # Skip weekends
        if day_start.weekday() >= 5:
            training_logger.info(f"\nDay {i}: {day_start.date(, operation="enhanced_logging")} - WEEKEND (skipped)")
            continue

        if core_hours_only:
            start_utc = day_start.replace(hour=13, minute=30)
            end_utc = day_start.replace(hour=20, minute=0)
        else:
            start_utc = day_start
            end_utc = day_start.replace(hour=23, minute=59, second=59)

        training_logger.info(f"\nDay {i}: {day_start.date(, operation="enhanced_logging")}")
        training_logger.info(f"  Window: {start_utc} to {end_utc}", operation="enhanced_logging")

        quotes = client.fetch_quotes_window(symbol, start_utc, end_utc, limit=1000)
        training_logger.info(f"  Quotes fetched: {len(quotes, operation="enhanced_logging")}")

        if quotes:
            # Check the structure
            training_logger.info(f"  First quote keys: {list(quotes[0].keys(, operation="enhanced_logging"))}")

            # Show a few quotes
            for j, q in enumerate(quotes[:3]):
                bid = q.get("bid_price", "N/A")
                ask = q.get("ask_price", "N/A")
                training_logger.info(f"    Quote {j+1}: bid={bid}, ask={ask}", operation="enhanced_logging")

        day_median = client.compute_median_spreads(quotes)
        medians.append(day_median)
        training_logger.info(f"  Day median: ${day_median[0]:.3f} ({day_median[1]:.1f} bps, operation="enhanced_logging")")

    # Compute final median
    if medians:
        dollar = sorted([m[0] for m in medians])
        bps = sorted([m[1] for m in medians])
        final_dollar = dollar[len(dollar) // 2]
        final_bps = bps[len(bps) // 2]

        training_logger.info(f"\nFinal 5-day median: ${final_dollar:.3f} ({final_bps:.1f} bps, operation="enhanced_logging")")

        if final_dollar > 1000:
            training_logger.warning("\n⚠️ Problem: Still getting unrealistic spreads!", operation="enhanced_logging")
            training_logger.info("   This happens when some days have no valid quotes", operation="enhanced_logging")
            training_logger.info("   Check if we're hitting weekends or holidays", operation="enhanced_logging")


if __name__ == "__main__":
    main()
