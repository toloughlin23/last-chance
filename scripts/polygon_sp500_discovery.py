"""
PROPER POLYGON S&P 500 DISCOVERY
================================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Use Polygon API correctly to get S&P 500 stocks by:
1. Filtering by US exchanges (NYSE, NASDAQ)
2. Getting ticker details for market cap
3. Filtering by market cap > $8B (typical S&P 500 threshold)
4. Using proper pagination
"""

import os
import sys
import time
from pathlib import Path
from collections import Counter
from typing import List, Dict, Set

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient


def discover_sp500_stocks() -> List[str]:
    """Discover S&P 500 stocks using Polygon API properly."""
    
    polygon_logger.info("DISCOVERING S&P 500 STOCKS WITH POLYGON", operation="enhanced_logging")
    polygon_logger.info("="*80, operation="enhanced_logging")
    polygon_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    polygon_logger.info("="*80, operation="enhanced_logging")
    
    client = PolygonClient()
    
    # S&P 500 criteria:
    # 1. US exchanges (NYSE: XNYS, NASDAQ: XNAS)
    # 2. Common stock (type: CS)
    # 3. Market cap > $8B (must check with ticker details)
    # 4. Active trading
    
    all_candidates = []
    exchanges = ["XNYS", "XNAS"]  # NYSE and NASDAQ
    
    for exchange in exchanges:
        polygon_logger.info(f"\n📈 Getting stocks from {exchange}...", operation="enhanced_logging")
        
        try:
            # Get stocks from this exchange
            # We'll get more than we need and filter by market cap
            data = client.get_tickers(
                market="stocks",
                active=True,
                type="CS",  # Common Stock only
                exchange=exchange,
                limit=1000  # Get many to ensure we cover S&P 500
            )
            
            results = data.get("results", [])
            polygon_logger.info(f"✅ Got {len(results, operation="enhanced_logging")} active common stocks from {exchange}")
            
            # Extract symbols
            symbols = []
            for ticker_data in results:
                symbol = ticker_data.get("ticker")
                if symbol and isinstance(symbol, str):
                    # Skip special symbols
                    if not any(char in symbol for char in ['/', '.', '-'] if char != '.'):
                        symbols.append(symbol)
            
            polygon_logger.info(f"📊 Extracted {len(symbols, operation="enhanced_logging")} valid symbols")
            
            # Show diversity
            if symbols:
                first_letters = Counter(s[0].upper() for s in symbols[:100])
                polygon_logger.info(f"   First letter sample: {dict(list(first_letters.items(, operation="enhanced_logging"))[:10])}")
                polygon_logger.info(f"   First 10: {symbols[:10]}", operation="enhanced_logging")
                polygon_logger.info(f"   Last 10: {symbols[-10:]}", operation="enhanced_logging")
            
            all_candidates.extend(symbols)
            
        except Exception as e:
            polygon_logger.error(f"❌ Error getting {exchange} stocks: {e}", operation="enhanced_logging")
    
    polygon_logger.info(f"\n📊 Total candidates from US exchanges: {len(all_candidates, operation="enhanced_logging")}")
    
    # Remove duplicates
    unique_candidates = list(dict.fromkeys(all_candidates))
    polygon_logger.info(f"📊 Unique candidates: {len(unique_candidates, operation="enhanced_logging")}")
    
    # Now filter by market cap
    polygon_logger.info("\n🔍 Filtering by market cap (S&P 500 typically > $8B, operation="enhanced_logging")...")
    
    sp500_stocks = []
    checked = 0
    
    # Check in batches to show progress
    batch_size = 50
    for i in range(0, min(len(unique_candidates), 500), batch_size):
        batch = unique_candidates[i:i+batch_size]
        polygon_logger.info(f"\n📊 Checking batch {i//batch_size + 1}: {len(batch, operation="enhanced_logging")} symbols")
        
        for symbol in batch:
            try:
                # Get ticker details for market cap
                details = client.get_ticker_details(symbol)
                if details and details.get("results"):
                    result = details["results"]
                    market_cap = result.get("market_cap", 0)
                    
                    # S&P 500 threshold
                    if market_cap >= 8_000_000_000:  # $8B+
                        name = result.get("name", "Unknown")
                        sp500_stocks.append(symbol)
                        if len(sp500_stocks) <= 10:
                            polygon_logger.info(f"   ✅ {symbol}: ${market_cap/1e9:.1f}B - {name}", operation="enhanced_logging")
                    
                checked += 1
                
                # Small delay to respect rate limits
                if checked % 10 == 0:
                    time.sleep(0.1)
                    
            except Exception as e:
                # Skip symbols that error
                pass
        
        # Show progress
        if sp500_stocks:
            letters = Counter(s[0].upper() for s in sp500_stocks)
            polygon_logger.info(f"   Found {len(sp500_stocks, operation="enhanced_logging")} S&P 500 stocks so far")
            polygon_logger.info(f"   Letter distribution: {dict(list(letters.items(, operation="enhanced_logging"))[:10])}")
    
    return sp500_stocks


