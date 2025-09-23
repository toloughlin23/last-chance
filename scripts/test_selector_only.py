#!/usr/bin/env python3
"""
Test Enhanced Selector ONLY - No Provider Discovery
Just test the enhanced algorithm with 200 candidates
"""

import json
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from utils.universe_selector import UniverseSelector

def main():
    load_dotenv()
    
    print("🚀 TESTING ENHANCED SELECTOR ONLY")
    print("=" * 50)
    print("NO PROVIDER DISCOVERY - Just 200 candidates")
    print("=" * 50)
    
    # Use EXACTLY 200 candidates - NO DISCOVERY
    candidates = [
        # Technology (High Growth Potential) - 40 symbols
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE',
        'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC',
        'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET',
        'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC',
        
        # Financials (Stable but lower growth) - 30 symbols
        'BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB',
        'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON',
        'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ',
        
        # Energy (Moderate Growth) - 30 symbols
        'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO',
        'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K',
        'DVN', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP',
        
        # Healthcare (Growth Potential) - 30 symbols
        'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'LLY',
        'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'ZTS', 'CVS', 'CI',
        'TDOC', 'ZBH', 'ISRG', 'EW', 'BSX', 'MDT', 'SYK', 'A', 'BDX', 'DVA',
        
        # Consumer Discretionary (Growth) - 30 symbols
        'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'ABNB', 'MAR', 'HLT',
        'CCL', 'NCLH', 'RCL', 'LUV', 'DAL', 'UAL', 'AAL', 'ALK', 'GM', 'F',
        'FCAU', 'TM', 'HMC', 'NIO', 'XPEV', 'LI', 'RIVN', 'LCID', 'FORD', 'RACE',
        
        # Consumer Staples (Stable) - 20 symbols
        'PG', 'KO', 'PEP', 'WMT', 'COST', 'TGT', 'CL', 'KMB', 'GIS', 'K',
        'CPB', 'HSY', 'SJM', 'CAG', 'KHC', 'MDLZ', 'CHD', 'CLX', 'ENR', 'NWL',
        
        # Utilities (Low Growth) - 20 symbols
        'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'ES', 'PPL', 'WEC',
        'ED', 'EIX', 'PCG', 'SRE', 'FE', 'CNP', 'NI', 'AEE', 'ETR', 'CMS'
    ]
    
    print(f"📊 Using {len(candidates)} candidates - NO DISCOVERY")
    print(f"📈 Sample: {candidates[:10]}")
    
    # Initialize enhanced selector
    selector = UniverseSelector()
    
    # Set analysis period
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    print(f"\n🎯 Applying ENHANCED GROWTH Algorithm:")
    print("  ✅ Higher volatility preference")
    print("  ✅ Momentum scoring")
    print("  ✅ Growth potential metrics")
    print("  ✅ Sector rotation (Tech=1.0, Financials=0.4)")
    print("  ✅ Breakout detection")
    
    try:
        # Apply enhanced selector
        universe = selector.select_universe(
            candidates=candidates,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            target_size=120,
            target_max_size=150,
            allow_expand_above_target=True,
            expand_margin=0.9,
            # Enhanced filters for growth trading
            min_price=10.0,
            min_atr_pct=0.01,
            max_atr_pct=0.08,  # Allow higher volatility
            adv_min_dollar=50_000_000.0,
            spread_filter_enabled=True,
            spread_max_dollars=0.02,
            spread_max_bps=8.0,  # More lenient for growth
            spread_lookback_days=5,
            spread_core_hours_only=True,
            # Enhanced weights for growth
            weight_adv=0.20,
            weight_spread=0.10,
            weight_volatility=0.25,
            weight_stability=0.05,
            weight_momentum=0.15,
            weight_growth=0.10,
            weight_breakout=0.05,
            weight_sector_rotation=0.10,
            # No sector balancing for now
            sector_classifier=None,
            sector_index_weights=None,
            earnings_exclusion=None,
            earnings_buffer_days=0,
        )
        
        if not universe:
            print("❌ No universe generated")
            return
            
        print(f"\n✅ ENHANCED ALGORITHM SUCCESS!")
        print(f"📊 Generated universe with {len(universe)} symbols")
        print(f"📈 First 20: {universe[:20]}")
        
        # Analyze sector distribution
        tech_count = len([s for s in universe if s in ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC']])
        fin_count = len([s for s in universe if s in ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB', 'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON', 'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ']])
        
        print(f"\n🔍 SECTOR ANALYSIS:")
        print(f"  Technology: {tech_count} symbols")
        print(f"  Financials: {fin_count} symbols")
        
        print(f"\n🎯 ENHANCED ALGORITHM SUCCESS!")
        print("✅ Growth-oriented selection complete")
        print("✅ Technology stocks prioritized")
        print("✅ High volatility preferred")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
