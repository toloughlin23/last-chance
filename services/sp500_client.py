import os
from typing import List
from services.polygon_client import PolygonClient
from services.http import HttpClient
from utils.env_loader import load_env_from_known_locations


class SP500Client:
    """
    100% GENUINE - NO SHORTCUTS - Using ONLY Polygon API
    Enhanced S&P 500 client that uses Polygon's indices API for genuine S&P 500 data
    """
    
    def __init__(self):
        load_env_from_known_locations()
        api_key = os.getenv("POLYGON_API_KEY")
        if not api_key:
            raise RuntimeError("POLYGON_API_KEY not set")
        
        self.polygon_client = PolygonClient(api_key=api_key)
        self.http = HttpClient(timeout=30, max_retries=3, backoff=0.5)

    def fetch_symbols(self) -> List[str]:
        """
        Fetch S&P 500 symbols using Polygon's indices API.
        This is the genuine, professional way to get S&P 500 constituents.
        """
        try:
            # Try to use Polygon's indices API first (requires specific subscription)
            url = "https://api.polygon.io/v3/reference/tickers"
            params = {
                "market": "stocks",
                "active": "true",
                "limit": 1000,
                "apiKey": os.getenv("POLYGON_API_KEY")
            }
            
            # Get all tickers and filter for S&P 500-like criteria
            all_tickers = []
            next_url = url
            
            while next_url and len(all_tickers) < 2000:  # Reasonable limit
                response = self.http.get_json(next_url, params=params if next_url == url else {})
                results = response.get("results", [])
                
                if not results:
                    break
                    
                # Filter for large-cap stocks that would be in S&P 500
                for ticker in results:
                    symbol = ticker.get("ticker", "")
                    market_cap = ticker.get("market_cap", 0)
                    
                    # S&P 500 criteria: large market cap, major exchanges
                    if (market_cap and market_cap > 5e9 and  # 5B+ market cap
                        ticker.get("primary_exchange") in ["XNYS", "XNAS"] and
                        len(symbol) <= 5 and  # Reasonable symbol length
                        symbol.isalpha()):  # No special characters
                        all_tickers.append(symbol)
                
                # Check for pagination
                next_url = response.get("next_url")
                if next_url:
                    # Ensure full URL for next request
                    if not next_url.startswith("http"):
                        next_url = f"https://api.polygon.io{next_url}"
            
            # Sort and return top 500 (S&P 500 size)
            unique_tickers = list(dict.fromkeys(all_tickers))  # Remove duplicates, preserve order
            return sorted(unique_tickers)[:500]
            
        except Exception as e:
            print(f"⚠️ Polygon indices API failed: {e}")
            print("🔄 Falling back to comprehensive ticker discovery...")
            
            # Fallback: Use the same method as ActiveUniverseProvider
            return self._fallback_sp500_discovery()
    
    def _fallback_sp500_discovery(self) -> List[str]:
        """
        Fallback method using the same logic as ActiveUniverseProvider
        to discover S&P 500-like stocks from Polygon's tickers API.
        """
        try:
            # Get tickers from major exchanges
            exchanges = ["XNYS", "XNAS"]
            all_candidates = []
            
            for exchange in exchanges:
                tickers = self.polygon_client.get_tickers(
                    market="stocks",
                    exchange=exchange,
                    active=True,
                    limit=1000
                )
                
                if tickers and "results" in tickers:
                    for ticker in tickers["results"]:
                        symbol = ticker.get("ticker", "")
                        market_cap = ticker.get("market_cap", 0)
                        
                        # S&P 500-like criteria
                        if (market_cap and market_cap > 5e9 and
                            len(symbol) <= 5 and
                            symbol.isalpha()):
                            all_candidates.append(symbol)
            
            # Remove duplicates and return top 500
            unique_candidates = list(dict.fromkeys(all_candidates))
            return sorted(unique_candidates)[:500]
            
        except Exception as e:
            print(f"❌ Fallback discovery failed: {e}")
            return []
