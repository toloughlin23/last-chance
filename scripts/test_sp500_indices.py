"""
Test if we can get S&P 500 constituents directly from Polygon Indices API
"""
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
    
    print("TESTING S&P 500 ACCESS WITH POLYGON PREMIUM")
    print("="*60)
    
    # Test 1: Try to get S&P 500 index directly
    print("\nTest 1: Get S&P 500 index (I:SPX)")
    try:
        data = client.get_tickers(
            search="SPX",
            type="IDX",  # Index type
            active=True,
            limit=10
        )
        results = data.get("results", [])
        print(f"Found {len(results)} index results")
        for r in results:
            print(f"  - {r.get('ticker')}: {r.get('name')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Try common S&P 500 index tickers
    print("\n\nTest 2: Search for S&P 500 index variants")
    sp500_tickers = ["I:SPX", "SPX", "^SPX", "$SPX", "SP500"]
    
    for ticker in sp500_tickers:
        try:
            print(f"\nTrying ticker: {ticker}")
            details = client.get_ticker_details(ticker)
            if details and details.get("results"):
                result = details["results"]
                print(f"✅ Found: {result.get('name')}")
                print(f"   Type: {result.get('type')}")
                print(f"   Market: {result.get('market')}")
        except Exception as e:
            print(f"❌ Not found: {e}")
    
    # Test 3: Check if we have an index endpoint
    print("\n\nTest 3: Check for index-specific endpoints")
    try:
        # Try the reference/indices endpoint
        path = "/v3/reference/indices"
        url = f"{client.BASE_URL}{path}"
        data = client.http.get_json(url, params=client._auth_params({}))
        print("✅ Indices endpoint exists!")
        print(f"Response: {data}")
    except Exception as e:
        print(f"❌ No indices endpoint: {e}")
    
    # Test 4: Look for ETFs that track S&P 500
    print("\n\nTest 4: S&P 500 ETFs (SPY, VOO, IVV)")
    etfs = ["SPY", "VOO", "IVV"]
    for etf in etfs:
        try:
            details = client.get_ticker_details(etf)
            if details and details.get("results"):
                result = details["results"]
                print(f"\n{etf}: {result.get('name')}")
                print(f"  Market cap: ${result.get('market_cap', 0)/1e9:.1f}B")
        except Exception as e:
            print(f"{etf}: Error - {e}")

if __name__ == "__main__":
    test_sp500_indices()
