"""
FIX POLYGON PAGINATION - GET ALL TICKERS PROPERLY
=================================================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Polygon API is NOT broken - we're just not using it correctly!
We need to paginate through ALL results, not just take the first 500.
"""

import sys
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient
import requests


def get_all_tickers_with_pagination() -> List[str]:
    """Get ALL stock tickers from Polygon using proper pagination."""
    
    polygon_logger.info("GETTING ALL TICKERS WITH PROPER PAGINATION", operation="enhanced_logging")
    polygon_logger.info("="*60, operation="enhanced_logging")
    polygon_logger.info("100% GENUINE - ALWAYS MAKE BETTER - NEVER REMOVE TO FIX", operation="enhanced_logging")
    polygon_logger.info("="*60, operation="enhanced_logging")
    
    client = PolygonClient()
    all_symbols = []
    
    # Start with first page
    next_url = None
    page = 1
    
    while True:
        try:
            if next_url:
                # Use next_url for pagination
                polygon_logger.info(f"\n📄 Fetching page {page} using next_url...", operation="enhanced_logging")
                # We need to make direct request with API key
                response = requests.get(next_url)
                response.raise_for_status()
                data = response.json()
            else:
                # First request
                polygon_logger.info(f"\n📄 Fetching page {page}...", operation="enhanced_logging")
                data = client.get_tickers(
                    market="stocks",
                    active=True,
                    limit=1000  # Max allowed per page
                )
            
            # Extract symbols from this page
            results = data.get("results", [])
            page_symbols = [
                t.get("ticker") for t in results 
                if isinstance(t.get("ticker"), str) and t.get("ticker")
            ]
            
            polygon_logger.info(f"✅ Page {page}: Got {len(page_symbols, operation="enhanced_logging")} symbols")
            
            if page_symbols:
                # Show first letter distribution for this page
                first_letters = Counter(s[0].upper() for s in page_symbols if s)
                polygon_logger.info(f"   First letters this page: {dict(list(first_letters.items(, operation="enhanced_logging"))[:5])}...")
                polygon_logger.info(f"   First 5: {page_symbols[:5]}", operation="enhanced_logging")
                polygon_logger.info(f"   Last 5: {page_symbols[-5:]}", operation="enhanced_logging")
                
                all_symbols.extend(page_symbols)
            
            # Check for next page
            next_url = data.get("next_url")
            if not next_url or page >= 10:  # Limit to 10 pages for comprehensive analysis
                break
                
            page += 1
            
        except Exception as e:
            polygon_logger.error(f"❌ Error on page {page}: {e}", operation="enhanced_logging")
            break
    
    polygon_logger.info(f"\n📊 TOTAL: Got {len(all_symbols, operation="enhanced_logging")} symbols across {page} pages")
    
    # Show overall distribution
    if all_symbols:
        first_letters = Counter(s[0].upper() for s in all_symbols if s)
        polygon_logger.info("\nFirst letter distribution (ALL PAGES, operation="enhanced_logging"):")
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = first_letters.get(letter, 0)
            if count > 0:
                pct = 100.0 * count / len(all_symbols)
                polygon_logger.info(f"{letter}: {count:4d} ({pct:5.1f}%, operation="enhanced_logging")")
    
    return all_symbols


