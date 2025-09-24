"""Test SP500Client to verify it gets all 500 symbols properly distributed."""

from services.sp500_client import SP500Client
from collections import Counter

# Get S&P 500 symbols
client = SP500Client()
symbols = client.fetch_symbols()

print(f"Got {len(symbols)} S&P 500 symbols from Polygon API")
print("="*60)

# Check distribution
first_letters = Counter(s[0] for s in symbols if s)
print("\nFirst letter distribution:")
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    count = first_letters.get(letter, 0)
    if count > 0:
        bar = '█' * int(count / 2)
        print(f"{letter}: {count:3d} {bar}")

print(f"\nFirst 20 symbols: {symbols[:20]}")
print(f"\nLast 20 symbols: {symbols[-20:]}")

# Verify some known S&P 500 stocks are included
known = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V", "WMT"]
found = [s for s in known if s in symbols]
print(f"\nVerified {len(found)}/{len(known)} known S&P 500 stocks: {found}")
