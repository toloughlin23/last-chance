"""
COMPREHENSIVE UNIVERSE SYSTEM AUDIT
===================================

This script audits every stage of the universe selection pipeline to identify
where alphabetical bias and other issues are introduced.

WHAT THE SYSTEM SHOULD DO:
1. Provider discovers ALL S&P 500 symbols (500+ tickers)
2. Provider ranks them by quality metrics (ADV, spreads, ATR%, stability)
3. Provider outputs top 200-300 diverse candidates
4. Selector applies strict filters (price, ATR, ADV, spreads)
5. Selector ranks and selects 120-150 high-quality diverse symbols
6. Final universe should have symbols starting with all letters A-Z

NO SHORTCUTS, 100% GENUINE DATA, NO MOCKS, NO PLACEHOLDERS
"""

import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector


def analyze_symbol_distribution(symbols: List[str], stage: str) -> Dict[str, int]:
    """Analyze first-letter distribution of symbols."""
    print(f"\n{'='*60}")
    print(f"STAGE: {stage}")
    print(f"Total symbols: {len(symbols)}")
    
    if not symbols:
        print("⚠️ NO SYMBOLS!")
        return {}
    
    # First letter distribution
    first_letters = Counter(s[0].upper() for s in symbols if s)
    
    # Show distribution
    print("\nFirst-letter distribution:")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        count = first_letters.get(letter, 0)
        if count > 0:
            pct = 100.0 * count / len(symbols)
            bar = '█' * int(pct / 2)
            print(f"{letter}: {count:3d} ({pct:5.1f}%) {bar}")
    
    # Show first 20 and last 20
    print(f"\nFirst 20: {symbols[:20]}")
    print(f"Last 20: {symbols[-20:]}")
    
    # Detect bias
    if len(symbols) >= 20:
        a_count = first_letters.get('A', 0)
        a_pct = 100.0 * a_count / len(symbols)
        if a_pct > 25:
            print(f"\n🚨 ALPHABETICAL BIAS DETECTED! {a_pct:.1f}% start with 'A'")
    
    return dict(first_letters)


def audit_provider_discovery():
    """Audit Step 1: How provider discovers candidates."""
    print("\n" + "="*80)
    print("AUDIT 1: PROVIDER DISCOVERY")
    print("="*80)
    
    client = PolygonClient()
    
    # Test get_tickers
    print("\n1.1 Testing get_tickers endpoint...")
    try:
        data = client.get_tickers(market="stocks", active=True, limit=500)
        results = data.get("results", [])
        print(f"✅ Got {len(results)} tickers from Polygon")
        
        # Extract symbols
        symbols = [t.get("ticker") for t in results if isinstance(t.get("ticker"), str)]
        print(f"✅ Extracted {len(symbols)} valid symbols")
        
        # Analyze distribution
        analyze_symbol_distribution(symbols, "RAW POLYGON TICKERS")
        
        return symbols
        
    except Exception as e:
        print(f"❌ Error in get_tickers: {e}")
        return []


def audit_provider_ranking(symbols: List[str]):
    """Audit Step 2: How provider ranks candidates."""
    print("\n" + "="*80)
    print("AUDIT 2: PROVIDER RANKING")
    print("="*80)
    
    provider = ActiveUniverseProvider()
    
    # Check if provider sorts alphabetically somewhere
    print("\n2.1 Checking provider's _rank_symbols_by_quality method...")
    
    # Mock dates
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    # Test with first 50 symbols
    test_symbols = symbols[:50]
    print(f"\nTesting with {len(test_symbols)} symbols...")
    
    try:
        # This is where ranking happens
        ranked = provider._rank_symbols_by_quality(
            test_symbols,
            min_market_cap=100_000_000,
            analysis_days=60,
            start_date=start_date,
            end_date=end_date,
            max_candidates=200,
            batch_size=10
        )
        
        print(f"✅ Ranked {len(ranked)} symbols")
        analyze_symbol_distribution(ranked, "PROVIDER RANKED OUTPUT")
        
        return ranked
        
    except Exception as e:
        print(f"❌ Error in ranking: {e}")
        return []


