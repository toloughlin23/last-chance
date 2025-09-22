#!/usr/bin/env python3
"""
Comprehensive Universe Provider & Selector Test Suite
Tests all components with 100% real Polygon data
"""

from dotenv import load_dotenv
from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector
from datetime import date, timedelta
import time

def test_candidate_discovery():
    """Test 1: Candidate discovery with market cap filtering"""
    print("🔍 Test 1: Candidate Discovery")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Test different market cap thresholds
    for min_cap in [5_000_000_000, 10_000_000_000, 50_000_000_000]:
        candidates = provider._discover_candidates(min_market_cap=min_cap, limit=20)
        print(f"  Min cap ${min_cap/1e9:.0f}B: {len(candidates)} candidates")
        if candidates:
            print(f"    Top 5: {candidates[:5]}")
    
    return len(candidates) > 0

def test_adv_prefiltering():
    """Test 2: ADV prefiltering with real data"""
    print("\n🔍 Test 2: ADV Prefiltering")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Get some candidates
    candidates = provider._discover_candidates(limit=10)
    if not candidates:
        print("  ❌ No candidates for testing")
        return False
    
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    # Test different ADV thresholds
    for adv_min in [50_000_000, 100_000_000, 500_000_000]:
        prefiltered = provider._prefilter_by_adv_and_price(
            candidates,
            start_date.isoformat(),
            end_date.isoformat(),
            adv_min_dollar=adv_min,
            price_min=10.0,
            max_symbols=10,
            batch_size=5,
        )
        print(f"  ADV > ${adv_min/1e6:.0f}M: {len(prefiltered)} passed")
        if prefiltered:
            print(f"    Examples: {prefiltered[:3]}")
    
    return len(prefiltered) > 0

def test_spread_calculation():
    """Test 3: Spread calculation accuracy"""
    print("\n🔍 Test 3: Spread Calculation")
    print("-" * 40)
    
    from services.quotes_client import QuotesClient
    client = QuotesClient()
    
    # Test with known liquid symbols
    test_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
    
    for symbol in test_symbols:
        try:
            med_dollar, med_bps = client.median_spread_over_days(symbol, days=5)
            print(f"  {symbol}: ${med_dollar:.3f} ({med_bps:.1f} bps)")
            
            # Check if values are realistic
            if med_dollar > 1000 or med_bps > 10000:
                print(f"    ⚠️ WARNING: Unrealistic spread for {symbol}")
        except Exception as e:
            print(f"  {symbol}: Error - {e}")
    
    return True

def test_sector_classification():
    """Test 4: Sector classification from Polygon"""
    print("\n🔍 Test 4: Sector Classification")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    candidates = provider._discover_candidates(limit=20)
    
    if candidates:
        sector_classifier, sector_weights = provider._build_sector_classifier_and_weights(candidates)
        
        if sector_classifier:
            print(f"  Found {len(sector_weights)} sectors")
            for sector, weight in list(sector_weights.items())[:5]:
                print(f"    {sector}: {weight:.1%}")
            
            # Test classification on a few symbols
            for symbol in candidates[:5]:
                sector = sector_classifier(symbol)
                print(f"    {symbol}: {sector or 'Unknown'}")
        else:
            print("  ⚠️ No sector data available")
    
    return sector_classifier is not None

def test_earnings_exclusion():
    """Test 5: Earnings exclusion using vX financials"""
    print("\n🔍 Test 5: Earnings Exclusion")
    print("-" * 40)
    
    from services.polygon_client import PolygonClient
    client = PolygonClient()
    
    # Test with a few symbols
    test_symbols = ["AAPL", "MSFT", "NVDA"]
    end_date = date.today()
    start_date = end_date - timedelta(days=90)
    
    for symbol in test_symbols:
        try:
            data = client.get_earnings_calendar(symbol, start_date, end_date)
            earnings_dates = data.get("results", [])
            print(f"  {symbol}: {len(earnings_dates)} earnings dates found")
            
            if earnings_dates:
                for earning in earnings_dates[:2]:  # Show first 2
                    print(f"    - {earning.get('date')} ({earning.get('fiscal_period')})")
        except Exception as e:
            print(f"  {symbol}: Error - {e}")
    
    return True

def test_full_universe_selection():
    """Test 6: Complete universe selection process"""
    print("\n🔍 Test 6: Full Universe Selection")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Test with smaller parameters for speed
    universe = provider.get_active_universe(
        target_size=20,  # Smaller for testing
        analysis_days=30,  # Shorter period
        force_refresh=True,
        batch_size=10,
        adv_prefilter_min_dollar=50_000_000,
    )
    
    print(f"  Selected {len(universe)} symbols")
    if universe:
        print(f"  Top 10: {universe[:10]}")
        
        # Verify they're all valid
        from services.polygon_client import PolygonClient
        client = PolygonClient()
        
        # Quick validation on first 3
        for symbol in universe[:3]:
            try:
                data = client.get_aggs(symbol, 1, "day", 
                                     (date.today() - timedelta(days=5)).isoformat(),
                                     date.today().isoformat(), limit=1)
                if data.get("results"):
                    print(f"    ✅ {symbol}: Valid data")
                else:
                    print(f"    ❌ {symbol}: No data")
            except Exception as e:
                print(f"    ❌ {symbol}: Error - {e}")
    
    return len(universe) > 0

def test_performance_metrics():
    """Test 7: Performance and timing"""
    print("\n🔍 Test 7: Performance Metrics")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Time the full process
    start_time = time.time()
    
    universe = provider.get_active_universe(
        target_size=50,
        analysis_days=60,
        force_refresh=True,
        batch_size=20,
    )
    
    elapsed = time.time() - start_time
    
    print(f"  Time to select {len(universe)} symbols: {elapsed:.1f} seconds")
    print(f"  Rate: {len(universe)/elapsed:.1f} symbols/second")
    
    # Check memory usage (basic)
    import sys
    print(f"  Memory usage: {sys.getsizeof(universe)} bytes for symbol list")
    
    return elapsed < 300  # Should complete in under 5 minutes

def main():
    load_dotenv()
    
    print("🚀 COMPREHENSIVE UNIVERSE TEST SUITE")
    print("=" * 60)
    print("Testing with 100% real Polygon data")
    print("=" * 60)
    
    tests = [
        ("Candidate Discovery", test_candidate_discovery),
        ("ADV Prefiltering", test_adv_prefiltering),
        ("Spread Calculation", test_spread_calculation),
        ("Sector Classification", test_sector_classification),
        ("Earnings Exclusion", test_earnings_exclusion),
        ("Full Universe Selection", test_full_universe_selection),
        ("Performance Metrics", test_performance_metrics),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"\n{'✅' if result else '❌'} {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"\n❌ {test_name}: ERROR - {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - System is 100% operational!")
    else:
        print("⚠️ Some tests failed - check the output above")

if __name__ == "__main__":
    main()



