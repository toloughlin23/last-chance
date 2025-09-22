#!/usr/bin/env python3
"""
Debug Polygon API market cap access to see what's really happening.
"""

import os
import sys

from dotenv import load_dotenv

try:
    from services.polygon_client import PolygonClient
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from services.polygon_client import PolygonClient

load_dotenv()


def debug_polygon_market_cap():
    """Debug how we're accessing Polygon market cap data."""

    print("🔍 DEBUGGING POLYGON MARKET CAP ACCESS")
    print("=" * 50)

    try:
        polygon_client = PolygonClient()

        # Test 1: Check get_tickers endpoint
        print("\n📊 Test 1: get_tickers endpoint")
        print("-" * 30)

        data = polygon_client.get_tickers(market="stocks", active=True, limit=10)
        results = data.get("results", [])

        print(f"Status: {data.get('status', 'Unknown')}")
        print(f"Count: {data.get('count', 0)}")
        print(f"Results: {len(results)}")

        if results:
            print("\nFirst few tickers:")
            for i, ticker in enumerate(results[:3]):
                print(f"  {i+1}. {ticker}")
                # Check if market_cap is in the ticker data
                if "market_cap" in ticker:
                    print(f"     Market Cap: {ticker['market_cap']}")
                else:
                    print("     Market Cap: NOT IN TICKER DATA")

        # Test 2: Check get_ticker_details for specific symbols
        print("\n📊 Test 2: get_ticker_details for specific symbols")
        print("-" * 40)

        test_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "META"]

        for symbol in test_symbols:
            print(f"\n🔍 Testing {symbol}:")
            try:
                details = polygon_client.get_ticker_details(symbol)
                print(f"   Status: {details.get('status', 'Unknown')}")

                if details.get("results"):
                    result = details["results"]
                    print(f"   Market Cap: {result.get('market_cap', 'NOT FOUND')}")
                    print(f"   Name: {result.get('name', 'NOT FOUND')}")
                    print(f"   Type: {result.get('type', 'NOT FOUND')}")
                    print(f"   Market: {result.get('market', 'NOT FOUND')}")
                    print(
                        f"   Primary Exchange: {result.get('primary_exchange', 'NOT FOUND')}"
                    )
                else:
                    print("   No results found")

            except Exception as e:
                print(f"   ERROR: {e}")

        # Test 3: Check if we need different parameters
        print("\n📊 Test 3: Different get_tickers parameters")
        print("-" * 40)

        # Try with different parameters
        test_params = [
            {"market": "stocks", "active": True, "limit": 5},
            {"market": "stocks", "active": "true", "limit": 5},
            {"market": "stocks", "limit": 5},
            {"market": "stocks", "active": True, "limit": 5, "sort": "ticker"},
        ]

        for i, params in enumerate(test_params):
            print(f"\n  Test 3.{i+1}: {params}")
            try:
                data = polygon_client.get_tickers(**params)
                results = data.get("results", [])
                print(f"    Status: {data.get('status')}")
                print(f"    Count: {data.get('count')}")
                print(f"    Results: {len(results)}")

                if results and len(results) > 0:
                    first_ticker = results[0]
                    print(f"    First ticker keys: {list(first_ticker.keys())}")
                    if "market_cap" in first_ticker:
                        print(
                            f"    First ticker market_cap: {first_ticker['market_cap']}"
                        )
                    else:
                        print("    First ticker market_cap: NOT FOUND")

            except Exception as e:
                print(f"    ERROR: {e}")

        # Test 4: Check API key and permissions
        print("\n📊 Test 4: API Key and Permissions")
        print("-" * 35)

        # Check if we can access basic endpoints
        try:
            # Test a simple endpoint
            test_data = polygon_client.get_aggs(
                "AAPL", 1, "day", "2024-01-01", "2024-01-02", limit=1
            )
            print(f"   Aggs endpoint: {test_data.get('status', 'Unknown')}")
        except Exception as e:
            print(f"   Aggs endpoint ERROR: {e}")

        # Test ticker details endpoint
        try:
            test_details = polygon_client.get_ticker_details("AAPL")
            print(f"   Ticker details: {test_details.get('status', 'Unknown')}")
        except Exception as e:
            print(f"   Ticker details ERROR: {e}")

        print("\n🎯 SUMMARY:")
        print("=" * 20)
        print("The issue might be:")
        print("1. get_tickers doesn't include market_cap by default")
        print("2. We need to call get_ticker_details for each symbol")
        print("3. Some symbols might not have market_cap data")
        print("4. API key might not have access to market_cap data")

        return True

    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = debug_polygon_market_cap()
    sys.exit(0 if success else 1)
