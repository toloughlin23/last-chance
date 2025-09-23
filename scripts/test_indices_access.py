"""
Test if we have access to Polygon Indices API with current subscription
"""
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
    
    print("TESTING POLYGON INDICES API ACCESS")
    print("="*50)
    
    # Test 1: Try to get S&P 500 index info
    print("\n1. Testing S&P 500 index (I:SPX)...")
    try:
        data = client.get_tickers(
            search="SPX",
            type="IDX",  # Index type
            active=True,
            limit=10
        )
        results = data.get("results", [])
        print(f"   Found {len(results)} index results")
        for r in results:
            print(f"   - {r.get('ticker')}: {r.get('name')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Try different S&P 500 ticker formats
    print("\n2. Testing S&P 500 ticker formats...")
    sp500_variants = ["I:SPX", "SPX", "^SPX", "$SPX", "SP500", "SPY"]
    
    for ticker in sp500_variants:
        try:
            print(f"   Testing {ticker}...")
            details = client.get_ticker_details(ticker)
            if details and details.get("results"):
                result = details["results"]
                print(f"   ✅ {ticker}: {result.get('name')} (Type: {result.get('type')})")
            else:
                print(f"   ❌ {ticker}: No results")
        except Exception as e:
            print(f"   ❌ {ticker}: {e}")
    
    # Test 3: Check if we can search for indices
    print("\n3. Testing index search...")
    try:
        data = client.get_tickers(
            market="indices",  # Try indices market
            active=True,
            limit=5
        )
        results = data.get("results", [])
        print(f"   Found {len(results)} indices")
        for r in results[:3]:
            print(f"   - {r.get('ticker')}: {r.get('name')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Try to get index constituents (if available)
    print("\n4. Testing index constituents...")
    try:
        # This would be the ideal endpoint if available
        path = "/v3/reference/indices"
        url = f"{client.BASE_URL}{path}"
        data = client.http.get_json(url, params=client._auth_params({}))
        print("   ✅ Indices endpoint accessible!")
        print(f"   Response: {data}")
    except Exception as e:
        print(f"   ❌ Indices endpoint: {e}")
    
    # Test 5: Check what markets are available
    print("\n5. Testing available markets...")
    markets = ["stocks", "indices", "options", "forex", "crypto"]
    for market in markets:
        try:
            data = client.get_tickers(market=market, active=True, limit=1)
            if data.get("results"):
                print(f"   ✅ {market}: Available")
            else:
                print(f"   ❌ {market}: No results")
        except Exception as e:
            print(f"   ❌ {market}: {e}")

if __name__ == "__main__":
    test_indices_access()
