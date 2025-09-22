#!/usr/bin/env python3
"""Test if earnings calendar is working with the vX update"""

from datetime import date, timedelta

from dotenv import load_dotenv

from services.polygon_client import PolygonClient


def main():
    load_dotenv()

    print("Testing Current Earnings Implementation")
    print("=" * 50)

    client = PolygonClient()

    # Test with a few symbols
    symbols = ["AAPL", "MSFT", "GOOGL"]
    end_date = date.today()
    start_date = end_date - timedelta(days=90)  # Last 3 months

    for symbol in symbols:
        print(f"\n{symbol}:")
        try:
            data = client.get_earnings_calendar(symbol, start_date, end_date)

            if data.get("results"):
                print(f"  ✅ Found {len(data['results'])} earnings dates")
                for earning in data["results"][:3]:  # Show first 3
                    print(
                        f"     - {earning.get('date')} ({earning.get('fiscal_period')} {earning.get('fiscal_year')})"
                    )
            else:
                print("  ❌ No earnings data found")

        except Exception as e:
            print(f"  ❌ Error: {e}")

    # Test the full integration
    print("\n\nTesting Full Universe Selection with Earnings:")
    print("-" * 50)

    from utils.active_universe_provider import ActiveUniverseProvider

    provider = ActiveUniverseProvider()

    # Just test if it runs without errors
    try:
        # Small test - just check if the system identifies earnings capability
        test = provider.get_active_universe(
            target_size=5,  # Small for quick test
            analysis_days=30,
            force_refresh=True,
            batch_size=5,
        )
        print("✅ Universe selection completed successfully")
        print(f"   Selected {len(test)} symbols: {test}")
    except Exception as e:
        print(f"❌ Error in universe selection: {e}")


if __name__ == "__main__":
    main()
