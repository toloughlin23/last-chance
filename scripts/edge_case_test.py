#!/usr/bin/env python3
"""
Edge Case Testing for Universe Provider & Selector
Tests error handling, rate limits, and edge cases
"""

from dotenv import load_dotenv
from utils.active_universe_provider import ActiveUniverseProvider
from utils.universe_selector import UniverseSelector
from datetime import date, timedelta
import time

def test_empty_candidates():
    """Test: What happens with empty candidate list"""
    print("🔍 Edge Case 1: Empty Candidates")
    print("-" * 40)
    
    selector = UniverseSelector()
    
    # Test with empty list
    result = selector.select_universe(
        candidates=[],
        target_size=10,
        analysis_days=30,
    )
    
    print(f"  Empty candidates → {len(result)} symbols selected")
    return len(result) == 0

def test_insufficient_candidates():
    """Test: What happens when candidates < target_size"""
    print("\n🔍 Edge Case 2: Insufficient Candidates")
    print("-" * 40)
    
    selector = UniverseSelector()
    
    # Test with only 3 candidates but target of 10
    result = selector.select_universe(
        candidates=["AAPL", "MSFT", "NVDA"],
        target_size=10,
        analysis_days=30,
    )
    
    print(f"  3 candidates, target 10 → {len(result)} symbols selected")
    return len(result) == 3

def test_all_candidates_filtered_out():
    """Test: What happens when all candidates fail filters"""
    print("\n🔍 Edge Case 3: All Candidates Filtered Out")
    print("-" * 40)
    
    selector = UniverseSelector()
    
    # Use very strict filters to eliminate everything
    result = selector.select_universe(
        candidates=["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"],
        target_size=10,
        analysis_days=30,
        min_adv_dollars=1_000_000_000_000,  # $1T ADV (impossible)
        min_price=10000,  # $10k price (impossible)
        min_atr_pct=50,  # 50% ATR (impossible)
        max_spread_dollars=0.001,  # 0.1 cent spread (impossible)
    )
    
    print(f"  Impossible filters → {len(result)} symbols selected")
    return len(result) == 0

def test_weekend_data():
    """Test: Behavior on weekends when markets are closed"""
    print("\n🔍 Edge Case 4: Weekend Data Handling")
    print("-" * 40)
    
    from services.quotes_client import QuotesClient
    client = QuotesClient()
    
    # Test spread calculation on weekend
    today = date.today()
    weekend_days = []
    
    # Find a recent weekend
    for i in range(7):
        test_date = today - timedelta(days=i)
        if test_date.weekday() >= 5:  # Saturday or Sunday
            weekend_days.append(test_date)
    
    if weekend_days:
        test_date = weekend_days[0]
        print(f"  Testing weekend data for {test_date}")
        
        try:
            med_dollar, med_bps = client.median_spread_over_days("AAPL", days=1, end_date=test_date)
            print(f"    Weekend spread: ${med_dollar:.3f} ({med_bps:.1f} bps)")
            
            # Should handle gracefully (not crash)
            return True
        except Exception as e:
            print(f"    Weekend error: {e}")
            return False
    else:
        print("  No recent weekend found for testing")
        return True

def test_api_rate_limits():
    """Test: Behavior under API rate limiting"""
    print("\n🔍 Edge Case 5: API Rate Limiting")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Test with very large batch to potentially hit rate limits
    start_time = time.time()
    
    try:
        universe = provider.get_active_universe(
            target_size=200,  # Large target
            analysis_days=60,
            force_refresh=True,
            batch_size=50,  # Large batches
        )
        
        elapsed = time.time() - start_time
        print(f"  Large batch completed in {elapsed:.1f}s")
        print(f"  Selected {len(universe)} symbols")
        
        # Check if we got reasonable results despite potential rate limits
        return len(universe) > 0
        
    except Exception as e:
        print(f"  Rate limit error: {e}")
        return False

def test_missing_polygon_key():
    """Test: Behavior without POLYGON_API_KEY"""
    print("\n🔍 Edge Case 6: Missing API Key")
    print("-" * 40)
    
    import os
    original_key = os.environ.get("POLYGON_API_KEY")
    
    try:
        # Temporarily remove the key
        if "POLYGON_API_KEY" in os.environ:
            del os.environ["POLYGON_API_KEY"]
        
        provider = ActiveUniverseProvider()
        
        # This should fail gracefully
        universe = provider.get_active_universe(
            target_size=10,
            analysis_days=30,
            force_refresh=True,
        )
        
        print(f"  No API key → {len(universe)} symbols (should be 0)")
        return len(universe) == 0
        
    except Exception as e:
        print(f"  Expected error without API key: {e}")
        return True
    finally:
        # Restore the key
        if original_key:
            os.environ["POLYGON_API_KEY"] = original_key

def test_invalid_symbols():
    """Test: Behavior with invalid/non-existent symbols"""
    print("\n🔍 Edge Case 7: Invalid Symbols")
    print("-" * 40)
    
    selector = UniverseSelector()
    
    # Mix of valid and invalid symbols
    mixed_candidates = ["AAPL", "INVALID123", "MSFT", "FAKESYMBOL", "NVDA"]
    
    result = selector.select_universe(
        candidates=mixed_candidates,
        target_size=10,
        analysis_days=30,
    )
    
    print(f"  Mixed valid/invalid → {len(result)} symbols selected")
    print(f"  Selected: {result}")
    
    # Should only return valid symbols
    valid_symbols = ["AAPL", "MSFT", "NVDA"]
    return all(symbol in valid_symbols for symbol in result)

def test_extreme_parameters():
    """Test: Behavior with extreme parameter values"""
    print("\n🔍 Edge Case 8: Extreme Parameters")
    print("-" * 40)
    
    provider = ActiveUniverseProvider()
    
    # Test with extreme values
    try:
        universe = provider.get_active_universe(
            target_size=1,  # Very small target
            analysis_days=1,  # Very short analysis
            force_refresh=True,
            batch_size=1,  # Very small batch
        )
        
        print(f"  Extreme params → {len(universe)} symbols")
        return True
        
    except Exception as e:
        print(f"  Extreme params error: {e}")
        return False

def main():
    load_dotenv()
    
    print("🚀 EDGE CASE TEST SUITE")
    print("=" * 60)
    print("Testing error handling and edge cases")
    print("=" * 60)
    
    tests = [
        ("Empty Candidates", test_empty_candidates),
        ("Insufficient Candidates", test_insufficient_candidates),
        ("All Filtered Out", test_all_candidates_filtered_out),
        ("Weekend Data", test_weekend_data),
        ("API Rate Limits", test_api_rate_limits),
        ("Missing API Key", test_missing_polygon_key),
        ("Invalid Symbols", test_invalid_symbols),
        ("Extreme Parameters", test_extreme_parameters),
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
    print("EDGE CASE SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nOverall: {passed}/{total} edge cases handled correctly")
    
    if passed == total:
        print("🎉 ALL EDGE CASES HANDLED - System is robust!")
    else:
        print("⚠️ Some edge cases need attention")

if __name__ == "__main__":
    main()



