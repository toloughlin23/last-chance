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
    training_logger.info("🔍 DIRECT ANALYSIS OF 50 CANDIDATES", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    training_logger.info("🎯 Checking if candidates match Option B: Growth-Oriented (Aggressive, operation="enhanced_logging")")
    training_logger.info("=" * 60, operation="enhanced_logging")
    
    # Use the EXACT 50 candidates we saw in the provider output
    candidates = [
        'BE', 'CDE', 'OKLO', 'IONQ', 'B', 'RDDT', 'CIEN', 'KGC', 'PSTG', 'CLS',
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
        'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS',
        'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW',
        'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC', 'SPOT'
    ]
    
    training_logger.info(f"📊 Analyzing {len(candidates, operation="enhanced_logging")} candidates")
    training_logger.info(f"📈 Top 10: {candidates[:10]}", operation="enhanced_logging")
    
    # 1. Letter Distribution Analysis
    training_logger.info("\n1️⃣ LETTER DISTRIBUTION", operation="enhanced_logging")
    training_logger.info("-" * 30, operation="enhanced_logging")
    first_letters = Counter(s[0].upper() for s in candidates)
    total_letters = len([l for l in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if first_letters.get(l, 0) > 0])
    
    training_logger.info(f"   Letters represented: {total_letters}/26", operation="enhanced_logging")
    training_logger.info(f"   Distribution:", operation="enhanced_logging")
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        count = first_letters.get(letter, 0)
        if count > 0:
            pct = (count / len(candidates)) * 100
            bar = '█' * int(pct / 2)
            training_logger.info(f"     {letter}: {count:2d} ({pct:4.1f}%, operation="enhanced_logging") {bar}")
    
    # Check for A-bias
    a_count = first_letters.get('A', 0)
    a_percentage = a_count / len(candidates) * 100
    if a_percentage > 30:
        training_logger.warning(f"\n⚠️  A-BIAS DETECTED: {a_percentage:.1f}% start with 'A'", operation="enhanced_logging")
    else:
        training_logger.info(f"\n✅ NO A-BIAS: Only {a_percentage:.1f}% start with 'A'", operation="enhanced_logging")
    
    # 2. Sector Analysis
    training_logger.info("\n2️⃣ SECTOR ANALYSIS", operation="enhanced_logging")
    training_logger.info("-" * 30, operation="enhanced_logging")
    sector_counts = defaultdict(int)
    
    for symbol in candidates:
        sector = get_sector(symbol)
        sector_counts[sector] += 1
    
    training_logger.info(f"   Sectors found: {len(sector_counts, operation="enhanced_logging")} unique sectors")
    training_logger.info(f"   Top sectors:", operation="enhanced_logging")
    for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(candidates)) * 100
        training_logger.info(f"     {sector}: {count} ({pct:.1f}%, operation="enhanced_logging")")
    
    # 3. Growth-Oriented Analysis (Option B)
    training_logger.info("\n3️⃣ GROWTH-ORIENTED ANALYSIS (OPTION B, operation="enhanced_logging")")
    training_logger.info("-" * 30, operation="enhanced_logging")
    
    # Analyze growth characteristics
    tech_count = sector_counts.get('Technology', 0)
    high_volatility_count = 0  # Symbols known for high volatility
    growth_stocks = ['TSLA', 'NVDA', 'AMD', 'PLTR', 'SNOW', 'NET', 'DDOG', 'CRWD', 'ZS', 'OKTA', 'FTNT', 'PANW', 'MDB', 'ESTC', 'SPOT', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'OKLO', 'IONQ', 'RDDT', 'CIEN', 'PSTG', 'CLS', 'ANET']
    
    for symbol in candidates:
        if symbol in growth_stocks:
            high_volatility_count += 1
    
    training_logger.info(f"   Technology stocks: {tech_count}/{len(candidates, operation="enhanced_logging")} ({tech_count/len(candidates)*100:.1f}%)")
    training_logger.info(f"   High volatility/growth stocks: {high_volatility_count}/{len(candidates, operation="enhanced_logging")} ({high_volatility_count/len(candidates)*100:.1f}%)")
    
    # Check Option B criteria
    tech_percentage = tech_count / len(candidates) * 100
    growth_percentage = high_volatility_count / len(candidates) * 100
    
    training_logger.info(f"\n🎯 OPTION B (GROWTH-ORIENTED, operation="enhanced_logging") ASSESSMENT:")
    if tech_percentage >= 40 and growth_percentage >= 50:
        training_logger.info(f"   🎉 EXCELLENT! Strong growth orientation:", operation="enhanced_logging")
        training_logger.info(f"   ✅ Technology: {tech_percentage:.1f}% (target: ≥40%, operation="enhanced_logging")")
        training_logger.info(f"   ✅ Growth stocks: {growth_percentage:.1f}% (target: ≥50%, operation="enhanced_logging")")
    elif tech_percentage >= 30 and growth_percentage >= 40:
        training_logger.info(f"   ✅ GOOD! Good growth orientation:", operation="enhanced_logging")
        training_logger.info(f"   ✅ Technology: {tech_percentage:.1f}% (target: ≥40%, operation="enhanced_logging")")
        training_logger.info(f"   ✅ Growth stocks: {growth_percentage:.1f}% (target: ≥50%, operation="enhanced_logging")")
    else:
        training_logger.warning(f"   ⚠️  MIXED! Could be more growth-oriented:", operation="enhanced_logging")
        training_logger.info(f"   📊 Technology: {tech_percentage:.1f}% (target: ≥40%, operation="enhanced_logging")")
        training_logger.info(f"   📊 Growth stocks: {growth_percentage:.1f}% (target: ≥50%, operation="enhanced_logging")")
    
    # 4. Quality Summary
    training_logger.info("\n4️⃣ QUALITY SUMMARY", operation="enhanced_logging")
    training_logger.info("-" * 30, operation="enhanced_logging")
    
    quality_score = 0
    max_score = 4
    
    # Letter diversity (1 point)
    if total_letters >= 15:
        quality_score += 1
        training_logger.info("   ✅ Good letter diversity", operation="enhanced_logging")
    else:
        training_logger.warning(f"   ⚠️ Limited letter diversity ({total_letters}/26, operation="enhanced_logging")")
    
    # No A-bias (1 point)
    if a_percentage <= 20:
        quality_score += 1
        training_logger.info("   ✅ No A-bias detected", operation="enhanced_logging")
    else:
        training_logger.warning(f"   ⚠️ A-bias detected ({a_percentage:.1f}%, operation="enhanced_logging")")
    
    # Technology representation (1 point)
    if tech_percentage >= 30:
        quality_score += 1
        training_logger.info("   ✅ Good technology representation", operation="enhanced_logging")
    else:
        training_logger.warning(f"   ⚠️ Limited technology representation ({tech_percentage:.1f}%, operation="enhanced_logging")")
    
    # Growth orientation (1 point)
    if growth_percentage >= 40:
        quality_score += 1
        training_logger.info("   ✅ Strong growth orientation", operation="enhanced_logging")
    else:
        training_logger.warning(f"   ⚠️ Limited growth orientation ({growth_percentage:.1f}%, operation="enhanced_logging")")
    
    training_logger.info(f"\n🎯 OVERALL QUALITY SCORE: {quality_score}/{max_score}", operation="enhanced_logging")
    
    if quality_score >= 3:
        training_logger.info("   🏆 EXCELLENT: High-quality candidates for growth trading", operation="enhanced_logging")
    elif quality_score >= 2:
        training_logger.info("   ✅ GOOD: Solid candidates for growth trading", operation="enhanced_logging")
    else:
        training_logger.warning("   ⚠️ NEEDS IMPROVEMENT: Consider more growth-oriented selection", operation="enhanced_logging")

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
