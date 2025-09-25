#!/usr/bin/env python3
"""Test if quotes API is working correctly"""

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from services.quotes_client import QuotesClient


def main():
    load_dotenv()

    training_logger.info("Testing Quotes API", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    client = QuotesClient()

    # Test fetching quotes for AAPL
    symbol = "AAPL"

    # Try different time windows
    end = datetime.now(timezone.utc)

    training_logger.info(f"\n1. Testing quotes for {symbol}:", operation="enhanced_logging")

    # Test 1: Last trading day during market hours
    # Go back to a weekday
    days_back = 1
    while (end - timedelta(days=days_back)).weekday() >= 5:  # Skip weekends
        days_back += 1

    test_date = end - timedelta(days=days_back)
    start_time = test_date.replace(
        hour=14, minute=30, second=0, microsecond=0
    )  # 9:30 AM ET
    end_time = test_date.replace(
        hour=21, minute=0, second=0, microsecond=0
    )  # 4:00 PM ET

    training_logger.info(f"   Fetching quotes from {start_time} to {end_time}", operation="enhanced_logging")

    quotes = client.fetch_quotes_window(symbol, start_time, end_time, limit=100)
    training_logger.info(f"   Received {len(quotes, operation="enhanced_logging")} quotes")

    if quotes:
        # Show first few quotes
        training_logger.info("\n   First 3 quotes:", operation="enhanced_logging")
        for i, q in enumerate(quotes[:3]):
            bid = q.get("bidPrice") or q.get("bp") or "N/A"
            ask = q.get("askPrice") or q.get("ap") or "N/A"
            training_logger.info(f"   {i+1}. Bid: {bid}, Ask: {ask}", operation="enhanced_logging")

        # Compute spreads
        med_dollar, med_bps = client.compute_median_spreads(quotes)
        training_logger.info(f"\n   Median spread: ${med_dollar:.3f} ({med_bps:.1f} bps, operation="enhanced_logging")")
    else:
        training_logger.error("   ❌ No quotes received!", operation="enhanced_logging")

    # Test 2: Use the median_spread_over_days method
    training_logger.info(f"\n2. Testing median_spread_over_days for {symbol}:", operation="enhanced_logging")
    try:
        med_dollar, med_bps = client.median_spread_over_days(
            symbol, days=5, core_hours_only=True
        )
        training_logger.info(f"   5-day median spread: ${med_dollar:.3f} ({med_bps:.1f} bps, operation="enhanced_logging")")

        if med_dollar > 1000:
            training_logger.warning("   ⚠️ WARNING: Spread calculation returning unrealistic values!", operation="enhanced_logging")
            training_logger.info("   This is causing universe selection to fail!", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"   ❌ Error: {e}", operation="enhanced_logging")


if __name__ == "__main__":
    main()