def audit_full_pipeline():
    """Audit the complete pipeline end-to-end."""
    print("\n" + "="*80)
    print("AUDIT 3: FULL PIPELINE")
    print("="*80)
    
    provider = ActiveUniverseProvider()
    
    # Run provider's discover_and_rank_candidates
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    print("\n3.1 Running provider._discover_and_rank_candidates...")
    candidates = provider._discover_and_rank_candidates(
        min_market_cap=100_000_000,
        analysis_days=60,
        start_date=start_date,
        end_date=end_date,
        max_candidates=200,
        batch_size=10
    )
    
    analyze_symbol_distribution(candidates, "PROVIDER CANDIDATES")
    
    if len(candidates) < 100:
        print(f"\n⚠️ Provider only produced {len(candidates)} candidates!")
        print("This is the PRIMARY ISSUE - provider should produce 200-300 candidates")
    
    # Now run selector
    print("\n3.2 Running UniverseSelector.select_universe...")
    selector = UniverseSelector()
    
    selected = selector.select_universe(
        candidates=candidates,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        target_size=120,
        target_max_size=150,
        min_price=10.0,
        min_atr_pct=0.01,
        max_atr_pct=0.05,
        adv_min_dollar=50_000_000.0,
        spread_filter_enabled=True,
        spread_max_dollars=0.02,
        spread_max_bps=5.0
    )
    
    analyze_symbol_distribution(selected, "SELECTOR OUTPUT")
    
    return candidates, selected


def check_for_hidden_sorts():
    """Check if there are any hidden alphabetical sorts in the code."""
    print("\n" + "="*80)
    print("AUDIT 4: CHECKING FOR HIDDEN SORTS")
    print("="*80)
    
    # Read provider code
    provider_file = Path("utils/active_universe_provider.py")
    with open(provider_file, 'r') as f:
        provider_code = f.read()
    
    # Look for sorts
    import re
    sort_patterns = [
        r'\.sort\(',
        r'sorted\(',
        r'\.sort\s*\(',
        r'sorted\s*\('
    ]
    
    print("\n4.1 Searching for sort operations in provider...")
    for pattern in sort_patterns:
        matches = re.findall(f'.*{pattern}.*', provider_code)
        if matches:
            print(f"\nFound {len(matches)} sort operations:")
            for match in matches[:5]:  # Show first 5
                print(f"  {match.strip()}")
    
    # Check where Top 10 is printed
    print("\n4.2 Finding where 'Top 10' is printed...")
    top_10_matches = re.findall(r'.*Top 10.*', provider_code)
    for match in top_10_matches:
        print(f"  {match.strip()}")


def main():
    """Run comprehensive audit."""
    print("COMPREHENSIVE UNIVERSE SYSTEM AUDIT")
    print("===================================")
    print("\nWHAT THE SYSTEM SHOULD DO:")
    print("1. Provider: Discover 500+ S&P 500 symbols")
    print("2. Provider: Rank by quality metrics")
    print("3. Provider: Output 200-300 diverse candidates")
    print("4. Selector: Apply strict filters")
    print("5. Selector: Select 120-150 diverse symbols")
    print("6. Result: Symbols from A-Z, no alphabetical bias")
    
    # Step 1: Audit discovery
    raw_symbols = audit_provider_discovery()
    
    if len(raw_symbols) < 100:
        print("\n❌ CRITICAL: Not enough symbols from Polygon!")
        return
    
    # Step 2: Audit ranking
    ranked_subset = audit_provider_ranking(raw_symbols[:50])
    
    # Step 3: Audit full pipeline
    candidates, selected = audit_full_pipeline()
    
    # Step 4: Check for hidden sorts
    check_for_hidden_sorts()
    
    # Summary
    print("\n" + "="*80)
    print("AUDIT SUMMARY")
    print("="*80)
    print(f"\n1. Raw Polygon symbols: {len(raw_symbols)}")
    print(f"2. Provider candidates: {len(candidates)}")
    print(f"3. Final selected: {len(selected)}")
    
    if len(candidates) < 100:
        print("\n🚨 ROOT CAUSE: Provider is not producing enough candidates!")
        print("   Expected: 200-300 candidates")
        print(f"   Actual: {len(candidates)} candidates")
        print("\n   This forces selector to work with limited, biased input")
    
    if all(c[0] == 'A' for c in candidates[:10]):
        print("\n🚨 BIAS SOURCE: Provider output is alphabetically biased!")
        print("   The ranking algorithm is not properly randomizing")


if __name__ == "__main__":
    main()

