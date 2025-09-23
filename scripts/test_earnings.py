#!/usr/bin/env python3
"""
Test Earnings Calendar Method
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

def main():
    print("🔍 TESTING EARNINGS CALENDAR METHOD")
    print("=" * 50)
    
    try:
        from services.polygon_client import PolygonClient
        
        client = PolygonClient()
        
        # Test earnings calendar with a few symbols
        test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'BE', 'CDE']
        
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        
        print(f"📅 Testing earnings calendar from {start_date} to {end_date}")
        
        for symbol in test_symbols:
            try:
                print(f"\n🧪 Testing {symbol}...")
                data = client.get_earnings_calendar(symbol, start_date, end_date)
                results = data.get("results", [])
                print(f"✅ {symbol}: Found {len(results)} earnings dates")
                if results:
                    print(f"   First date: {results[0].get('date', 'N/A')}")
            except Exception as e:
                print(f"❌ {symbol}: {e}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
