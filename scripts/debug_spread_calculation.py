#!/usr/bin/env python3
"""Debug why spread calculation is still failing"""

from dotenv import load_dotenv
from services.quotes_client import QuotesClient
from datetime import datetime, timedelta, timezone

def main():
    load_dotenv()
    
    client = QuotesClient()
    
    # Test the median_spread_over_days method step by step
    symbol = "AAPL"
    days = 5
    core_hours_only = True
    
    print(f"Debugging median_spread_over_days for {symbol}")
    print("=" * 60)
    
    end = datetime.now(timezone.utc)
    medians = []
    
    for i in range(1, days + 1):
        day_end = end - timedelta(days=i - 1)
        day_start = day_end.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Skip weekends
        if day_start.weekday() >= 5:
            print(f"\nDay {i}: {day_start.date()} - WEEKEND (skipped)")
            continue
            
        if core_hours_only:
            start_utc = day_start.replace(hour=13, minute=30)
            end_utc = day_start.replace(hour=20, minute=0)
        else:
            start_utc = day_start
            end_utc = day_start.replace(hour=23, minute=59, second=59)
            
        print(f"\nDay {i}: {day_start.date()}")
        print(f"  Window: {start_utc} to {end_utc}")
        
        quotes = client.fetch_quotes_window(symbol, start_utc, end_utc, limit=1000)
        print(f"  Quotes fetched: {len(quotes)}")
        
        if quotes:
            # Check the structure
            print(f"  First quote keys: {list(quotes[0].keys())}")
            
            # Show a few quotes
            for j, q in enumerate(quotes[:3]):
                bid = q.get('bid_price', 'N/A')
                ask = q.get('ask_price', 'N/A') 
                print(f"    Quote {j+1}: bid={bid}, ask={ask}")
        
        day_median = client.compute_median_spreads(quotes)
        medians.append(day_median)
        print(f"  Day median: ${day_median[0]:.3f} ({day_median[1]:.1f} bps)")
    
    # Compute final median
    if medians:
        dollar = sorted([m[0] for m in medians])
        bps = sorted([m[1] for m in medians])
        final_dollar = dollar[len(dollar) // 2]
        final_bps = bps[len(bps) // 2]
        
        print(f"\nFinal 5-day median: ${final_dollar:.3f} ({final_bps:.1f} bps)")
        
        if final_dollar > 1000:
            print("\n⚠️ Problem: Still getting unrealistic spreads!")
            print("   This happens when some days have no valid quotes")
            print("   Check if we're hitting weekends or holidays")

if __name__ == "__main__":
    main()



