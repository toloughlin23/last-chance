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
    training_logger.info("🔍 TESTING API KEY AND DIRECT CALLS", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")
    
    # Check API key
    api_key = os.getenv('POLYGON_API_KEY')
    training_logger.info(f'API Key found: {bool(api_key, operation="enhanced_logging")}')
    training_logger.info(f'API Key length: {len(api_key, operation="enhanced_logging") if api_key else 0}')
    if api_key:
        training_logger.info(f'API Key starts with: {api_key[:10]}...', operation="enhanced_logging")
    else:
        training_logger.info('API Key: None', operation="enhanced_logging")
        return
    
    # Test Polygon client
    try:
        from services.polygon_client import PolygonClient
        
        client = PolygonClient()
        training_logger.info(f'Client API key: {client.api_key[:10] if client.api_key else "None"}...', operation="enhanced_logging")
        
        # Test direct API call
        training_logger.info("\n🧪 Testing direct API call...", operation="enhanced_logging")
        data = client.get_aggs('AAPL', 1, 'day', '2024-01-01', '2024-01-02', limit=5)
        training_logger.info('✅ Direct API call successful', operation="enhanced_logging")
        training_logger.info(f'Data keys: {list(data.keys(, operation="enhanced_logging"))}')
        
        # Test with provider candidates
        training_logger.info("\n🧪 Testing with provider candidates...", operation="enhanced_logging")
        provider_candidates = ['BE', 'CDE', 'OKLO', 'IONQ', 'B']
        
        for symbol in provider_candidates:
            try:
                data = client.get_aggs(symbol, 1, 'day', '2024-01-01', '2024-01-02', limit=5)
                training_logger.info(f'✅ {symbol}: Success', operation="enhanced_logging")
            except Exception as e:
                training_logger.error(f'❌ {symbol}: {e}', operation="enhanced_logging")
                
    except Exception as e:
        training_logger.error(f'❌ Error: {e}', operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

