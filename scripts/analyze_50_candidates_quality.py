#!/usr/bin/env python3
"""
Analyze Quality of 50 Candidates - Check Sector Balance & Growth Criteria
"""

import os
import sys
from datetime import date, timedelta
from collections import defaultdict

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from dotenv import load_dotenv
load_dotenv()

def main():
    training_logger.info("🔍 ANALYZING 50 CANDIDATES QUALITY", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    training_logger.info("🎯 Checking if candidates match Option B: Growth-Oriented (Aggressive, operation="enhanced_logging")")
    training_logger.info("=" * 60, operation="enhanced_logging")
    
    try:
        from utils.active_universe_provider import ActiveUniverseProvider
        
        provider = ActiveUniverseProvider()
        
        # Get the exact 50 candidates the provider found
        training_logger.info("📊 Getting 50 top-ranked candidates from provider...", operation="enhanced_logging")
        
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
        
        training_logger.info(f"✅ Found {len(ranked_candidates, operation="enhanced_logging")} ranked candidates")
        training_logger.info(f"📈 Top 10: {ranked_candidates[:10]}", operation="enhanced_logging")
        
        # Analyze each candidate's quality metrics
        training_logger.info("\n🔍 ANALYZING QUALITY METRICS FOR EACH CANDIDATE", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        
        quality_data = []
        sector_counts = defaultdict(int)
        letter_counts = defaultdict(int)
        
        for i, symbol in enumerate(ranked_candidates[:50]):
            try:
                # Get quality metrics for this symbol
                metrics = provider._analyze_symbol_quality(
                    symbol=symbol,
                    min_market_cap=1e9,  # 1B minimum market cap
                    analysis_days=30,
                    start_date=start_date,
                    end_date=end_date,
                    quotes_client=provider.quotes_client
                )
                
                if metrics:
                    quality_data.append({
                        'symbol': symbol,
                        'market_cap': metrics.get('market_cap', 0),
                        'adv': metrics.get('adv', 0),
                        'spread_bps': metrics.get('spread_bps', 0),
                        'atr_pct': metrics.get('atr_pct', 0),
                        'stability': metrics.get('stability', 0),
                        'quality_score': metrics.get('quality_score', 0),
                        'price_change_pct': metrics.get('price_change_pct', 0),
                        'growth_potential': metrics.get('growth_potential', 0),
                        'breakout_potential': metrics.get('breakout_potential', 0)
                    })
                    
                    # Count by first letter
                    first_letter = symbol[0].upper()
                    letter_counts[first_letter] += 1
                    
                    # Count by sector (simplified mapping)
                    sector = get_sector(symbol)
                    sector_counts[sector] += 1
                    
                    training_logger.info(f"{i+1:2d}. {symbol:6s} | Market Cap: ${metrics.get('market_cap', 0, operation="enhanced_logging")/1e9:6.1f}B | "
                          f"ADV: ${metrics.get('adv', 0)/1e6:6.1f}M | Spread: {metrics.get('spread_bps', 0):5.1f}bps | "
                          f"ATR%: {metrics.get('atr_pct', 0)*100:5.1f}% | Growth: {metrics.get('growth_potential', 0):4.2f} | "
                          f"Score: {metrics.get('quality_score', 0):5.2f}")
                else:
                    training_logger.error(f"{i+1:2d}. {symbol:6s} | ❌ No metrics available", operation="enhanced_logging")
                    
            except Exception as e:
                training_logger.error(f"{i+1:2d}. {symbol:6s} | ❌ Error: {e}", operation="enhanced_logging")
        
        # Analyze the results
        training_logger.info("\n📊 QUALITY ANALYSIS RESULTS", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        
        if quality_data:
            # Calculate averages
            avg_market_cap = sum(d['market_cap'] for d in quality_data) / len(quality_data)
            avg_adv = sum(d['adv'] for d in quality_data) / len(quality_data)
            avg_spread = sum(d['spread_bps'] for d in quality_data) / len(quality_data)
            avg_atr = sum(d['atr_pct'] for d in quality_data) / len(quality_data)
            avg_growth = sum(d['growth_potential'] for d in quality_data) / len(quality_data)
            avg_score = sum(d['quality_score'] for d in quality_data) / len(quality_data)
            
            training_logger.info(f"📈 AVERAGE METRICS:", operation="enhanced_logging")
            training_logger.info(f"   Market Cap: ${avg_market_cap/1e9:.1f}B", operation="enhanced_logging")
            training_logger.info(f"   ADV: ${avg_adv/1e6:.1f}M", operation="enhanced_logging")
            training_logger.info(f"   Spread: {avg_spread:.1f} bps", operation="enhanced_logging")
            training_logger.info(f"   ATR%: {avg_atr*100:.1f}%", operation="enhanced_logging")
            training_logger.info(f"   Growth Potential: {avg_growth:.3f}", operation="enhanced_logging")
            training_logger.info(f"   Quality Score: {avg_score:.3f}", operation="enhanced_logging")
            
            # Check Option B criteria
            training_logger.info(f"\n🎯 OPTION B (GROWTH-ORIENTED, operation="enhanced_logging") CRITERIA CHECK:")
            training_logger.info("=" * 60, operation="enhanced_logging")
            
            high_volatility_count = sum(1 for d in quality_data if d['atr_pct'] >= 0.03)  # 3%+
            high_growth_count = sum(1 for d in quality_data if d['growth_potential'] >= 0.7)
            good_adv_count = sum(1 for d in quality_data if d['adv'] >= 50_000_000)  # $50M+
            reasonable_spread_count = sum(1 for d in quality_data if d['spread_bps'] <= 20.0)  # 20bps or less
            
            training_logger.info(f"✅ High Volatility (ATR% ≥ 3%, operation="enhanced_logging"): {high_volatility_count}/{len(quality_data)} ({high_volatility_count/len(quality_data)*100:.1f}%)")
            training_logger.info(f"✅ High Growth Potential (≥0.7, operation="enhanced_logging"): {high_growth_count}/{len(quality_data)} ({high_growth_count/len(quality_data)*100:.1f}%)")
            training_logger.info(f"✅ Good Liquidity (ADV ≥ $50M, operation="enhanced_logging"): {good_adv_count}/{len(quality_data)} ({good_adv_count/len(quality_data)*100:.1f}%)")
            training_logger.info(f"✅ Reasonable Spreads (≤20bps, operation="enhanced_logging"): {reasonable_spread_count}/{len(quality_data)} ({reasonable_spread_count/len(quality_data)*100:.1f}%)")
            
            # Overall assessment
            if high_volatility_count >= len(quality_data) * 0.6 and high_growth_count >= len(quality_data) * 0.4:
                training_logger.info(f"\n🎉 EXCELLENT! Candidates match Option B (Growth-Oriented, operation="enhanced_logging") criteria!")
            elif high_volatility_count >= len(quality_data) * 0.4:
                training_logger.info(f"\n✅ GOOD! Candidates mostly match Option B criteria", operation="enhanced_logging")
            else:
                training_logger.warning(f"\n⚠️  MIXED! Some candidates match Option B, but could be more aggressive", operation="enhanced_logging")
        
        # Sector distribution
        training_logger.info(f"\n🏢 SECTOR DISTRIBUTION:", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(ranked_candidates[:50]) * 100
            training_logger.info(f"   {sector:20s}: {count:2d} symbols ({percentage:5.1f}%, operation="enhanced_logging")")
        
        # Letter distribution
        training_logger.info(f"\n🔤 LETTER DISTRIBUTION:", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")
        for letter in sorted(letter_counts.keys()):
            count = letter_counts[letter]
            percentage = count / len(ranked_candidates[:50]) * 100
            training_logger.info(f"   {letter}: {count:2d} symbols ({percentage:5.1f}%, operation="enhanced_logging")")
        
        # Check for A-bias
        a_count = letter_counts.get('A', 0)
        a_percentage = a_count / len(ranked_candidates[:50]) * 100
        if a_percentage > 30:
            training_logger.warning(f"\n⚠️  A-BIAS DETECTED: {a_percentage:.1f}% start with 'A'", operation="enhanced_logging")
        else:
            training_logger.info(f"\n✅ NO A-BIAS: Only {a_percentage:.1f}% start with 'A'", operation="enhanced_logging")
            
    except Exception as e:
        training_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

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
    
    # Industrials
    elif any(ind in symbol_upper for ind in ['BA', 'CAT', 'GE', 'HON', 'UPS', 'RTX', 'LMT', 'NOC', 'GD', 'EMR', 'ITW', 'ETN', 'PH', 'MMM', 'DE', 'CMI', 'FDX', 'CSX', 'NSC', 'UNP', 'HPE']):
        return 'Industrials'
    
    # Consumer Discretionary
    elif any(cons in symbol_upper for cons in ['HD', 'MCD', 'NKE', 'SBUX', 'TJX', 'LOW', 'BKNG', 'ABNB', 'MAR', 'HLT', 'CCL', 'RCL', 'NCLH', 'UAL', 'ALK']):
        return 'Consumer Discretionary'
    
    # Consumer Staples
    elif any(staple in symbol_upper for staple in ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CL', 'KMB', 'GIS', 'K', 'HSY', 'CPB', 'SJM', 'CAG', 'KHC']):
        return 'Consumer Staples'
    
    # Utilities
    elif any(util in symbol_upper for util in ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL', 'PEG', 'ES', 'PCG', 'AEE', 'AEG']):
        return 'Utilities'
    
    # Communication Services
    elif any(comm in symbol_upper for comm in ['VZ', 'T', 'CMCSA', 'DIS', 'NFLX', 'GOOGL', 'META', 'TWTR', 'SNAP', 'PINS', 'ROKU', 'SPOT']):
        return 'Communication Services'
    
    # Real Estate
    elif any(re in symbol_upper for re in ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'UDR', 'ESS', 'CPT']):
        return 'Real Estate'
    
    else:
        return 'Other'

if __name__ == "__main__":
    main()
