#!/usr/bin/env python3
"""Debug Polygon API connection"""

from dotenv import load_dotenv
from services.polygon_client import PolygonClient
import json

def main():
    load_dotenv()
    
    print("Testing Polygon API connection...")
    client = PolygonClient()
    
    # Test get_tickers
    print("\n1. Testing get_tickers endpoint:")
    try:
        data = client.get_tickers(market="stocks", active=True, limit=5)
        print(f"   Status: {data.get('status')}")
        print(f"   Count: {data.get('count')}")
        print(f"   Results length: {len(data.get('results', []))}")
        
        if data.get('results'):
            first = data['results'][0]
            print(f"   First ticker: {first.get('ticker')}")
            print(f"   Market cap: {first.get('market_cap')}")
            print(f"   Fields available: {list(first.keys())[:10]}...")
    except Exception as e:
        print(f"   Error: {e}")
        
    # Test get_aggs
    print("\n2. Testing get_aggs endpoint:")
    try:
        data = client.get_aggs("AAPL", 1, "day", "2025-09-15", "2025-09-20", limit=5)
        print(f"   Status: {data.get('status')}")
        print(f"   Results length: {len(data.get('results', []))}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    main()


