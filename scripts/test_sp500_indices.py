"""
Test if we can get S&P 500 constituents directly from Polygon Indices API
"""
import os
import sys
from pathlib import Path

# Load environment
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient

def test_sp500_indices():
    """Test different ways to get S&P 500 from Polygon."""
    client = PolygonClient()
    
    training_logger.info("TESTING S&P 500 ACCESS WITH POLYGON PREMIUM", operation="enhanced_logging")
    training_logger.info("="*60, operation="enhanced_logging")
    
    # Test 1: Try to get S&P 500 index directly
    training_logger.info("\nTest 1: Get S&P 500 index (I:SPX, operation="enhanced_logging")")
    try:
        data = client.get_tickers(
            search="SPX",
            type="IDX",  # Index type
            active=True,
            limit=10
        )
        results = data.get("results", [])
        training_logger.info(f"Found {len(results, operation="enhanced_logging")} index results")
        for r in results:
            training_logger.info(f"  - {r.get('ticker', operation="enhanced_logging")}: {r.get('name')}")
    except Exception as e:
        training_logger.error(f"Error: {e}", operation="enhanced_logging")
    
    # Test 2: Try common S&P 500 index tickers
    training_logger.info("\n\nTest 2: Search for S&P 500 index variants", operation="enhanced_logging")
    sp500_tickers = ["I:SPX", "SPX", "^SPX", "$SPX", "SP500"]
    
    for ticker in sp500_tickers:
        try:
            training_logger.info(f"\nTrying ticker: {ticker}", operation="enhanced_logging")
            details = client.get_ticker_details(ticker)
            if details and details.get("results"):
                result = details["results"]
                training_logger.info(f"✅ Found: {result.get('name', operation="enhanced_logging")}")
                training_logger.info(f"   Type: {result.get('type', operation="enhanced_logging")}")
                training_logger.info(f"   Market: {result.get('market', operation="enhanced_logging")}")
        except Exception as e:
            training_logger.error(f"❌ Not found: {e}", operation="enhanced_logging")
    
    # Test 3: Check if we have an index endpoint
    training_logger.info("\n\nTest 3: Check for index-specific endpoints", operation="enhanced_logging")
    try:
        # Try the reference/indices endpoint
        path = "/v3/reference/indices"
        url = f"{client.BASE_URL}{path}"
        data = client.http.get_json(url, params=client._auth_params({}))
        training_logger.info("✅ Indices endpoint exists!", operation="enhanced_logging")
        training_logger.info(f"Response: {data}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"❌ No indices endpoint: {e}", operation="enhanced_logging")
    
    # Test 4: Look for ETFs that track S&P 500
    training_logger.info("\n\nTest 4: S&P 500 ETFs (SPY, VOO, IVV, operation="enhanced_logging")")
    etfs = ["SPY", "VOO", "IVV"]
    for etf in etfs:
        try:
            details = client.get_ticker_details(etf)
            if details and details.get("results"):
                result = details["results"]
                training_logger.info(f"\n{etf}: {result.get('name', operation="enhanced_logging")}")
                training_logger.info(f"  Market cap: ${result.get('market_cap', 0, operation="enhanced_logging")/1e9:.1f}B")
        except Exception as e:
            training_logger.error(f"{etf}: Error - {e}", operation="enhanced_logging")

if __name__ == "__main__":
    test_sp500_indices()

