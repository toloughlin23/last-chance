"""
Test if we have access to Polygon Indices API with current subscription
"""
import os
import sys
from pathlib import Path

# Load environment
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient

def test_indices_access():
    """Test if we can access Indices API endpoints."""
    client = PolygonClient()
    
    training_logger.info("TESTING POLYGON INDICES API ACCESS", operation="enhanced_logging")
    training_logger.info("="*50, operation="enhanced_logging")
    
    # Test 1: Try to get S&P 500 index info
    training_logger.info("\n1. Testing S&P 500 index (I:SPX, operation="enhanced_logging")...")
    try:
        data = client.get_tickers(
            search="SPX",
            type="IDX",  # Index type
            active=True,
            limit=10
        )
        results = data.get("results", [])
        training_logger.info(f"   Found {len(results, operation="enhanced_logging")} index results")
        for r in results:
            training_logger.info(f"   - {r.get('ticker', operation="enhanced_logging")}: {r.get('name')}")
    except Exception as e:
        training_logger.error(f"   Error: {e}", operation="enhanced_logging")
    
    # Test 2: Try different S&P 500 ticker formats
    training_logger.info("\n2. Testing S&P 500 ticker formats...", operation="enhanced_logging")
    sp500_variants = ["I:SPX", "SPX", "^SPX", "$SPX", "SP500", "SPY"]
    
    for ticker in sp500_variants:
        try:
            training_logger.info(f"   Testing {ticker}...", operation="enhanced_logging")
            details = client.get_ticker_details(ticker)
            if details and details.get("results"):
                result = details["results"]
                training_logger.info(f"   ✅ {ticker}: {result.get('name', operation="enhanced_logging")} (Type: {result.get('type')})")
            else:
                training_logger.error(f"   ❌ {ticker}: No results", operation="enhanced_logging")
        except Exception as e:
            training_logger.error(f"   ❌ {ticker}: {e}", operation="enhanced_logging")
    
    # Test 3: Check if we can search for indices
    training_logger.info("\n3. Testing index search...", operation="enhanced_logging")
    try:
        data = client.get_tickers(
            market="indices",  # Try indices market
            active=True,
            limit=5
        )
        results = data.get("results", [])
        training_logger.info(f"   Found {len(results, operation="enhanced_logging")} indices")
        for r in results[:3]:
            training_logger.info(f"   - {r.get('ticker', operation="enhanced_logging")}: {r.get('name')}")
    except Exception as e:
        training_logger.error(f"   Error: {e}", operation="enhanced_logging")
    
    # Test 4: Try to get index constituents (if available)
    training_logger.info("\n4. Testing index constituents...", operation="enhanced_logging")
    try:
        # This would be the ideal endpoint if available
        path = "/v3/reference/indices"
        url = f"{client.BASE_URL}{path}"
        data = client.http.get_json(url, params=client._auth_params({}))
        training_logger.info("   ✅ Indices endpoint accessible!", operation="enhanced_logging")
        training_logger.info(f"   Response: {data}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"   ❌ Indices endpoint: {e}", operation="enhanced_logging")
    
    # Test 5: Check what markets are available
    training_logger.info("\n5. Testing available markets...", operation="enhanced_logging")
    markets = ["stocks", "indices", "options", "forex", "crypto"]
    for market in markets:
        try:
            data = client.get_tickers(market=market, active=True, limit=1)
            if data.get("results"):
                training_logger.info(f"   ✅ {market}: Available", operation="enhanced_logging")
            else:
                training_logger.error(f"   ❌ {market}: No results", operation="enhanced_logging")
        except Exception as e:
            training_logger.error(f"   ❌ {market}: {e}", operation="enhanced_logging")

if __name__ == "__main__":
    test_indices_access()

