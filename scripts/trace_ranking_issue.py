"""
TRACE THE RANKING ISSUE
=======================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Even with alphabetical input, the ranking should produce diverse output.
Let's trace why it's not working.
"""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient
from utils.active_universe_provider import ActiveUniverseProvider


def trace_ranking_process():
    """Trace exactly what happens in the ranking process."""
    
    print("TRACING RANKING PROCESS")
    print("="*80)
    print("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER")
    print("="*80)
    
    # Get some test symbols - mix of A's and others
    test_symbols = [
        # Some A's
        "AAPL", "AMD", "AMZN", "ABBV", "ABT",
        # Tech giants (non-A)
        "MSFT", "GOOGL", "META", "NVDA", "TSLA",
        # Financials (non-A)
        "JPM", "BAC", "GS", "MS", "WFC",
        # Healthcare (non-A)
        "JNJ", "UNH", "PFE", "LLY", "MRK",
        # Other sectors (non-A)
        "WMT", "HD", "PG", "KO", "DIS"
    ]
    
    print(f"\nTest symbols: {test_symbols}")
    print(f"First letters: {Counter(s[0] for s in test_symbols)}")
    
    # Create provider
    provider = ActiveUniverseProvider()
    
    # Test the ranking function directly
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    print(f"\nCalling _rank_symbols_by_quality with {len(test_symbols)} symbols...")
    
    try:
        # First, let's see what happens with our diverse test set
        ranked = provider._rank_symbols_by_quality(
            test_symbols,
            min_market_cap=100_000_000,  # Low threshold
            analysis_days=60,
            start_date=start_date,
            end_date=end_date,
            max_candidates=30,  # Get all
            batch_size=5
        )
        
        print(f"\nRanked output: {len(ranked)} symbols")
        print(f"Ranked symbols: {ranked}")
        
        # Check first letters
        first_letters = Counter(s[0] for s in ranked)
        print(f"First letters in ranked output: {dict(first_letters)}")
        
        # The issue is clear if only A's come out even with diverse input
        
    except Exception as e:
        print(f"Error in ranking: {e}")
        import traceback
        traceback.print_exc()
    
    # Now let's check what the actual Top 10 print statement shows
    print("\n\nChecking the 'Top 10' output...")
    print("If this shows all A's even with diverse input, the issue is in the ranking logic")


def check_ranking_algorithm():
    """Check if the ranking algorithm has an inherent bias."""
    
    print("\n\nCHECKING RANKING ALGORITHM")
    print("="*80)
    
    # Read the provider code
    provider_file = Path("utils/active_universe_provider.py")
    with open(provider_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find where top_candidates is created
    import re
    
    # Look for the line that creates top_candidates
    pattern = r'top_candidates\s*=.*'
    matches = re.findall(pattern, content)
    
    if matches:
        print("\nFound top_candidates assignment:")
        for match in matches:
            print(f"  {match}")
    
    # Look for where Top 10 is printed
    pattern = r'.*Top 10:.*'
    matches = re.findall(pattern, content)
    
    if matches:
        print("\nFound 'Top 10' print statement:")
        for match in matches:
            print(f"  {match.strip()}")
    
    # Check if there's a sort by symbol name anywhere
    pattern = r'sorted.*key=.*symbol.*'
    matches = re.findall(pattern, content, re.IGNORECASE)
    
    if matches:
        print("\n⚠️ Found sorting by symbol name:")
        for match in matches:
            print(f"  {match.strip()}")


def test_with_known_good_symbols():
    """Test with symbols we KNOW should rank well."""
    
    print("\n\nTESTING WITH KNOWN HIGH-QUALITY SYMBOLS")
    print("="*80)
    
    # These are known high-quality S&P 500 stocks
    high_quality = [
        "MSFT",  # Huge volume, tight spreads
        "AAPL",  # Huge volume, tight spreads
        "GOOGL", # High volume
        "JPM",   # High volume financial
        "TSLA",  # High volume, higher volatility
        "NVDA",  # High volume tech
        "META",  # High volume
        "BRK.B", # Berkshire
        "UNH",   # Healthcare giant
        "WMT"    # Retail giant
    ]
    
    print(f"Testing with known high-quality symbols: {high_quality}")
    
    # If the ranking works correctly, these should all pass quality filters
    # and maintain diversity in the output


if __name__ == "__main__":
    # First trace the ranking process
    trace_ranking_process()
    
    # Then check the algorithm
    check_ranking_algorithm()
    
    # Test with known good symbols
    test_with_known_good_symbols()
    
    print("\n\nCONCLUSION:")
    print("="*80)
    print("If diverse input produces only A's in output, the issue is in:")
    print("1. The ranking algorithm itself")
    print("2. How candidates are selected from ranked_data")
    print("3. A hidden alphabetical sort somewhere")
    print("\n100% GENUINE SYSTEM REQUIRES GENUINE DIVERSITY!")

