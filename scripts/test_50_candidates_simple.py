#!/usr/bin/env python3
"""
Simple test of 50 candidates using QuotesClient for quality analysis.
This is much faster and more focused than the full provider analysis.
"""

import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.active_universe_provider import ActiveUniverseProvider
from services.quotes_client import QuotesClient
from dotenv import load_dotenv

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
    elif any(health in symbol_upper for health in ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'BNTX', 'ZTS', 'SYK', 'ISRG', 'EW', 'BSX', 'MDT', 'CVS', 'CNC', 'UHS', 'HCA']):
        return 'Healthcare'
    
    # Energy
    elif any(energy in symbol_upper for energy in ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO', 'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'CVE', 'TECK']):
        return 'Energy'
    
    # Materials
    elif any(mat in symbol_upper for mat in ['LIN', 'APD', 'SHW', 'ECL', 'DD', 'FCX', 'NEM', 'LYB', 'DOW', 'PPG', 'ALB', 'BE', 'CDE', 'KGC', 'AU', 'PAAS', 'AGI', 'FNV', 'AEM']):
        return 'Materials'
    
    # Industrials
    elif any(ind in symbol_upper for ind in ['BA', 'CAT', 'GE', 'HON', 'UPS', 'RTX', 'LMT', 'DE', 'MMM', 'CSX', 'NOC', 'GD', 'EMR', 'ETN', 'ITW', 'WM', 'FDX', 'NSC', 'JCI', 'PH', 'CMI', 'ROK', 'OTIS', 'CARR', 'TT', 'IR', 'APTV', 'DAY', 'HPE', 'APH', 'CRH', 'JEF', 'WMS', 'FN', 'JLL', 'BMO', 'ENB']):
        return 'Industrials'
    
    # Consumer Discretionary
    elif any(cons in symbol_upper for cons in ['AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'CMG', 'GME', 'W']):
        return 'Consumer Discretionary'
    
    # Consumer Staples
    elif any(staples in symbol_upper for staples in ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CL', 'KMB', 'GIS', 'K', 'HSY', 'MO']):
        return 'Consumer Staples'
    
    # Utilities
    elif any(util in symbol_upper for util in ['NEE', 'DUK', 'SO', 'AEP', 'EXC', 'XEL', 'WEC', 'ES', 'PEG', 'ED', 'GLW']):
        return 'Utilities'
    
    # Real Estate
    elif any(re in symbol_upper for re in ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'U']):
        return 'Real Estate'
    
    # Communication Services
    elif any(comm in symbol_upper for comm in ['GOOGL', 'GOOG', 'META', 'NFLX', 'DIS', 'CMCSA', 'VZ', 'T', 'CHTR', 'TMUS']):
        return 'Communication Services'
    
    else:
        return 'Other'

def main():
    print("🔍 SIMPLE 50 CANDIDATES QUALITY TEST")
    print("=" * 60)
    print("🎯 Using QuotesClient for fast quality analysis")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    try:
        # Get 50 candidates from provider
        print("📊 Getting 50 top-ranked candidates from provider...")
        provider = ActiveUniverseProvider()
        candidates = provider.get_active_universe()
        
        if len(candidates) < 50:
            print(f"⚠️ Only got {len(candidates)} candidates, using all of them")
            ranked_candidates = candidates
        else:
            ranked_candidates = candidates[:50]
        
        print(f"✅ Found {len(ranked_candidates)} candidates")
        print(f"📈 Top 10: {ranked_candidates[:10]}")
        
        # Initialize quotes client
        quotes_client = QuotesClient()
        
        # Set up time window (last 7 days for quotes)
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        print(f"\n🔍 ANALYZING QUALITY METRICS FOR EACH CANDIDATE")
        print("=" * 60)
        
        quality_data = []
        sector_counts = defaultdict(int)
        letter_counts = defaultdict(int)
        
        for i, symbol in enumerate(ranked_candidates):
            try:
                print(f"{i+1:2d}. {symbol:5s} | ", end="", flush=True)
                
                # Get quotes for this symbol
                quotes = quotes_client.fetch_quotes_window(
                    ticker=symbol,
                    start_utc=start_time,
                    end_utc=end_time,
                    limit=1000  # Reasonable limit for testing
                )
                
                if quotes:
                    # Compute spreads
                    median_dollar_spread, median_bps_spread = quotes_client.compute_median_spreads(quotes)
                    
                    # Get sector
                    sector = get_sector(symbol)
                    sector_counts[sector] += 1
                    
                    # Count first letter
                    first_letter = symbol[0].upper()
                    letter_counts[first_letter] += 1
                    
                    # Store quality data
                    quality_data.append({
                        'symbol': symbol,
                        'sector': sector,
                        'median_dollar_spread': median_dollar_spread,
                        'median_bps_spread': median_bps_spread,
                        'quote_count': len(quotes)
                    })
                    
                    # Print result
                    if median_bps_spread <= 5.0:
                        print(f"✅ {sector:15s} | ${median_dollar_spread:.3f} | {median_bps_spread:.1f}bps | {len(quotes):3d} quotes")
                    elif median_bps_spread <= 10.0:
                        print(f"⚠️ {sector:15s} | ${median_dollar_spread:.3f} | {median_bps_spread:.1f}bps | {len(quotes):3d} quotes")
                    else:
                        print(f"❌ {sector:15s} | ${median_dollar_spread:.3f} | {median_bps_spread:.1f}bps | {len(quotes):3d} quotes")
                else:
                    print(f"❌ No quotes data")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)[:50]}...")
        
        # Analysis Results
        print(f"\n📊 QUALITY ANALYSIS RESULTS")
        print("=" * 60)
        
        if quality_data:
            # Calculate averages
            avg_spread_bps = sum(d['median_bps_spread'] for d in quality_data) / len(quality_data)
            avg_quote_count = sum(d['quote_count'] for d in quality_data) / len(quality_data)
            
            print(f"📈 AVERAGE METRICS:")
            print(f"   Median Spread: {avg_spread_bps:.1f} bps")
            print(f"   Average Quotes: {avg_quote_count:.0f} per symbol")
            
            # Count quality symbols (≤5 bps spread)
            quality_symbols = [d for d in quality_data if d['median_bps_spread'] <= 5.0]
            print(f"   Quality Symbols (≤5bps): {len(quality_symbols)}/{len(quality_data)} ({len(quality_symbols)/len(quality_data)*100:.1f}%)")
            
            # Sector distribution
            print(f"\n🏢 SECTOR DISTRIBUTION:")
            print("=" * 60)
            for sector, count in sorted(sector_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = count / len(quality_data) * 100
                print(f"   {sector:20s}: {count:2d} symbols ({percentage:5.1f}%)")
            
            # Letter distribution
            print(f"\n🔤 LETTER DISTRIBUTION:")
            print("=" * 60)
            for letter in sorted(letter_counts.keys()):
                count = letter_counts[letter]
                percentage = count / len(quality_data) * 100
                print(f"   {letter}: {count:2d} symbols ({percentage:5.1f}%)")
            
            # Check for A-bias
            a_count = letter_counts.get('A', 0)
            a_percentage = a_count / len(quality_data) * 100
            if a_percentage > 30:
                print(f"\n⚠️  A-BIAS DETECTED: {a_percentage:.1f}% start with 'A'")
            else:
                print(f"\n✅ NO A-BIAS: Only {a_percentage:.1f}% start with 'A'")
            
            # Growth-Oriented Analysis (Option B)
            print(f"\n🎯 GROWTH-ORIENTED ANALYSIS (Option B)")
            print("=" * 60)
            
            tech_count = sector_counts.get('Technology', 0)
            tech_percentage = tech_count / len(quality_data) * 100
            
            print(f"📊 Technology Focus: {tech_count}/{len(quality_data)} = {tech_percentage:.1f}%")
            
            if tech_percentage >= 80:
                print("✅ EXCELLENT: High tech concentration for growth trading")
            elif tech_percentage >= 60:
                print("✅ GOOD: Strong tech focus for growth potential")
            elif tech_percentage >= 40:
                print("⚠️ MODERATE: Balanced approach, could be more tech-focused")
            else:
                print("❌ LOW: Not enough tech focus for aggressive growth strategy")
            
            # Volatility analysis (using spread as proxy)
            high_vol_symbols = [d for d in quality_data if d['median_bps_spread'] >= 3.0]
            vol_percentage = len(high_vol_symbols) / len(quality_data) * 100
            print(f"📈 Volatility (spread≥3bps): {len(high_vol_symbols)}/{len(quality_data)} = {vol_percentage:.1f}%")
            
            if vol_percentage >= 60:
                print("✅ EXCELLENT: High volatility for growth opportunities")
            elif vol_percentage >= 40:
                print("✅ GOOD: Good volatility mix for trading")
            else:
                print("⚠️ LOW: May need more volatile symbols for growth strategy")
        
        print(f"\n✅ ANALYSIS COMPLETE!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
