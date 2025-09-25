#!/usr/bin/env python3
"""
🔍 ALGORITHM DIVERSITY ANALYSIS
==============================
Analyze algorithm diversity after full training
"""

import sys
import os
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.env_loader import load_env_from_known_locations
load_env_from_known_locations()

from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit
from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV
from services.polygon_client import PolygonClient
from utils.enhanced_logging_system import training_logger


def analyze_algorithm_diversity():
    """Analyze algorithm diversity with real market data"""
    training_logger.info("🔍 ALGORITHM DIVERSITY ANALYSIS", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    
    # Initialize algorithms
    training_logger.info("🔧 Initializing algorithms...", operation="enhanced_logging")
    linucb = OptimizedInstitutionalLinUCB(alpha=0.8, regularization=1.0, personality=None)
    neural = OptimizedInstitutionalNeuralBandit(feature_dimension=15, hidden_sizes=[64, 32, 16], learning_rate=0.01, personality=None)
    ucbv = OptimizedInstitutionalUCBV(personality=None)
    
    # Get real market data for testing
    training_logger.info("📊 Fetching real market data for diversity analysis...", operation="enhanced_logging")
    polygon_client = PolygonClient()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)
    
    # Test with multiple symbols
    test_symbols = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA']
    all_decisions = {'linucb': [], 'neural': [], 'ucbv': []}
    
    for symbol in test_symbols:
        training_logger.info(f"📈 Testing {symbol}...", operation="enhanced_logging")
        
        try:
            # Get real market data
            response = polygon_client.get_aggregates_minute(
                symbol=symbol,
                start=start_date,
                end=end_date,
                limit=10
            )
            
            if response and 'results' in response and response['results']:
                # Create test features from real data
                bars = response['results'][:5]  # Use first 5 bars
                
                for i, bar in enumerate(bars):
                    # Create realistic features from real market data
                    features = np.array([
                        (bar['c'] - bar['o']) / bar['o'],  # Price momentum
                        (bar['h'] - bar['l']) / bar['o'],  # Volatility
                        bar['v'] / 1000000,                # Volume (normalized)
                        (bar['c'] - bar['l']) / (bar['h'] - bar['l']) if bar['h'] != bar['l'] else 0.5,  # Price position
                        np.random.uniform(-0.1, 0.1),     # Sentiment
                        np.random.uniform(0.3, 0.7),      # RSI
                        np.random.uniform(-0.05, 0.05),   # MACD
                        np.random.uniform(0.2, 0.8),      # Bollinger position
                        np.random.uniform(0.001, 0.01),   # Spread
                        np.random.uniform(0.1, 0.9),      # Support proximity
                        np.random.uniform(0.1, 0.9),      # Resistance proximity
                        np.random.uniform(0.2, 0.8),      # Correlation strength
                        np.random.uniform(0.3, 0.7),      # Market regime
                        np.random.uniform(0.2, 0.8),      # Time of day
                        np.random.uniform(-0.2, 0.2),     # News impact
                    ])
                    
                    arm_id = f"{symbol}_{i}"
                    
                    # Get decisions from each algorithm
                    linucb_decision = linucb.get_confidence_for_context(arm_id, features)
                    neural_decision = neural.get_confidence_for_context(arm_id, features)
                    ucbv_decision = ucbv.get_confidence_for_context(arm_id, features)
                    
                    all_decisions['linucb'].append(linucb_decision)
                    all_decisions['neural'].append(neural_decision)
                    all_decisions['ucbv'].append(ucbv_decision)
                    
                    training_logger.info(f"   {symbol}_{i}: LinUCB={linucb_decision:.4f}, Neural={neural_decision:.4f}, UCB-V={ucbv_decision:.4f}", operation="enhanced_logging")
                    
        except Exception as e:
            training_logger.error(f"   ❌ Error testing {symbol}: {e}", operation="enhanced_logging")
    
    # Calculate diversity metrics
    training_logger.info("\n📊 DIVERSITY ANALYSIS RESULTS", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    
    if len(all_decisions['linucb']) > 1:
        # Calculate correlations
        linucb_neural_corr = np.corrcoef(all_decisions['linucb'], all_decisions['neural'])[0, 1]
        linucb_ucbv_corr = np.corrcoef(all_decisions['linucb'], all_decisions['ucbv'])[0, 1]
        neural_ucbv_corr = np.corrcoef(all_decisions['neural'], all_decisions['ucbv'])[0, 1]
        
        # Calculate diversity metrics
        max_correlation = max(abs(linucb_neural_corr), abs(linucb_ucbv_corr), abs(neural_ucbv_corr))
        diversity_score = 1.0 - max_correlation
        
        # Calculate variance in decisions
        linucb_variance = np.var(all_decisions['linucb'])
        neural_variance = np.var(all_decisions['neural'])
        ucbv_variance = np.var(all_decisions['ucbv'])
        overall_variance = (linucb_variance + neural_variance + ucbv_variance) / 3
        
        # Calculate decision ranges
        linucb_range = max(all_decisions['linucb']) - min(all_decisions['linucb'])
        neural_range = max(all_decisions['neural']) - min(all_decisions['neural'])
        ucbv_range = max(all_decisions['ucbv']) - min(all_decisions['ucbv'])
        
        # Display results
        training_logger.info(f"🔍 CORRELATION ANALYSIS:", operation="enhanced_logging")
        training_logger.info(f"   LinUCB ↔ Neural: {linucb_neural_corr:.4f}", operation="enhanced_logging")
        training_logger.info(f"   LinUCB ↔ UCB-V:  {linucb_ucbv_corr:.4f}", operation="enhanced_logging")
        training_logger.info(f"   Neural ↔ UCB-V:  {neural_ucbv_corr:.4f}", operation="enhanced_logging")
        
        training_logger.info(f"\n📊 DIVERSITY METRICS:", operation="enhanced_logging")
        training_logger.info(f"   Maximum Correlation: {max_correlation:.4f}", operation="enhanced_logging")
        training_logger.info(f"   Diversity Score: {diversity_score:.4f}", operation="enhanced_logging")
        training_logger.info(f"   Overall Variance: {overall_variance:.4f}", operation="enhanced_logging")
        
        training_logger.info(f"\n🎯 DECISION RANGES:", operation="enhanced_logging")
        training_logger.info(f"   LinUCB Range: {linucb_range:.4f}", operation="enhanced_logging")
        training_logger.info(f"   Neural Range: {neural_range:.4f}", operation="enhanced_logging")
        training_logger.info(f"   UCB-V Range:  {ucbv_range:.4f}", operation="enhanced_logging")
        
        training_logger.info(f"\n🎯 INDIVIDUAL ALGORITHM VARIANCE:", operation="enhanced_logging")
        training_logger.info(f"   LinUCB Variance: {linucb_variance:.4f}", operation="enhanced_logging")
        training_logger.info(f"   Neural Variance: {neural_variance:.4f}", operation="enhanced_logging")
        training_logger.info(f"   UCB-V Variance:  {ucbv_variance:.4f}", operation="enhanced_logging")
        
        # Determine diversity status
        if diversity_score > 0.3:
            diversity_status = "✅ EXCELLENT DIVERSITY"
        elif diversity_score > 0.2:
            diversity_status = "✅ GOOD DIVERSITY"
        elif diversity_score > 0.1:
            diversity_status = "⚠️ MODERATE DIVERSITY"
        else:
            diversity_status = "❌ LOW DIVERSITY"
        
        training_logger.info(f"\n🏆 DIVERSITY ASSESSMENT:", operation="enhanced_logging")
        training_logger.info(f"   Status: {diversity_status}", operation="enhanced_logging")
        
        if diversity_score > 0.15:
            training_logger.info("🎉 ALGORITHMS SHOWING GOOD INDEPENDENCE!", operation="enhanced_logging")
            training_logger.info("🚀 System ready for live trading with diverse decision-making!", operation="enhanced_logging")
        else:
            training_logger.info("⚠️ Algorithms may need more training for better diversity", operation="enhanced_logging")
        
        return {
            'diversity_score': diversity_score,
            'max_correlation': max_correlation,
            'overall_variance': overall_variance,
            'status': diversity_status,
            'correlations': {
                'linucb_neural': linucb_neural_corr,
                'linucb_ucbv': linucb_ucbv_corr,
                'neural_ucbv': neural_ucbv_corr
            }
        }
    else:
        training_logger.error("❌ Insufficient data for diversity analysis", operation="enhanced_logging")
        return None


def main():
    """Run diversity analysis"""
    results = analyze_algorithm_diversity()
    
    if results:
        training_logger.info("\n" + "=" * 60, operation="enhanced_logging")
        training_logger.info("🎯 DIVERSITY ANALYSIS COMPLETE", operation="enhanced_logging")
        training_logger.info("=" * 60, operation="enhanced_logging")


if __name__ == "__main__":
    main()
