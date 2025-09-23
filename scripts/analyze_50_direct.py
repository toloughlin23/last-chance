#!/usr/bin/env python3
"""
Direct Analysis of 50 Candidates - Focus on Option B Growth Criteria
"""

import os
import sys
from collections import Counter, defaultdict

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv

load_dotenv()

def main():
    print("🔍 DIRECT ANALYSIS OF 50 CANDIDATES")
    print("=" * 60)
    print("🎯 Checking if candidates match Option B: Growth-Oriented (Aggressive)")
    print("=" * 60)
    
    # Use the EXACT 50 candidates we saw in the provider output
    candidates = [
        'BE', 'CDE', 'OKLO', 'IONQ', 'B', 'RDDT', 'CIEN', 'KGC', 'PSTG', 'CLS',
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
        'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS',
        'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW',
        'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC', 'SPOT'
    ]
    
    print(f"📊 Analyzing {len(candidates)} candidates")
    print(f"📈 Top 10: {candidates[:10]}")
    
    # 1. Letter Distribution Analysis
    print("\n1️⃣ LETTER DISTRIBUTION")
    print("-" * 30)
    first_letters = Counter(s[0].upper() for s in candidates)
    total_letters = len([letter for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if first_letters.get(letter, 0) > 0])
    
    print(f"   Letters represented: {total_letters}/26")
    print("   Distribution:")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        count = first_letters.get(letter, 0)
        if count > 0:
            pct = (count / len(candidates)) * 100
            bar = '█' * int(pct / 2)
            print(f"     {letter}: {count:2d} ({pct:4.1f}%) {bar}")
    
    # Check for A-bias
    a_count = first_letters.get('A', 0)
    a_percentage = a_count / len(candidates) * 100
    if a_percentage > 30:
        print(f"\n⚠️  A-BIAS DETECTED: {a_percentage:.1f}% start with 'A'")
    else:
        print(f"\n✅ NO A-BIAS: Only {a_percentage:.1f}% start with 'A'")
    
    # 2. Sector Analysis
    print("\n2️⃣ SECTOR ANALYSIS")
    print("-" * 30)
    sector_counts = defaultdict(int)
    
    for symbol in candidates:
        sector = get_sector(symbol)
        sector_counts[sector] += 1
    
    print(f"   Sectors found: {len(sector_counts)} unique sectors")
    print("   Top sectors:")
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(candidates)) * 100
        print(f"     {sector}: {count} ({pct:.1f}%)")
    
    # 3. Growth-Oriented Analysis (Option B)
    print("\n3️⃣ GROWTH-ORIENTED ANALYSIS (OPTION B)")
    print("-" * 30)
    
    # Analyze growth characteristics
    tech_count = sector_counts.get('Technology', 0)
    high_volatility_count = 0  # Symbols known for high volatility
    growth_stocks = ['TSLA', 'NVDA', 'AMD', 'PLTR', 'SNOW', 'NET', 'DDOG', 'CRWD', 'ZS', 'OKTA', 'FTNT', 'PANW', 'MDB', 'ESTC', 'SPOT', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'OKLO', 'IONQ', 'RDDT', 'CIEN', 'PSTG', 'CLS', 'ANET']
    
    for symbol in candidates:
        if symbol in growth_stocks:
            high_volatility_count += 1
    
    print(f"   Technology stocks: {tech_count}/{len(candidates)} ({tech_count/len(candidates)*100:.1f}%)")
    print(f"   High volatility/growth stocks: {high_volatility_count}/{len(candidates)} ({high_volatility_count/len(candidates)*100:.1f}%)")
    
    # Check Option B criteria
    tech_percentage = tech_count / len(candidates) * 100
    growth_percentage = high_volatility_count / len(candidates) * 100
    
    print("\n🎯 OPTION B (GROWTH-ORIENTED) ASSESSMENT:")
    if tech_percentage >= 40 and growth_percentage >= 50:
        print("   🎉 EXCELLENT! Strong growth orientation:")
        print(f"   ✅ Technology: {tech_percentage:.1f}% (target: ≥40%)")
        print(f"   ✅ Growth stocks: {growth_percentage:.1f}% (target: ≥50%)")
    elif tech_percentage >= 30 and growth_percentage >= 40:
        print("   ✅ GOOD! Good growth orientation:")
        print(f"   ✅ Technology: {tech_percentage:.1f}% (target: ≥40%)")
        print(f"   ✅ Growth stocks: {growth_percentage:.1f}% (target: ≥50%)")
    else:
        print("   ⚠️  MIXED! Could be more growth-oriented:")
        print(f"   📊 Technology: {tech_percentage:.1f}% (target: ≥40%)")
        print(f"   📊 Growth stocks: {growth_percentage:.1f}% (target: ≥50%)")
    
    # 4. Quality Summary
    print("\n4️⃣ QUALITY SUMMARY")
    print("-" * 30)
    
    quality_score = 0
    max_score = 4
    
    # Letter diversity (1 point)
    if total_letters >= 15:
        quality_score += 1
        print("   ✅ Good letter diversity")
    else:
        print(f"   ⚠️ Limited letter diversity ({total_letters}/26)")
    
    # No A-bias (1 point)
    if a_percentage <= 20:
        quality_score += 1
        print("   ✅ No A-bias detected")
    else:
        print(f"   ⚠️ A-bias detected ({a_percentage:.1f}%)")
    
    # Technology representation (1 point)
    if tech_percentage >= 30:
        quality_score += 1
        print("   ✅ Good technology representation")
    else:
        print(f"   ⚠️ Limited technology representation ({tech_percentage:.1f}%)")
    
    # Growth orientation (1 point)
    if growth_percentage >= 40:
        quality_score += 1
        print("   ✅ Strong growth orientation")
    else:
        print(f"   ⚠️ Limited growth orientation ({growth_percentage:.1f}%)")
    
    print(f"\n🎯 OVERALL QUALITY SCORE: {quality_score}/{max_score}")
    
    if quality_score >= 3:
        print("   🏆 EXCELLENT: High-quality candidates for growth trading")
    elif quality_score >= 2:
        print("   ✅ GOOD: Solid candidates for growth trading")
    else:
        print("   ⚠️ NEEDS IMPROVEMENT: Consider more growth-oriented selection")

