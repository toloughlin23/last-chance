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
    universe_logger.info("🔍 TESTING SELECTOR WITH PROVIDER'S ACTUAL OUTPUT", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")
    
    try:
        from utils.universe_selector import UniverseSelector
        from services.polygon_client import PolygonClient
        
        # Use the exact candidates the provider found
        provider_candidates = [
            'BE', 'CDE', 'OKLO', 'IONQ', 'B', 'RDDT', 'CIEN', 'KGC', 'PSTG', 'CLS',
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
            'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS',
            'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW',
            'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC', 'SPOT'
        ]
        
        universe_logger.info(f"📊 Testing with {len(provider_candidates, operation="enhanced_logging")} provider candidates")
        universe_logger.info(f"📈 Sample: {provider_candidates[:10]}", operation="enhanced_logging")
        
        # Initialize selector
        polygon_client = PolygonClient()
        selector = UniverseSelector(polygon_client)
        
        universe_logger.info("\n🎯 Testing selector with provider candidates...", operation="enhanced_logging")
        
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
            universe_logger.info(f"✅ SUCCESS: Generated {len(universe, operation="enhanced_logging")} symbols")
            universe_logger.info(f"📈 First 10: {universe[:10]}", operation="enhanced_logging")
            
            # Check distribution
            first_letters = {}
            for symbol in universe:
                first_letter = symbol[0].upper()
                first_letters[first_letter] = first_letters.get(first_letter, 0) + 1
            
            universe_logger.info(f"\n🔍 Distribution: {dict(sorted(first_letters.items(, operation="enhanced_logging")))}")
        else:
            universe_logger.error("❌ FAILED: No universe generated", operation="enhanced_logging")
                
    except Exception as e:
        universe_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

