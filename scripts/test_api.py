#!/usr/bin/env python3
"""
Test API Key and Direct Calls
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

load_dotenv()

def main():
    print("🔍 TESTING API KEY AND DIRECT CALLS")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv('POLYGON_API_KEY')
    print(f'API Key found: {bool(api_key)}')
    print(f'API Key length: {len(api_key) if api_key else 0}')
    if api_key:
        print(f'API Key starts with: {api_key[:10]}...')
    else:
        print('API Key: None')
        return
    
    # Test Polygon client
    try:
        from services.polygon_client import PolygonClient
        
        client = PolygonClient()
        print(f'Client API key: {client.api_key[:10] if client.api_key else "None"}...')
        
        # Test direct API call
        print("\n🧪 Testing direct API call...")
        data = client.get_aggs('AAPL', 1, 'day', '2024-01-01', '2024-01-02', limit=5)
        print('✅ Direct API call successful')
        print(f'Data keys: {list(data.keys())}')
        
        # Test with provider candidates
        print("\n🧪 Testing with provider candidates...")
        provider_candidates = ['BE', 'CDE', 'OKLO', 'IONQ', 'B']
        
        for symbol in provider_candidates:
            try:
                data = client.get_aggs(symbol, 1, 'day', '2024-01-01', '2024-01-02', limit=5)
                print(f'✅ {symbol}: Success')
            except Exception as e:
                print(f'❌ {symbol}: {e}')
                
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
