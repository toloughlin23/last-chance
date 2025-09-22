#!/usr/bin/env python3
"""Debug the structure of quotes data"""

from dotenv import load_dotenv
from services.quotes_client import QuotesClient
from datetime import datetime, timedelta, timezone
import json

def main():
    load_dotenv()
    
    client = QuotesClient()
    
    # Get a recent trading day
    end = datetime.now(timezone.utc)
    days_back = 1
    while (end - timedelta(days=days_back)).weekday() >= 5:
        days_back += 1
    
    test_date = end - timedelta(days=days_back)
    start_time = test_date.replace(hour=14, minute=30, second=0, microsecond=0)
    end_time = test_date.replace(hour=14, minute=35, second=0, microsecond=0)  # Just 5 minutes
    
    print(f"Fetching quotes for AAPL from {start_time} to {end_time}")
    
    quotes = client.fetch_quotes_window("AAPL", start_time, end_time, limit=5)
    
    print(f"\nReceived {len(quotes)} quotes")
    
    if quotes:
        print("\nStructure of first quote:")
        print(json.dumps(quotes[0], indent=2, default=str))
        
        print("\nAll available fields:")
        print(list(quotes[0].keys()))
    else:
        print("No quotes received!")
        
        # Try a direct API call to see raw response
        print("\nTrying direct API call...")
        url = f"{client.base}/v3/quotes/AAPL"
        params = {
            "timestamp.gte": start_time.isoformat().replace("+00:00", "Z"),
            "timestamp.lte": end_time.isoformat().replace("+00:00", "Z"),
            "limit": 5,
            "order": "asc",
        }
        params["apiKey"] = client.api_key
        
        import requests
        resp = requests.get(url, params=params)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Response keys: {list(data.keys())}")
            if 'results' in data and data['results']:
                print("\nFirst result structure:")
                print(json.dumps(data['results'][0], indent=2))

if __name__ == "__main__":
    main()


