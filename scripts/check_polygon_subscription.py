#!/usr/bin/env python3
"""Check which Polygon endpoints are available with current subscription"""


from dotenv import load_dotenv

from services.polygon_client import PolygonClient


def test_endpoint(client, name, test_func):
    print(f"\n{name}:")
    try:
        result = test_func()
        if isinstance(result, dict):
            status = result.get("status", "No status")
            if status == "OK":
                print(f"  ✅ Available (status: {status})")
                if "results" in result:
                    print(f"     Results: {len(result.get('results', []))}")
            else:
                print(f"  ❌ Error: {status}")
                if "error" in result:
                    print(f"     {result['error']}")
        else:
            print("  ✅ Available")
    except Exception as e:
        print(f"  ❌ Not available: {e}")


def main():
    load_dotenv()

    print("Checking Polygon Premium Subscription Features")
    print("=" * 50)

    client = PolygonClient()

    # Test various endpoints
    test_endpoint(
        client,
        "1. Daily Aggregates (Bars)",
        lambda: client.get_aggs("AAPL", 1, "day", "2025-09-15", "2025-09-20"),
    )

    test_endpoint(
        client,
        "2. Active Tickers List",
        lambda: client.get_tickers(market="stocks", active=True, limit=5),
    )

    test_endpoint(
        client,
        "3. Earnings Calendar (Benzinga)",
        lambda: client.get_earnings_calendar(
            "AAPL", date(2025, 9, 1), date(2025, 9, 30)
        ),
    )

    # Test news endpoint if available
    print("\n4. News API:")
    try:
        # Try the news endpoint
        import requests

        url = "https://api.polygon.io/v2/reference/news"
        params = {"apiKey": client.api_key, "ticker": "AAPL", "limit": 1}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            print("  ✅ News API available")
        else:
            print(f"  ❌ News API status: {resp.status_code}")
    except Exception as e:
        print(f"  ❌ News API error: {e}")

    # Check ticker details endpoint
    print("\n5. Ticker Details (with market cap):")
    try:
        url = "https://api.polygon.io/v3/reference/tickers/AAPL"
        params = {"apiKey": client.api_key}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", {})
            print("  ✅ Ticker details available")
            print(f"     Market cap field: {'market_cap' in results}")
            if "market_cap" in results:
                print(f"     Market cap: ${results['market_cap']:,.0f}")
        else:
            print(f"  ❌ Status: {resp.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")

    # Check financials endpoint
    print("\n6. Financials/Fundamentals:")
    try:
        url = "https://api.polygon.io/vX/reference/financials"
        params = {"apiKey": client.api_key, "ticker": "AAPL", "limit": 1}
        resp = requests.get(url, params=params)
        print(f"  Status code: {resp.status_code}")
        if resp.status_code == 404:
            print("  ℹ️  Financials might be under different endpoint")
    except Exception as e:
        print(f"  ❌ Error: {e}")


if __name__ == "__main__":
    from datetime import date

    main()
