#!/usr/bin/env python3
"""
Test Selector with Provider's Actual Output
"""

import os
import sys
from datetime import date, timedelta

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv

load_dotenv()

def main():
    print("🔍 TESTING SELECTOR WITH PROVIDER'S ACTUAL OUTPUT")
    print("=" * 60)
    
    try:
        from services.polygon_client import PolygonClient
        from utils.universe_selector import UniverseSelector
        
        # Use the exact candidates the provider found
        provider_candidates = [
            'BE', 'CDE', 'OKLO', 'IONQ', 'B', 'RDDT', 'CIEN', 'KGC', 'PSTG', 'CLS',
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
            'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS',
            'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW',
            'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC', 'SPOT'
        ]
        
        print(f"📊 Testing with {len(provider_candidates)} provider candidates")
        print(f"📈 Sample: {provider_candidates[:10]}")
        
        # Initialize selector
        polygon_client = PolygonClient()
        selector = UniverseSelector(polygon_client)
        
        print("\n🎯 Testing selector with provider candidates...")
        
        # Test the selector
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        
        universe = selector.select_universe(
            candidates=provider_candidates,
            target_size=50,
            start_date=start_date,
            end_date=end_date,
            earnings_exclusion=None  # Disable earnings exclusion to isolate the issue
        )
        
        if universe:
            print(f"✅ SUCCESS: Generated {len(universe)} symbols")
            print(f"📈 First 10: {universe[:10]}")
            
            # Check distribution
            first_letters = {}
            for symbol in universe:
                first_letter = symbol[0].upper()
                first_letters[first_letter] = first_letters.get(first_letter, 0) + 1
            
            print(f"\n🔍 Distribution: {dict(sorted(first_letters.items()))}")
        else:
            print("❌ FAILED: No universe generated")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
