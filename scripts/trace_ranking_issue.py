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
    
    training_logger.info("TRACING RANKING PROCESS", operation="enhanced_logging")
    training_logger.info("="*80, operation="enhanced_logging")
    training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    training_logger.info("="*80, operation="enhanced_logging")
    
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
    
    training_logger.info(f"\nTest symbols: {test_symbols}", operation="enhanced_logging")
    training_logger.info(f"First letters: {Counter(s[0] for s in test_symbols, operation="enhanced_logging")}")
    
    # Create provider
    provider = ActiveUniverseProvider()
    
    # Test the ranking function directly
    from datetime import date, timedelta
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    training_logger.info(f"\nCalling _rank_symbols_by_quality with {len(test_symbols, operation="enhanced_logging")} symbols...")
    
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
        
        training_logger.info(f"\nRanked output: {len(ranked, operation="enhanced_logging")} symbols")
        training_logger.info(f"Ranked symbols: {ranked}", operation="enhanced_logging")
        
        # Check first letters
        first_letters = Counter(s[0] for s in ranked)
        training_logger.info(f"First letters in ranked output: {dict(first_letters, operation="enhanced_logging")}")
        
        # The issue is clear if only A's come out even with diverse input
        
    except Exception as e:
        training_logger.error(f"Error in ranking: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()
    
    # Now let's check what the actual Top 10 print statement shows
    training_logger.info("\n\nChecking the 'Top 10' output...", operation="enhanced_logging")
    training_logger.info("If this shows all A's even with diverse input, the issue is in the ranking logic", operation="enhanced_logging")


def check_ranking_algorithm():
    """Check if the ranking algorithm has an inherent bias."""
    
    training_logger.info("\n\nCHECKING RANKING ALGORITHM", operation="enhanced_logging")
    training_logger.info("="*80, operation="enhanced_logging")
    
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
        training_logger.info("\nFound top_candidates assignment:", operation="enhanced_logging")
        for match in matches:
            training_logger.info(f"  {match}", operation="enhanced_logging")
    
    # Look for where Top 10 is printed
    pattern = r'.*Top 10:.*'
    matches = re.findall(pattern, content)
    
    if matches:
        training_logger.info("\nFound 'Top 10' print statement:", operation="enhanced_logging")
        for match in matches:
            training_logger.info(f"  {match.strip(, operation="enhanced_logging")}")
    
    # Check if there's a sort by symbol name anywhere
    pattern = r'sorted.*key=.*symbol.*'
    matches = re.findall(pattern, content, re.IGNORECASE)
    
    if matches:
        training_logger.warning("\n⚠️ Found sorting by symbol name:", operation="enhanced_logging")
        for match in matches:
            training_logger.info(f"  {match.strip(, operation="enhanced_logging")}")


def test_with_known_good_symbols():
    """Test with symbols we KNOW should rank well."""
    
    training_logger.info("\n\nTESTING WITH KNOWN HIGH-QUALITY SYMBOLS", operation="enhanced_logging")
    training_logger.info("="*80, operation="enhanced_logging")
    
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
    
    training_logger.info(f"Testing with known high-quality symbols: {high_quality}", operation="enhanced_logging")
    
    # If the ranking works correctly, these should all pass quality filters
    # and maintain diversity in the output


if __name__ == "__main__":
    # First trace the ranking process
    trace_ranking_process()
    
    # Then check the algorithm
    check_ranking_algorithm()
    
    # Test with known good symbols
    test_with_known_good_symbols()
    
    training_logger.info("\n\nCONCLUSION:", operation="enhanced_logging")
    training_logger.info("="*80, operation="enhanced_logging")
    training_logger.info("If diverse input produces only A's in output, the issue is in:", operation="enhanced_logging")
    training_logger.info("1. The ranking algorithm itself", operation="enhanced_logging")
    training_logger.info("2. How candidates are selected from ranked_data", operation="enhanced_logging")
    training_logger.info("3. A hidden alphabetical sort somewhere", operation="enhanced_logging")
    training_logger.info("\n100% GENUINE SYSTEM REQUIRES GENUINE DIVERSITY!", operation="enhanced_logging")


