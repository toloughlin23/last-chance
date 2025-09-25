#!/usr/bin/env python3
"""Check which Polygon endpoints are available with current subscription"""


from dotenv import load_dotenv

from services.polygon_client import PolygonClient


def test_endpoint(client, name, test_func):
    polygon_logger.info(f"\n{name}:", operation="enhanced_logging")
    try:
        result = test_func()
        if isinstance(result, dict):
            status = result.get("status", "No status")
            if status == "OK":
                polygon_logger.info(f"  ✅ Available (status: {status}, operation="enhanced_logging")")
                if "results" in result:
                    polygon_logger.info(f"     Results: {len(result.get('results', [], operation="enhanced_logging"))}")
            else:
                polygon_logger.error(f"  ❌ Error: {status}", operation="enhanced_logging")
                if "error" in result:
                    polygon_logger.error(f"     {result['error']}", operation="enhanced_logging")
        else:
            polygon_logger.info("  ✅ Available", operation="enhanced_logging")
    except Exception as e:
        polygon_logger.error(f"  ❌ Not available: {e}", operation="enhanced_logging")


def main():
    load_dotenv()

    polygon_logger.info("Checking Polygon Premium Subscription Features", operation="enhanced_logging")
    polygon_logger.info("=" * 50, operation="enhanced_logging")

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
    polygon_logger.info("\n4. News API:", operation="enhanced_logging")
    try:
        # Try the news endpoint
        import requests

        url = "https://api.polygon.io/v2/reference/news"
        params = {"apiKey": client.api_key, "ticker": "AAPL", "limit": 1}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            polygon_logger.info("  ✅ News API available", operation="enhanced_logging")
        else:
            polygon_logger.error(f"  ❌ News API status: {resp.status_code}", operation="enhanced_logging")
    except Exception as e:
        polygon_logger.error(f"  ❌ News API error: {e}", operation="enhanced_logging")

    # Check ticker details endpoint
    polygon_logger.info("\n5. Ticker Details (with market cap, operation="enhanced_logging"):")
    try:
        url = "https://api.polygon.io/v3/reference/tickers/AAPL"
        params = {"apiKey": client.api_key}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", {})
            polygon_logger.info("  ✅ Ticker details available", operation="enhanced_logging")
            polygon_logger.info(f"     Market cap field: {'market_cap' in results}", operation="enhanced_logging")
            if "market_cap" in results:
                polygon_logger.info(f"     Market cap: ${results['market_cap']:,.0f}", operation="enhanced_logging")
        else:
            polygon_logger.error(f"  ❌ Status: {resp.status_code}", operation="enhanced_logging")
    except Exception as e:
        polygon_logger.error(f"  ❌ Error: {e}", operation="enhanced_logging")

    # Check financials endpoint
    polygon_logger.info("\n6. Financials/Fundamentals:", operation="enhanced_logging")
    try:
        url = "https://api.polygon.io/vX/reference/financials"
        params = {"apiKey": client.api_key, "ticker": "AAPL", "limit": 1}
        resp = requests.get(url, params=params)
        polygon_logger.info(f"  Status code: {resp.status_code}", operation="enhanced_logging")
        if resp.status_code == 404:
            polygon_logger.info("  ℹ️  Financials might be under different endpoint", operation="enhanced_logging")
    except Exception as e:
        polygon_logger.error(f"  ❌ Error: {e}", operation="enhanced_logging")


if __name__ == "__main__":
    from datetime import date

    main()
