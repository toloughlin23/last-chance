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
    training_logger.info("🔍 TESTING EARNINGS CALENDAR METHOD", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")
    
    try:
        from services.polygon_client import PolygonClient
        
        client = PolygonClient()
        
        # Test earnings calendar with a few symbols
        test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'BE', 'CDE']
        
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        
        training_logger.info(f"📅 Testing earnings calendar from {start_date} to {end_date}", operation="enhanced_logging")
        
        for symbol in test_symbols:
            try:
                training_logger.info(f"\n🧪 Testing {symbol}...", operation="enhanced_logging")
                data = client.get_earnings_calendar(symbol, start_date, end_date)
                results = data.get("results", [])
                training_logger.info(f"✅ {symbol}: Found {len(results, operation="enhanced_logging")} earnings dates")
                if results:
                    training_logger.info(f"   First date: {results[0].get('date', 'N/A', operation="enhanced_logging")}")
            except Exception as e:
                training_logger.error(f"❌ {symbol}: {e}", operation="enhanced_logging")
                
    except Exception as e:
        training_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

