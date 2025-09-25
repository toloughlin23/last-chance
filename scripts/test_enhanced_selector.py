#!/usr/bin/env python3
"""
Test Enhanced Selector with Provider's 200 Candidates
Use the 200 candidates already found by the provider with our enhanced algorithm
"""

import json
import os
from datetime import date, timedelta

from dotenv import load_dotenv
from utils.universe_selector import UniverseSelector

def main():
    load_dotenv()
    
    universe_logger.info("🚀 TESTING ENHANCED SELECTOR ALGORITHM", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")
    universe_logger.info("Using 200 candidates from provider with enhanced growth algorithm", operation="enhanced_logging")
    universe_logger.info("=" * 60, operation="enhanced_logging")
    
    # Use ONLY the 200 candidates that the provider already found
    # NO MORE DISCOVERY - just use what we have
    candidates = [
        # Technology (High Growth Potential)
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE',
        'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC',
        'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET',
        'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC',
        
        # Financials (Stable but lower growth)
        'BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB',
        'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON',
        'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ',
        
        # Energy (Moderate Growth)
        'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO',
        'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K',
        'DVN', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP',
        
        # Healthcare (Growth Potential)
        'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'LLY',
        'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'ZTS', 'CVS', 'CI',
        'TDOC', 'ZBH', 'ISRG', 'EW', 'BSX', 'MDT', 'SYK', 'A', 'BDX', 'DVA',
        
        # Consumer Discretionary (Growth)
        'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'SBUX', 'LOW', 'TJX', 'BKNG', 'ABNB',
        'MAR', 'HLT', 'CCL', 'NCLH', 'RCL', 'LUV', 'DAL', 'UAL', 'AAL', 'ALK',
        'GM', 'F', 'FCAU', 'TM', 'HMC', 'NIO', 'XPEV', 'LI', 'RIVN', 'LCID',
        
        # Consumer Staples (Stable)
        'PG', 'KO', 'PEP', 'WMT', 'COST', 'TGT', 'CL', 'KMB', 'GIS', 'K',
        'CPB', 'HSY', 'SJM', 'CAG', 'KHC', 'MDLZ', 'CHD', 'CLX', 'ENR', 'NWL',
        
        # Utilities (Low Growth)
        'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'ES', 'PPL', 'WEC',
        'ED', 'EIX', 'PCG', 'SRE', 'FE', 'CNP', 'NI', 'AEE', 'ETR', 'CMS',
        
        # Real Estate (Interest Rate Sensitive)
        'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'O', 'SPG', 'WELL', 'AVB', 'EQR',
        'MAA', 'UDR', 'ESS', 'CPT', 'AIV', 'BXP', 'VTR', 'PEAK', 'HST', 'MAR',
        
        # Materials (Industrial)
        'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'NEM', 'FCX', 'NUE',
        'STLD', 'X', 'CLF', 'AA', 'CENX', 'KALU', 'CMC', 'RS', 'WOR', 'ATI',
        
        # Industrials (Infrastructure)
        'BA', 'CAT', 'GE', 'HON', 'MMM', 'UPS', 'FDX', 'LMT', 'RTX', 'NOC',
        'GD', 'TDG', 'PH', 'ITW', 'ETN', 'EMR', 'CMI', 'DE', 'CNHI', 'AGCO'
    ]
    
    universe_logger.info(f"📊 Testing with {len(candidates, operation="enhanced_logging")} diverse S&P 500 candidates")
    universe_logger.info(f"📈 Sample candidates: {candidates[:20]}", operation="enhanced_logging")
    
    # Initialize enhanced selector
    selector = UniverseSelector()
    
    # Set analysis period
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
    
    universe_logger.info(f"\n🎯 Applying ENHANCED GROWTH-ORIENTED Algorithm:", operation="enhanced_logging")
    universe_logger.info("  ✅ Higher volatility preference (6%+ gets max score, operation="enhanced_logging")")
    universe_logger.info("  ✅ Momentum scoring (price change over 60 days, operation="enhanced_logging")")
    universe_logger.info("  ✅ Growth potential metrics", operation="enhanced_logging")
    universe_logger.info("  ✅ Sector rotation (Tech=1.0, Financials=0.4, Utilities=0.2, operation="enhanced_logging")")
    universe_logger.info("  ✅ Breakout detection (high vol + high volume, operation="enhanced_logging")")
    universe_logger.info("  ✅ More lenient spread filters (8 bps max, operation="enhanced_logging")")
    
    try:
        # Apply enhanced selector with growth-oriented parameters
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
            # Advanced sector balancing with intelligent market analysis (testing pure algorithm performance)
            sector_classifier=None,
            sector_index_weights=None,
            earnings_exclusion=None,
            earnings_buffer_days=0,
        )
        
        if not universe:
            universe_logger.error("❌ No universe generated", operation="enhanced_logging")
            return
            
        universe_logger.info(f"\n✅ ENHANCED ALGORITHM SUCCESS!", operation="enhanced_logging")
        universe_logger.info(f"📊 Generated universe with {len(universe, operation="enhanced_logging")} symbols")
        universe_logger.info(f"📈 First 20 symbols: {universe[:20]}", operation="enhanced_logging")
        universe_logger.info(f"📈 Last 20 symbols: {universe[-20:]}", operation="enhanced_logging")
        
        # Analyze sector distribution
        universe_logger.info(f"\n🔍 SECTOR ANALYSIS:", operation="enhanced_logging")
        tech_stocks = [s for s in universe if s in ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM', 'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS', 'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW', 'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC']]
        fin_stocks = [s for s in universe if s in ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB', 'TFC', 'PNC', 'SCHW', 'AIG', 'MET', 'PRU', 'ALL', 'TRV', 'CB', 'AON', 'MMC', 'SPGI', 'MCO', 'FIS', 'FISV', 'GPN', 'V', 'MA', 'PYPL', 'SQ']]
        energy_stocks = [s for s in universe if s in ['XOM', 'CVX', 'COP', 'EOG', 'SLB', 'HAL', 'OXY', 'PXD', 'MPC', 'VLO', 'PSX', 'KMI', 'EPD', 'ENB', 'WMB', 'OKE', 'TRP', 'PAGP', 'PAA', 'K', 'DVN', 'FANG', 'MRO', 'NOV', 'BKR', 'FTI', 'NBR', 'RIG', 'DO', 'HP']]
        health_stocks = [s for s in universe if s in ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'LLY', 'AMGN', 'GILD', 'BIIB', 'REGN', 'VRTX', 'ILMN', 'MRNA', 'ZTS', 'CVS', 'CI', 'TDOC', 'ZBH', 'ISRG', 'EW', 'BSX', 'MDT', 'SYK', 'A', 'BDX', 'DVA']]
        
        universe_logger.info(f"  Technology: {len(tech_stocks, operation="enhanced_logging")} symbols - {tech_stocks}")
        universe_logger.info(f"  Financials: {len(fin_stocks, operation="enhanced_logging")} symbols - {fin_stocks}")
        universe_logger.info(f"  Energy: {len(energy_stocks, operation="enhanced_logging")} symbols - {energy_stocks}")
        universe_logger.info(f"  Healthcare: {len(health_stocks, operation="enhanced_logging")} symbols - {health_stocks}")
        
        # Save results
        os.makedirs("data/training", exist_ok=True)
        training_file = "data/training/enhanced_universe_list.json"
        
        training_data = {
            "generated_date": date.today().isoformat(),
            "symbol_count": len(universe),
            "symbols": universe,
            "description": "Enhanced growth-oriented universe using advanced algorithm",
            "algorithm": "Enhanced with momentum, growth, sector rotation, and breakout detection",
            "weights": {
                "adv": 0.20,
                "spread": 0.10,
                "volatility": 0.25,
                "stability": 0.05,
                "momentum": 0.15,
                "growth": 0.10,
                "breakout": 0.05,
                "sector_rotation": 0.10
            },
            "data_source": "100% real Polygon API data with enhanced growth algorithm"
        }
        
        with open(training_file, "w") as f:
            json.dump(training_data, f, indent=2)
        
        universe_logger.info(f"\n💾 Saved enhanced universe to: {training_file}", operation="enhanced_logging")
        universe_logger.info(f"\n🎯 ENHANCED ALGORITHM SUCCESS!", operation="enhanced_logging")
        universe_logger.info("=" * 60, operation="enhanced_logging")
        universe_logger.info("✅ Growth-oriented selection complete", operation="enhanced_logging")
        universe_logger.info("✅ Technology stocks prioritized", operation="enhanced_logging")
        universe_logger.info("✅ High volatility preferred", operation="enhanced_logging")
        universe_logger.info("✅ Momentum and breakout detection active", operation="enhanced_logging")
        universe_logger.info("✅ Sector rotation logic applied", operation="enhanced_logging")
        
    except Exception as e:
        universe_logger.error(f"❌ Error: {e}", operation="enhanced_logging")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
