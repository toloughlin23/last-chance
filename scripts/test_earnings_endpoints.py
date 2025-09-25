#!/usr/bin/env python3
"""Test different earnings endpoints to find the correct one for premium subscription"""

import json

import requests
from dotenv import load_dotenv


def test_earnings_endpoint(api_key, endpoint_name, url, params):
    training_logger.info(f"\nTesting {endpoint_name}:", operation="enhanced_logging")
    training_logger.info(f"URL: {url}", operation="enhanced_logging")
    try:
        resp = requests.get(url, params=params)
        training_logger.info(f"Status: {resp.status_code}", operation="enhanced_logging")
        if resp.status_code == 200:
            data = resp.json()
            training_logger.info(f"Response keys: {list(data.keys(, operation="enhanced_logging"))}")
            if "results" in data:
                training_logger.info(f"Results count: {len(data['results'], operation="enhanced_logging")}")
                if data["results"]:
                    training_logger.info(f"First result: {json.dumps(data['results'][0], indent=2, operation="enhanced_logging")}")
        else:
            training_logger.error(f"Error: {resp.text[:200]}", operation="enhanced_logging")
    except Exception as e:
        training_logger.info(f"Exception: {e}", operation="enhanced_logging")


def main():
    load_dotenv()
    import os

    api_key = os.getenv("POLYGON_API_KEY")

    if not api_key:
        training_logger.info("No API key found!", operation="enhanced_logging")
        return

    training_logger.info("Testing Polygon Earnings Endpoints", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    # Test different possible earnings endpoints
    symbol = "AAPL"
    start_date = "2025-09-01"
    end_date = "2025-09-30"

    # 1. Benzinga earnings (current implementation)
    test_earnings_endpoint(
        api_key,
        "Benzinga Earnings (v1)",
        "https://api.polygon.io/v1/partners/benzinga/earnings",
        {
            "apiKey": api_key,
            "company_tickers": symbol,
            "from": start_date,
            "to": end_date,
            "limit": 10,
        },
    )

    # 2. Try v2 reference financials
    test_earnings_endpoint(
        api_key,
        "Reference Financials (v2)",
        f"https://api.polygon.io/v2/reference/financials/{symbol}",
        {
            "apiKey": api_key,
            "limit": 10,
            "type": "Y",  # Yearly
            "sort": "report_period",
        },
    )

    # 3. Try vX reference financials
    test_earnings_endpoint(
        api_key,
        "Reference Financials (vX)",
        "https://api.polygon.io/vX/reference/financials",
        {"apiKey": api_key, "ticker": symbol, "limit": 10, "timeframe": "quarterly"},
    )

    # 4. Try events endpoint
    test_earnings_endpoint(
        api_key,
        "Events API",
        "https://api.polygon.io/vX/reference/tickers/events",
        {
            "apiKey": api_key,
            "ticker": symbol,
            "types": "earnings",
            "from": start_date,
            "to": end_date,
        },
    )

    # 5. Check if earnings is in ticker details
    training_logger.info("\nChecking ticker details for earnings info:", operation="enhanced_logging")
    url = f"https://api.polygon.io/v3/reference/tickers/{symbol}"
    params = {"apiKey": api_key}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", {})
        # Look for any earnings-related fields
        earnings_fields = [
            k for k in results.keys() if "earning" in k.lower() or "report" in k.lower()
        ]
        if earnings_fields:
            training_logger.info(f"Found earnings fields: {earnings_fields}", operation="enhanced_logging")
            for field in earnings_fields:
                training_logger.info(f"  {field}: {results[field]}", operation="enhanced_logging")
        else:
            training_logger.info("No earnings fields found in ticker details", operation="enhanced_logging")


if __name__ == "__main__":
    main()