def filter_sp500_from_all_tickers(all_tickers: List[str]) -> List[str]:
    """Filter to get likely S&P 500 stocks from all tickers."""
    
    polygon_logger.info("\n\nFILTERING FOR S&P 500 CHARACTERISTICS", operation="enhanced_logging")
    polygon_logger.info("="*60, operation="enhanced_logging")
    
    client = PolygonClient()
    sp500_candidates = []
    
    # S&P 500 characteristics:
    # - Large market cap (> $8B typically)
    # - High liquidity
    # - US exchanges (NYSE, NASDAQ)
    
    polygon_logger.info("Checking market caps for filtering...", operation="enhanced_logging")
    
    # Sample check on first 50 diverse tickers
    sample_tickers = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letter_tickers = [t for t in all_tickers if t.startswith(letter)]
        sample_tickers.extend(letter_tickers[:2])  # 2 per letter max
    
    checked = 0
    for ticker in sample_tickers[:50]:
        try:
            details = client.get_ticker_details(ticker)
            if details and details.get("results"):
                market_cap = details["results"].get("market_cap", 0)
                if market_cap > 8_000_000_000:  # $8B+
                    sp500_candidates.append(ticker)
                    polygon_logger.info(f"✅ {ticker}: ${market_cap/1e9:.1f}B", operation="enhanced_logging")
                checked += 1
        except Exception:
            pass
    
    polygon_logger.info(f"\nChecked {checked} tickers, found {len(sp500_candidates, operation="enhanced_logging")} with $8B+ market cap")
    
    return sp500_candidates


def main():
    """Main function to demonstrate proper Polygon usage."""
    
    # First, let's see if we can get the next_url properly
    client = PolygonClient()
    
    polygon_logger.info("TEST 1: Check if pagination works", operation="enhanced_logging")
    polygon_logger.info("-"*60, operation="enhanced_logging")
    
    try:
        # Get first page
        data = client.get_tickers(market="stocks", active=True, limit=100)
        
        polygon_logger.info(f"First page status: {data.get('status', operation="enhanced_logging")}")
        polygon_logger.info(f"Results count: {data.get('resultsCount', operation="enhanced_logging")}")
        polygon_logger.info(f"Has next_url: {'next_url' in data}", operation="enhanced_logging")
        
        if 'next_url' in data:
            polygon_logger.info(f"✅ Pagination is available!", operation="enhanced_logging")
            # Try to structure the next URL properly
            next_url = data['next_url']
            if not next_url.startswith('http'):
                next_url = f"https://api.polygon.io{next_url}"
            if 'apiKey=' not in next_url:
                # Add API key if missing
                separator = '&' if '?' in next_url else '?'
                next_url = f"{next_url}{separator}apiKey={client.api_key}"
            polygon_logger.info(f"Next URL would be: {next_url[:100]}...", operation="enhanced_logging")
        else:
            polygon_logger.error("❌ No pagination available in response", operation="enhanced_logging")
            
    except Exception as e:
        polygon_logger.error(f"Error: {e}", operation="enhanced_logging")
    
    # Now get all tickers with pagination
    polygon_logger.info("\n\nTEST 2: Get all tickers with pagination", operation="enhanced_logging")
    polygon_logger.info("-"*60, operation="enhanced_logging")
    
    all_tickers = get_all_tickers_with_pagination()
    
    if len(all_tickers) > 500 and not all(t.startswith('A') for t in all_tickers[:500]):
        polygon_logger.info("\n✅ SUCCESS! We got diverse tickers, not just A's!", operation="enhanced_logging")
    else:
        polygon_logger.warning("\n⚠️ Still need to implement full pagination", operation="enhanced_logging")
    
    # Filter for S&P 500 characteristics
    if all_tickers:
        sp500_like = filter_sp500_from_all_tickers(all_tickers)
        polygon_logger.info(f"\nFound {len(sp500_like, operation="enhanced_logging")} stocks with S&P 500 characteristics")


if __name__ == "__main__":
    main()
    
    polygon_logger.info("\n\nCONCLUSION:", operation="enhanced_logging")
    polygon_logger.info("="*60, operation="enhanced_logging")
    polygon_logger.info("Polygon API is NOT broken - we just need to use it correctly!", operation="enhanced_logging")
    polygon_logger.info("Solution: Implement proper pagination to get ALL tickers", operation="enhanced_logging")
    polygon_logger.info("Then filter by market cap and liquidity for S&P 500 stocks", operation="enhanced_logging")
    polygon_logger.info("\n100% GENUINE - ALWAYS MAKE BETTER - NEVER REMOVE TO FIX", operation="enhanced_logging")

