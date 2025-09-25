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
    
    universe_logger.info("🔍 ANALYZING CURRENT 50 CANDIDATES QUALITY", operation="enhanced_logging")
    universe_logger.info("="*60, operation="enhanced_logging")
    universe_logger.info("🎯 Checking if candidates match Option B: Growth-Oriented (Aggressive, operation="enhanced_logging")")
    universe_logger.info("="*60, operation="enhanced_logging")
    
    # Get the current 50 candidates from provider instead of old universe file
    from utils.active_universe_provider import ActiveUniverseProvider
    from datetime import date, timedelta
    
    provider = ActiveUniverseProvider()
    
    universe_logger.info("📊 Getting current 50 top-ranked candidates from provider...", operation="enhanced_logging")
    
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
    universe_logger.info(f"📊 Analyzing {len(symbols, operation="enhanced_logging")} current candidates from provider")
    universe_logger.info(f"📈 Top 10: {symbols[:10]}", operation="enhanced_logging")
    
    if not symbols:
        universe_logger.error("❌ No symbols found in universe", operation="enhanced_logging")
        return
    
    # Initialize clients
    polygon_client = PolygonClient()
    quotes_client = QuotesClient()
    
    # 1. Letter Distribution Analysis
    universe_logger.info("\n1️⃣ LETTER DISTRIBUTION", operation="enhanced_logging")
    universe_logger.info("-" * 30, operation="enhanced_logging")
    first_letters = Counter(s[0].upper() for s in symbols)
    total_letters = len([l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if first_letters.get(l, 0) > 0])
    
    universe_logger.info(f"   Letters represented: {total_letters}/26", operation="enhanced_logging")
    universe_logger.info(f"   Distribution:", operation="enhanced_logging")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        count = first_letters.get(letter, 0)
        if count > 0:
            pct = (count / len(symbols)) * 100
            bar = '█' * int(pct / 2)
            universe_logger.info(f"     {letter}: {count:2d} ({pct:4.1f}%, operation="enhanced_logging") {bar}")
    
    # 2. Market Cap Analysis
    universe_logger.info("\n2️⃣ MARKET CAP ANALYSIS", operation="enhanced_logging")
    universe_logger.info("-" * 30, operation="enhanced_logging")
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
        
        universe_logger.info(f"   Market caps found: {len(market_caps, operation="enhanced_logging")}/{len(symbols)}")
        universe_logger.info(f"   Min: ${min_mcap:.1f}B", operation="enhanced_logging")
        universe_logger.info(f"   Max: ${max_mcap:.1f}B", operation="enhanced_logging") 
        universe_logger.info(f"   Median: ${median_mcap:.1f}B", operation="enhanced_logging")
        universe_logger.info(f"   Average: ${avg_mcap:.1f}B", operation="enhanced_logging")
        
        # Check S&P 500 threshold
        sp500_count = sum(1 for mcap in market_caps if mcap >= 8e9)
        universe_logger.info(f"   S&P 500 size (≥$8B, operation="enhanced_logging"): {sp500_count}/{len(market_caps)} ({sp500_count/len(market_caps)*100:.1f}%)")
    
    if missing_mcaps:
        universe_logger.info(f"   Missing market caps: {missing_mcaps[:5]}{'...' if len(missing_mcaps, operation="enhanced_logging") > 5 else ''}")
    
    # 3. Sector Analysis
    universe_logger.info("\n3️⃣ SECTOR ANALYSIS", operation="enhanced_logging")
    universe_logger.info("-" * 30, operation="enhanced_logging")
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
        universe_logger.info(f"   Sectors found: {len(sector_counts, operation="enhanced_logging")} unique sectors")
        universe_logger.info(f"   Top sectors:", operation="enhanced_logging")
        for sector, count in sector_counts.most_common(10):
            pct = (count / len(sectors)) * 100
            universe_logger.info(f"     {sector}: {count} ({pct:.1f}%, operation="enhanced_logging")")
    
    if missing_sectors:
        universe_logger.info(f"   Missing sectors: {len(missing_sectors, operation="enhanced_logging")} symbols")
    
    # 4. Liquidity Analysis (Sample)
    universe_logger.info("\n4️⃣ LIQUIDITY ANALYSIS (Sample, operation="enhanced_logging")")
    universe_logger.info("-" * 30, operation="enhanced_logging")
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
        universe_logger.info(f"   Sample size: {len(liquidity_data, operation="enhanced_logging")} symbols")
        universe_logger.info(f"   ADV range: ${min(d['adv_millions'] for d in liquidity_data, operation="enhanced_logging"):.1f}M - ${max(d['adv_millions'] for d in liquidity_data):.1f}M")
        
        valid_spreads = [d for d in liquidity_data if d['spread_bps'] != 'N/A']
        if valid_spreads:
            spread_bps = [d['spread_bps'] for d in valid_spreads]
            universe_logger.info(f"   Spread range: {min(spread_bps, operation="enhanced_logging"):.1f} - {max(spread_bps):.1f} bps")
        
        universe_logger.info(f"   Sample details:", operation="enhanced_logging")
        for data in liquidity_data[:5]:
            universe_logger.info(f"     {data['symbol']}: ADV=${data['adv_millions']:.1f}M, Spread={data['spread_bps']}bps", operation="enhanced_logging")
    
    # 5. Growth-Oriented Analysis (Option B)
    universe_logger.info("\n5️⃣ GROWTH-ORIENTED ANALYSIS (OPTION B, operation="enhanced_logging")")
    universe_logger.info("-" * 30, operation="enhanced_logging")
    
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
        
        universe_logger.info(f"   High Volatility (ATR% ≥ 3%, operation="enhanced_logging"): {high_volatility_count}/{len(growth_metrics)} ({high_volatility_count/len(growth_metrics)*100:.1f}%)")
        universe_logger.info(f"   High Growth Potential (≥0.7, operation="enhanced_logging"): {high_growth_count}/{len(growth_metrics)} ({high_growth_count/len(growth_metrics)*100:.1f}%)")
        universe_logger.info(f"   Good Liquidity (ADV ≥ $50M, operation="enhanced_logging"): {good_adv_count}/{len(growth_metrics)} ({good_adv_count/len(growth_metrics)*100:.1f}%)")
        universe_logger.info(f"   Positive Momentum: {positive_momentum_count}/{len(growth_metrics, operation="enhanced_logging")} ({positive_momentum_count/len(growth_metrics)*100:.1f}%)")
        
        # Check if matches Option B criteria
        if high_volatility_count >= len(growth_metrics) * 0.6 and high_growth_count >= len(growth_metrics) * 0.4:
            universe_logger.info(f"   🎉 EXCELLENT! Candidates match Option B (Growth-Oriented, operation="enhanced_logging") criteria!")
        elif high_volatility_count >= len(growth_metrics) * 0.4:
            universe_logger.info(f"   ✅ GOOD! Candidates mostly match Option B criteria", operation="enhanced_logging")
        else:
            universe_logger.warning(f"   ⚠️  MIXED! Some candidates match Option B, but could be more aggressive", operation="enhanced_logging")
    
    # 6. Quality Summary
    universe_logger.info("\n6️⃣ QUALITY SUMMARY", operation="enhanced_logging")
    universe_logger.info("-" * 30, operation="enhanced_logging")
    
    quality_score = 0
    max_score = 5
    
    # Letter diversity (1 point)
    if total_letters >= 15:
        quality_score += 1
        universe_logger.info("   ✅ Good letter diversity", operation="enhanced_logging")
    else:
        universe_logger.warning(f"   ⚠️ Limited letter diversity ({total_letters}/26, operation="enhanced_logging")")
    
    # Market cap quality (1 point)
    if market_caps and len(market_caps) >= len(symbols) * 0.8:
        quality_score += 1
        universe_logger.info("   ✅ Good market cap coverage", operation="enhanced_logging")
    else:
        universe_logger.warning("   ⚠️ Missing market cap data", operation="enhanced_logging")
    
    # S&P 500 size (1 point)
    if market_caps and sp500_count >= len(market_caps) * 0.7:
        quality_score += 1
        universe_logger.info("   ✅ Mostly S&P 500 size companies", operation="enhanced_logging")
    else:
        universe_logger.warning("   ⚠️ Many companies below S&P 500 threshold", operation="enhanced_logging")
    
    # Sector diversity (1 point)
    if sectors and len(sector_counts) >= 5:
        quality_score += 1
        universe_logger.info("   ✅ Good sector diversity", operation="enhanced_logging")
    else:
        universe_logger.warning("   ⚠️ Limited sector diversity", operation="enhanced_logging")
    
    # Liquidity (1 point)
    if liquidity_data and len(liquidity_data) >= 5:
        quality_score += 1
        universe_logger.info("   ✅ Good liquidity sample", operation="enhanced_logging")
    else:
        universe_logger.warning("   ⚠️ Limited liquidity data", operation="enhanced_logging")
    
    universe_logger.info(f"\n🎯 OVERALL QUALITY SCORE: {quality_score}/{max_score}", operation="enhanced_logging")
    
    if quality_score >= 4:
        universe_logger.info("   🏆 EXCELLENT: High-quality universe for training", operation="enhanced_logging")
    elif quality_score >= 3:
        universe_logger.info("   ✅ GOOD: Solid universe for training", operation="enhanced_logging")
    else:
        universe_logger.warning("   ⚠️ NEEDS IMPROVEMENT: Consider regenerating universe", operation="enhanced_logging")

if __name__ == "__main__":
    analyze_universe_quality()
