#!/usr/bin/env python3
"""Test if quotes API is working correctly"""

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from services.quotes_client import QuotesClient


def main():
    load_dotenv()

    print("Testing Quotes API")
    print("=" * 60)

    client = QuotesClient()

    # Test fetching quotes for AAPL
    symbol = "AAPL"

    # Try different time windows
    end = datetime.now(timezone.utc)

    print(f"\n1. Testing quotes for {symbol}:")

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

    print(f"   Fetching quotes from {start_time} to {end_time}")

    quotes = client.fetch_quotes_window(symbol, start_time, end_time, limit=100)
    print(f"   Received {len(quotes)} quotes")

    if quotes:
        # Show first few quotes
        print("\n   First 3 quotes:")
        for i, q in enumerate(quotes[:3]):
            bid = q.get("bidPrice") or q.get("bp") or "N/A"
            ask = q.get("askPrice") or q.get("ap") or "N/A"
            print(f"   {i+1}. Bid: {bid}, Ask: {ask}")

        # Compute spreads
        med_dollar, med_bps = client.compute_median_spreads(quotes)
        print(f"\n   Median spread: ${med_dollar:.3f} ({med_bps:.1f} bps)")
    else:
        print("   ❌ No quotes received!")

    # Test 2: Use the median_spread_over_days method
    print(f"\n2. Testing median_spread_over_days for {symbol}:")
    try:
        med_dollar, med_bps = client.median_spread_over_days(
            symbol, days=5, core_hours_only=True
        )
        print(f"   5-day median spread: ${med_dollar:.3f} ({med_bps:.1f} bps)")

        if med_dollar > 1000:
            print("   ⚠️ WARNING: Spread calculation returning unrealistic values!")
            print("   This is causing universe selection to fail!")
    except Exception as e:
        print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    main()