def get_sector(symbol):
    """Simplified sector mapping"""
    symbol_upper = symbol.upper()
    
    # Technology
    if any(tech in symbol_upper for tech in ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC', 'OKLO', 'IONQ', 'CIEN', 'PSTG', 'CLS', 'ANET']):
        return 'Technology'
    
    # Financials
    elif any(fin in symbol_upper for fin in ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB', 'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON', 'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ', 'RKT']):
        return 'Financials'
    
    # Healthcare
    elif any(health in symbol_upper for health in ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'BNTX', 'ZTS', 'SYK', 'ISRG', 'EW', 'BSX', 'MDT']):
        return 'Healthcare'
    
    # Energy
    elif any(energy in symbol_upper for energy in ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO', 'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K', 'DVN', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP', 'LBRT', 'WHD', 'CHX', 'LPI', 'PE', 'SM', 'REGI', 'CLR', 'CXO', 'TECK']):
        return 'Energy'
    
    # Materials
    elif any(mat in symbol_upper for mat in ['LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'NEM', 'FCX', 'NUE', 'STLD', 'X', 'CLF', 'AA', 'CDE', 'KGC', 'PAAS', 'BE']):
        return 'Materials'
    
    # Communication Services
    elif any(comm in symbol_upper for comm in ['VZ', 'T', 'CMCSA', 'DIS', 'NFLX', 'GOOGL', 'META', 'TWTR', 'SNAP', 'PINS', 'ROKU', 'SPOT']):
        return 'Communication Services'
    
    else:
        return 'Other'

if __name__ == "__main__":
    main()
