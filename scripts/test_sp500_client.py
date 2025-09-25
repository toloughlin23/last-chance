"""Test SP500Client to verify it gets all 500 symbols properly distributed."""

from services.sp500_client import SP500Client
from collections import Counter

# Get S&P 500 symbols
client = SP500Client()
symbols = client.fetch_symbols()

training_logger.info(f"Got {len(symbols, operation="enhanced_logging")} S&P 500 symbols from Polygon API")
training_logger.info("="*60, operation="enhanced_logging")

# Check distribution
first_letters = Counter(s[0] for s in symbols if s)
training_logger.info("\nFirst letter distribution:", operation="enhanced_logging")
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    count = first_letters.get(letter, 0)
    if count > 0:
        bar = '█' * int(count / 2)
        training_logger.info(f"{letter}: {count:3d} {bar}", operation="enhanced_logging")

training_logger.info(f"\nFirst 20 symbols: {symbols[:20]}", operation="enhanced_logging")
training_logger.info(f"\nLast 20 symbols: {symbols[-20:]}", operation="enhanced_logging")

# Verify some known S&P 500 stocks are included
known = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "WMT"]
found = [s for s in known if s in symbols]
training_logger.info(f"\nVerified {len(found, operation="enhanced_logging")}/{len(known)} known S&P 500 stocks: {found}")
