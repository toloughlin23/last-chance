#!/usr/bin/env python3
"""Test different earnings endpoints to find the correct one for premium subscription"""

from dotenv import load_dotenv
import requests
from datetime import date
import json

def test_earnings_endpoint(api_key, endpoint_name, url, params):
    print(f"\nTesting {endpoint_name}:")
    print(f"URL: {url}")
    try:
        resp = requests.get(url, params=params)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response keys: {list(data.keys())}")
            if 'results' in data:
                print(f"Results count: {len(data['results'])}")
                if data['results']:
                    print(f"First result: {json.dumps(data['results'][0], indent=2)}")
        else:
            print(f"Error: {resp.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

def main():
    load_dotenv()
    import os
    api_key = os.getenv("POLYGON_API_KEY")
    
    if not api_key:
        print("No API key found!")
        return
    
    print("Testing Polygon Earnings Endpoints")
    print("=" * 50)
    
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
            "limit": 10
        }
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
            "sort": "report_period"
        }
    )
    
    # 3. Try vX reference financials
    test_earnings_endpoint(
        api_key,
        "Reference Financials (vX)",
        "https://api.polygon.io/vX/reference/financials",
        {
            "apiKey": api_key,
            "ticker": symbol,
            "limit": 10,
            "timeframe": "quarterly"
        }
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
            "to": end_date
        }
    )
    
    # 5. Check if earnings is in ticker details
    print("\nChecking ticker details for earnings info:")
    url = f"https://api.polygon.io/v3/reference/tickers/{symbol}"
    params = {"apiKey": api_key}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        results = data.get('results', {})
        # Look for any earnings-related fields
        earnings_fields = [k for k in results.keys() if 'earning' in k.lower() or 'report' in k.lower()]
        if earnings_fields:
            print(f"Found earnings fields: {earnings_fields}")
            for field in earnings_fields:
                print(f"  {field}: {results[field]}")
        else:
            print("No earnings fields found in ticker details")

if __name__ == "__main__":
    main()



