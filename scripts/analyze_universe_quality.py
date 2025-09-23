"""
Analyze the quality of the generated universe symbols
"""
import os
import sys
import json
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any

# Load environment
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient

def analyze_universe_quality():
    """Analyze the quality of the current 50 candidates from provider."""
    
    print("🔍 ANALYZING CURRENT 50 CANDIDATES QUALITY")
    print("="*60)
    print("🎯 Checking if candidates match Option B: Growth-Oriented (Aggressive)")
    print("="*60)
    
    # Get the current 50 candidates from provider instead of old universe file
    from utils.active_universe_provider import ActiveUniverseProvider
    from datetime import date, timedelta
    
    provider = ActiveUniverseProvider()
    
    print("📊 Getting current 50 top-ranked candidates from provider...")
    
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    # Get ranked candidates
    ranked_candidates = provider._discover_and_rank_candidates(
        min_market_cap=10_000_000_000,
        analysis_days=60,
        start_date=start_date,
        end_date=end_date,
        max_candidates=50,
        batch_size=10
    )
    
    symbols = ranked_candidates[:50]  # Take top 50
    print(f"📊 Analyzing {len(symbols)} current candidates from provider")
    print(f"📈 Top 10: {symbols[:10]}")
    
    if not symbols:
        print("❌ No symbols found in universe")
        return
    
    # Initialize clients
    polygon_client = PolygonClient()
    quotes_client = QuotesClient()
    
    # 1. Letter Distribution Analysis
    print("\n1️⃣ LETTER DISTRIBUTION")
    print("-" * 30)
    first_letters = Counter(s[0].upper() for s in symbols)
    total_letters = len([l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if first_letters.get(l, 0) > 0])
    
    print(f"   Letters represented: {total_letters}/26")
    print(f"   Distribution:")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        count = first_letters.get(letter, 0)
        if count > 0:
            pct = (count / len(symbols)) * 100
            bar = '█' * int(pct / 2)
            print(f"     {letter}: {count:2d} ({pct:4.1f}%) {bar}")
    
    # 2. Market Cap Analysis
    print("\n2️⃣ MARKET CAP ANALYSIS")
    print("-" * 30)
    market_caps = []
    missing_mcaps = []
    
    for symbol in symbols:
        try:
            details = polygon_client.get_ticker_details(symbol)
            if details and details.get("results"):
                mcap = details["results"].get("market_cap", 0)
                if mcap > 0:
                    market_caps.append(mcap)
                else:
                    missing_mcaps.append(symbol)
            else:
                missing_mcaps.append(symbol)
        except Exception:
            missing_mcaps.append(symbol)
    
    if market_caps:
        market_caps.sort(reverse=True)
        min_mcap = min(market_caps) / 1e9
        max_mcap = max(market_caps) / 1e9
        median_mcap = market_caps[len(market_caps)//2] / 1e9
        avg_mcap = sum(market_caps) / len(market_caps) / 1e9
        
        print(f"   Market caps found: {len(market_caps)}/{len(symbols)}")
        print(f"   Min: ${min_mcap:.1f}B")
        print(f"   Max: ${max_mcap:.1f}B") 
        print(f"   Median: ${median_mcap:.1f}B")
        print(f"   Average: ${avg_mcap:.1f}B")
        
        # Check S&P 500 threshold
        sp500_count = sum(1 for mcap in market_caps if mcap >= 8e9)
        print(f"   S&P 500 size (≥$8B): {sp500_count}/{len(market_caps)} ({sp500_count/len(market_caps)*100:.1f}%)")
    
    if missing_mcaps:
        print(f"   Missing market caps: {missing_mcaps[:5]}{'...' if len(missing_mcaps) > 5 else ''}")
    
    # 3. Sector Analysis
    print("\n3️⃣ SECTOR ANALYSIS")
    print("-" * 30)
    sectors = {}
    missing_sectors = []
    
    for symbol in symbols:
        try:
            details = polygon_client.get_ticker_details(symbol)
            if details and details.get("results"):
                sector = details["results"].get("sic_description", "Unknown")
                if sector and sector != "Unknown":
                    sectors[symbol] = sector
                else:
                    missing_sectors.append(symbol)
            else:
                missing_sectors.append(symbol)
        except Exception:
            missing_sectors.append(symbol)
    
    if sectors:
        sector_counts = Counter(sectors.values())
        print(f"   Sectors found: {len(sector_counts)} unique sectors")
        print(f"   Top sectors:")
        for sector, count in sector_counts.most_common(10):
            pct = (count / len(sectors)) * 100
            print(f"     {sector}: {count} ({pct:.1f}%)")
    
    if missing_sectors:
        print(f"   Missing sectors: {len(missing_sectors)} symbols")
    
    # 4. Liquidity Analysis (Sample)
    print("\n4️⃣ LIQUIDITY ANALYSIS (Sample)")
    print("-" * 30)
    sample_symbols = symbols[:10]  # Check first 10 for speed
    liquidity_data = []
    
    for symbol in sample_symbols:
        try:
            # Get recent price data for ADV
            from datetime import date, timedelta
            end_date = date.today()
            start_date = end_date - timedelta(days=30)
            
            price_data = polygon_client.get_aggs(
                symbol, 1, "day", 
                start_date.isoformat(), end_date.isoformat(),
                limit=20, adjusted=True
            )
            
            if price_data and price_data.get("results"):
                results = price_data["results"]
                total_volume = sum(float(r.get("v", 0)) for r in results)
                avg_price = sum(float(r.get("c", 0)) for r in results) / len(results)
                adv = (total_volume * avg_price) / len(results)
                
                # Get spread data
                try:
                    med_dollar, med_bps = quotes_client.median_spread_over_days(symbol, days=5)
                    liquidity_data.append({
                        'symbol': symbol,
                        'adv_millions': adv / 1e6,
                        'spread_bps': med_bps,
                        'spread_dollar': med_dollar
                    })
                except Exception:
                    liquidity_data.append({
                        'symbol': symbol,
                        'adv_millions': adv / 1e6,
                        'spread_bps': 'N/A',
                        'spread_dollar': 'N/A'
                    })
        except Exception:
            continue
    
    if liquidity_data:
        print(f"   Sample size: {len(liquidity_data)} symbols")
        print(f"   ADV range: ${min(d['adv_millions'] for d in liquidity_data):.1f}M - ${max(d['adv_millions'] for d in liquidity_data):.1f}M")
        
        valid_spreads = [d for d in liquidity_data if d['spread_bps'] != 'N/A']
        if valid_spreads:
            spread_bps = [d['spread_bps'] for d in valid_spreads]
            print(f"   Spread range: {min(spread_bps):.1f} - {max(spread_bps):.1f} bps")
        
        print(f"   Sample details:")
        for data in liquidity_data[:5]:
            print(f"     {data['symbol']}: ADV=${data['adv_millions']:.1f}M, Spread={data['spread_bps']}bps")
    
    # 5. Growth-Oriented Analysis (Option B)
    print("\n5️⃣ GROWTH-ORIENTED ANALYSIS (OPTION B)")
    print("-" * 30)
    
    # Get quality metrics for growth analysis
    growth_metrics = []
    for symbol in symbols[:20]:  # Analyze first 20 for speed
        try:
            metrics = provider._analyze_symbol_quality(
                symbol=symbol,
                start_date=start_date,
                end_date=end_date
            )
            if metrics:
                growth_metrics.append({
                    'symbol': symbol,
                    'atr_pct': metrics.get('atr_pct', 0),
                    'growth_potential': metrics.get('growth_potential', 0),
                    'breakout_potential': metrics.get('breakout_potential', 0),
                    'price_change_pct': metrics.get('price_change_pct', 0),
                    'adv': metrics.get('adv', 0)
                })
        except Exception:
            continue
    
    if growth_metrics:
        high_volatility_count = sum(1 for m in growth_metrics if m['atr_pct'] >= 0.03)  # 3%+
        high_growth_count = sum(1 for m in growth_metrics if m['growth_potential'] >= 0.7)
        good_adv_count = sum(1 for m in growth_metrics if m['adv'] >= 50_000_000)  # $50M+
        positive_momentum_count = sum(1 for m in growth_metrics if m['price_change_pct'] > 0)
        
        print(f"   High Volatility (ATR% ≥ 3%): {high_volatility_count}/{len(growth_metrics)} ({high_volatility_count/len(growth_metrics)*100:.1f}%)")
        print(f"   High Growth Potential (≥0.7): {high_growth_count}/{len(growth_metrics)} ({high_growth_count/len(growth_metrics)*100:.1f}%)")
        print(f"   Good Liquidity (ADV ≥ $50M): {good_adv_count}/{len(growth_metrics)} ({good_adv_count/len(growth_metrics)*100:.1f}%)")
        print(f"   Positive Momentum: {positive_momentum_count}/{len(growth_metrics)} ({positive_momentum_count/len(growth_metrics)*100:.1f}%)")
        
        # Check if matches Option B criteria
        if high_volatility_count >= len(growth_metrics) * 0.6 and high_growth_count >= len(growth_metrics) * 0.4:
            print(f"   🎉 EXCELLENT! Candidates match Option B (Growth-Oriented) criteria!")
        elif high_volatility_count >= len(growth_metrics) * 0.4:
            print(f"   ✅ GOOD! Candidates mostly match Option B criteria")
        else:
            print(f"   ⚠️  MIXED! Some candidates match Option B, but could be more aggressive")
    
    # 6. Quality Summary
    print("\n6️⃣ QUALITY SUMMARY")
    print("-" * 30)
    
    quality_score = 0
    max_score = 5
    
    # Letter diversity (1 point)
    if total_letters >= 15:
        quality_score += 1
        print("   ✅ Good letter diversity")
    else:
        print(f"   ⚠️ Limited letter diversity ({total_letters}/26)")
    
    # Market cap quality (1 point)
    if market_caps and len(market_caps) >= len(symbols) * 0.8:
        quality_score += 1
        print("   ✅ Good market cap coverage")
    else:
        print("   ⚠️ Missing market cap data")
    
    # S&P 500 size (1 point)
    if market_caps and sp500_count >= len(market_caps) * 0.7:
        quality_score += 1
        print("   ✅ Mostly S&P 500 size companies")
    else:
        print("   ⚠️ Many companies below S&P 500 threshold")
    
    # Sector diversity (1 point)
    if sectors and len(sector_counts) >= 5:
        quality_score += 1
        print("   ✅ Good sector diversity")
    else:
        print("   ⚠️ Limited sector diversity")
    
    # Liquidity (1 point)
    if liquidity_data and len(liquidity_data) >= 5:
        quality_score += 1
        print("   ✅ Good liquidity sample")
    else:
        print("   ⚠️ Limited liquidity data")
    
    print(f"\n🎯 OVERALL QUALITY SCORE: {quality_score}/{max_score}")
    
    if quality_score >= 4:
        print("   🏆 EXCELLENT: High-quality universe for training")
    elif quality_score >= 3:
        print("   ✅ GOOD: Solid universe for training")
    else:
        print("   ⚠️ NEEDS IMPROVEMENT: Consider regenerating universe")

if __name__ == "__main__":
    analyze_universe_quality()