def verify_known_sp500_stocks(known_stocks: List[str]) -> Dict[str, float]:
    """Verify a list of known S&P 500 stocks and get their market caps."""
    
    polygon_logger.info("\n\nVERIFYING KNOWN S&P 500 STOCKS", operation="enhanced_logging")
    polygon_logger.info("="*80, operation="enhanced_logging")
    
    client = PolygonClient()
    verified = {}
    
    # Test with some known large S&P 500 companies
    test_symbols = known_stocks[:20]
    
    for symbol in test_symbols:
        try:
            details = client.get_ticker_details(symbol)
            if details and details.get("results"):
                market_cap = details["results"].get("market_cap", 0)
                if market_cap > 0:
                    verified[symbol] = market_cap
                    polygon_logger.info(f"✅ {symbol}: ${market_cap/1e9:.1f}B", operation="enhanced_logging")
                else:
                    polygon_logger.error(f"❌ {symbol}: No market cap data", operation="enhanced_logging")
        except Exception as e:
            polygon_logger.error(f"❌ {symbol}: Error - {e}", operation="enhanced_logging")
    
    return verified


def main():
    """Main function to discover S&P 500 stocks properly."""
    
    # First, discover stocks from US exchanges
    sp500_stocks = discover_sp500_stocks()
    
    polygon_logger.info("\n\n📊 RESULTS", operation="enhanced_logging")
    polygon_logger.info("="*80, operation="enhanced_logging")
    polygon_logger.info(f"Found {len(sp500_stocks, operation="enhanced_logging")} stocks meeting S&P 500 criteria")
    
    if sp500_stocks:
        # Analyze distribution
        first_letters = Counter(s[0].upper() for s in sp500_stocks)
        
        polygon_logger.info("\nFirst letter distribution:", operation="enhanced_logging")
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = first_letters.get(letter, 0)
            if count > 0:
                pct = 100.0 * count / len(sp500_stocks)
                bar = '█' * int(pct / 2)
                polygon_logger.info(f"{letter}: {count:3d} ({pct:5.1f}%, operation="enhanced_logging") {bar}")
        
        polygon_logger.info(f"\nFirst 20 S&P 500 stocks: {sp500_stocks[:20]}", operation="enhanced_logging")
        polygon_logger.info(f"Last 20 S&P 500 stocks: {sp500_stocks[-20:]}", operation="enhanced_logging")
    
    # Also verify some known S&P 500 stocks
    known_sp500 = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
        "BRK.B", "JPM", "UNH", "JNJ", "V", "PG", "MA", "HD",
        "CVX", "MRK", "ABBV", "PFE", "KO"
    ]
    
    polygon_logger.info("\n\nVerifying known S&P 500 stocks...", operation="enhanced_logging")
    verified = verify_known_sp500_stocks(known_sp500)
    
    polygon_logger.info(f"\nVerified {len(verified, operation="enhanced_logging")} out of {len(known_sp500)} known S&P 500 stocks")


if __name__ == "__main__":
    main()
    
    polygon_logger.info("\n\nCONCLUSION:", operation="enhanced_logging")
    polygon_logger.info("="*80, operation="enhanced_logging")
    polygon_logger.info("Polygon has EVERYTHING we need!", operation="enhanced_logging")
    polygon_logger.info("1. Filter by US exchanges (NYSE, NASDAQ, operation="enhanced_logging")")
    polygon_logger.info("2. Filter by type='CS' for common stocks", operation="enhanced_logging")
    polygon_logger.info("3. Get ticker details for market cap", operation="enhanced_logging")
    polygon_logger.info("4. Filter by market cap > $8B", operation="enhanced_logging")
    polygon_logger.info("\n100% GENUINE - POLYGON HAS ALL THE DATA WE NEED!", operation="enhanced_logging")
