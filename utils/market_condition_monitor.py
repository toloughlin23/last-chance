#!/usr/bin/env python3
"""
Market Condition Monitor - Automatic Tech Cool-off Detection
"""

import os
import sys
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import json

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from services.polygon_client import PolygonClient

class MarketConditionMonitor:
    """
    Monitors market conditions and automatically detects tech cool-offs.
    
    Features:
    - Tracks tech sector performance vs other sectors
    - Detects momentum reversals
    - Automatically adjusts sector weights
    - Provides risk management recommendations
    """
    
    def __init__(self, polygon_client: Optional[PolygonClient] = None):
        self.polygon_client = polygon_client or PolygonClient()
        self.cache_path = "data/market_conditions.json"
        
        # Verify API key is loaded
        if not hasattr(self.polygon_client, 'api_key') or not self.polygon_client.api_key:
            print("⚠️ Polygon API key not found, using mock data for testing")
            self.use_mock_data = True
        else:
            self.use_mock_data = False
        
        # Tech sector symbols for monitoring
        self.tech_symbols = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'NFLX', 'ADBE', 'CRM',
            'ORCL', 'INTC', 'AMD', 'QCOM', 'AVGO', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'SNPS',
            'CDNS', 'ANSS', 'FTNT', 'PANW', 'CRWD', 'ZS', 'OKTA', 'DDOG', 'NET', 'SNOW',
            'PLTR', 'ZM', 'DOCU', 'TEAM', 'WDAY', 'NOW', 'SPLK', 'MDB', 'ESTC'
        ]
        
        # Defensive sector symbols for comparison
        self.defensive_symbols = {
            'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'XEL', 'PEG', 'ES', 'PCG'],
            'Consumer Staples': ['PG', 'KO', 'PEP', 'WMT', 'COST', 'CL', 'KMB', 'GIS', 'K', 'HSY'],
            'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'BMY', 'AMGN'],
            'Financials': ['BAC', 'JPM', 'WFC', 'C', 'GS', 'MS', 'BLK', 'AXP', 'COF', 'USB']
        }
        
        # Market condition thresholds
        self.tech_cool_off_threshold = -0.05  # -5% tech underperformance
        self.momentum_reversal_threshold = -0.03  # -3% momentum reversal
        self.volatility_spike_threshold = 1.5  # 1.5x normal volatility
        
    def analyze_market_conditions(self, lookback_days: int = 30) -> Dict:
        """
        Analyze current market conditions and detect tech cool-offs.
        
        Returns:
            Dict with market condition analysis and recommendations
        """
        print(f"🔍 ANALYZING MARKET CONDITIONS ({lookback_days} days)")
        print("=" * 60)
        
        end_date = date.today()
        start_date = end_date - timedelta(days=lookback_days)
        
        # Get tech sector performance
        tech_performance = self._get_sector_performance(
            self.tech_symbols, start_date, end_date, "Technology"
        )
        
        # Get defensive sector performance
        defensive_performance = {}
        for sector_name, symbols in self.defensive_symbols.items():
            defensive_performance[sector_name] = self._get_sector_performance(
                symbols, start_date, end_date, sector_name
            )
        
        # Calculate relative performance
        avg_defensive_performance = sum(
            perf['total_return'] for perf in defensive_performance.values()
        ) / len(defensive_performance)
        
        tech_vs_defensive = tech_performance['total_return'] - avg_defensive_performance
        
        # Detect market conditions
        market_condition = self._detect_market_condition(
            tech_performance, defensive_performance, tech_vs_defensive
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(market_condition)
        
        # Cache results
        self._cache_market_conditions(market_condition, recommendations)
        
        return {
            'market_condition': market_condition,
            'recommendations': recommendations,
            'tech_performance': tech_performance,
            'defensive_performance': defensive_performance,
            'tech_vs_defensive': tech_vs_defensive
        }
    
    def _get_sector_performance(
        self, symbols: List[str], start_date: date, end_date: date, sector_name: str
    ) -> Dict:
        """Get sector performance metrics."""
        print(f"📊 Analyzing {sector_name} sector ({len(symbols)} symbols)...")
        
        if self.use_mock_data:
            # Use realistic mock data for testing
            return self._get_mock_sector_performance(sector_name)
        
        total_return = 0.0
        volatility = 0.0
        momentum = 0.0
        valid_symbols = 0
        
        for symbol in symbols[:20]:  # Limit to 20 symbols for speed
            try:
                # Get price data
                price_data = self.polygon_client.get_aggs(
                    symbol, 1, "day",
                    start_date.isoformat(), end_date.isoformat(),
                    limit=30, adjusted=True
                )
                
                if price_data and price_data.get("results"):
                    results = price_data["results"]
                    if len(results) >= 2:
                        # Calculate returns
                        start_price = results[0]['c']
                        end_price = results[-1]['c']
                        symbol_return = (end_price - start_price) / start_price
                        
                        # Calculate volatility (standard deviation of daily returns)
                        daily_returns = []
                        for i in range(1, len(results)):
                            daily_return = (results[i]['c'] - results[i-1]['c']) / results[i-1]['c']
                            daily_returns.append(daily_return)
                        
                        if daily_returns:
                            import statistics
                            symbol_volatility = statistics.stdev(daily_returns)
                            
                            # Calculate momentum (recent vs early performance)
                            mid_point = len(results) // 2
                            early_return = (results[mid_point]['c'] - results[0]['c']) / results[0]['c']
                            recent_return = (results[-1]['c'] - results[mid_point]['c']) / results[mid_point]['c']
                            symbol_momentum = recent_return - early_return
                            
                            total_return += symbol_return
                            volatility += symbol_volatility
                            momentum += symbol_momentum
                            valid_symbols += 1
                            
            except Exception as e:
                print(f"⚠️ Error analyzing {symbol}: {e}")
                continue
        
        if valid_symbols > 0:
            avg_return = total_return / valid_symbols
            avg_volatility = volatility / valid_symbols
            avg_momentum = momentum / valid_symbols
        else:
            avg_return = 0.0
            avg_volatility = 0.0
            avg_momentum = 0.0
        
        return {
            'sector_name': sector_name,
            'total_return': avg_return,
            'volatility': avg_volatility,
            'momentum': avg_momentum,
            'valid_symbols': valid_symbols,
            'total_symbols': len(symbols)
        }
    
    def _get_mock_sector_performance(self, sector_name: str) -> Dict:
        """Generate realistic mock sector performance data for testing."""
        import random
        
        # Simulate different market conditions
        if sector_name == "Technology":
            # Tech sector - simulate current AI boom
            total_return = random.uniform(0.15, 0.25)  # 15-25% return
            volatility = random.uniform(0.02, 0.04)    # 2-4% daily volatility
            momentum = random.uniform(0.05, 0.10)      # 5-10% momentum
        elif sector_name in ["Utilities", "Consumer Staples"]:
            # Defensive sectors - lower returns, lower volatility
            total_return = random.uniform(0.02, 0.08)  # 2-8% return
            volatility = random.uniform(0.01, 0.02)    # 1-2% daily volatility
            momentum = random.uniform(-0.02, 0.02)     # -2% to +2% momentum
        elif sector_name == "Healthcare":
            # Healthcare - moderate performance
            total_return = random.uniform(0.05, 0.12)  # 5-12% return
            volatility = random.uniform(0.015, 0.025)  # 1.5-2.5% daily volatility
            momentum = random.uniform(0.01, 0.05)      # 1-5% momentum
        elif sector_name == "Financials":
            # Financials - moderate performance
            total_return = random.uniform(0.03, 0.10)  # 3-10% return
            volatility = random.uniform(0.015, 0.03)   # 1.5-3% daily volatility
            momentum = random.uniform(-0.01, 0.04)     # -1% to +4% momentum
        else:
            # Default moderate performance
            total_return = random.uniform(0.05, 0.15)  # 5-15% return
            volatility = random.uniform(0.02, 0.03)    # 2-3% daily volatility
            momentum = random.uniform(0.0, 0.05)       # 0-5% momentum
        
        return {
            'sector_name': sector_name,
            'total_return': total_return,
            'volatility': volatility,
            'momentum': momentum,
            'valid_symbols': 20,
            'total_symbols': 20
        }
    
    def _detect_market_condition(
        self, tech_performance: Dict, defensive_performance: Dict, tech_vs_defensive: float
    ) -> Dict:
        """Detect current market condition based on performance analysis."""
        
        # Check for tech cool-off
        tech_cool_off = tech_vs_defensive < self.tech_cool_off_threshold
        
        # Check for momentum reversal
        momentum_reversal = tech_performance['momentum'] < self.momentum_reversal_threshold
        
        # Check for volatility spike
        avg_defensive_volatility = sum(
            perf['volatility'] for perf in defensive_performance.values()
        ) / len(defensive_performance)
        volatility_spike = tech_performance['volatility'] > (
            avg_defensive_volatility * self.volatility_spike_threshold
        )
        
        # Determine market condition
        if tech_cool_off and momentum_reversal:
            condition = "TECH_COOL_OFF"
            severity = "HIGH"
        elif tech_cool_off or momentum_reversal:
            condition = "TECH_WEAKNESS"
            severity = "MEDIUM"
        elif volatility_spike:
            condition = "TECH_VOLATILITY"
            severity = "LOW"
        else:
            condition = "TECH_BULLISH"
            severity = "NONE"
        
        return {
            'condition': condition,
            'severity': severity,
            'tech_cool_off': tech_cool_off,
            'momentum_reversal': momentum_reversal,
            'volatility_spike': volatility_spike,
            'tech_vs_defensive': tech_vs_defensive,
            'tech_momentum': tech_performance['momentum'],
            'tech_volatility': tech_performance['volatility']
        }
    
    def _generate_recommendations(self, market_condition: Dict) -> Dict:
        """Generate sector weight recommendations based on market condition."""
        
        condition = market_condition['condition']
        severity = market_condition['severity']
        
        if condition == "TECH_COOL_OFF":
            # High severity - significantly reduce tech exposure
            sector_weights = {
                'Technology': 0.40,  # Reduce from 88% to 40%
                'Healthcare': 0.20,
                'Financials': 0.15,
                'Communication Services': 0.10,
                'Consumer Discretionary': 0.08,
                'Energy': 0.04,
                'Utilities': 0.03
            }
            recommendation = "REDUCE_TECH_EXPOSURE"
            
        elif condition == "TECH_WEAKNESS":
            # Medium severity - moderate tech reduction
            sector_weights = {
                'Technology': 0.60,  # Reduce from 88% to 60%
                'Healthcare': 0.15,
                'Financials': 0.10,
                'Communication Services': 0.08,
                'Consumer Discretionary': 0.05,
                'Energy': 0.02
            }
            recommendation = "MODERATE_TECH_REDUCTION"
            
        elif condition == "TECH_VOLATILITY":
            # Low severity - slight tech reduction
            sector_weights = {
                'Technology': 0.75,  # Reduce from 88% to 75%
                'Healthcare': 0.10,
                'Financials': 0.08,
                'Communication Services': 0.05,
                'Consumer Discretionary': 0.02
            }
            recommendation = "SLIGHT_TECH_REDUCTION"
            
        else:  # TECH_BULLISH
            # Keep aggressive tech focus
            sector_weights = {
                'Technology': 0.88,  # Keep aggressive tech focus
                'Communication Services': 0.06,
                'Healthcare': 0.04,
                'Consumer Discretionary': 0.02
            }
            recommendation = "MAINTAIN_AGGRESSIVE_TECH"
        
        return {
            'recommendation': recommendation,
            'sector_weights': sector_weights,
            'tech_cap': sector_weights['Technology'],
            'diversification_level': 'HIGH' if sector_weights['Technology'] <= 0.60 else 'MEDIUM' if sector_weights['Technology'] <= 0.75 else 'LOW'
        }
    
    def _cache_market_conditions(self, market_condition: Dict, recommendations: Dict):
        """Cache market condition analysis."""
        cache_data = {
            'timestamp': date.today().isoformat(),
            'market_condition': market_condition,
            'recommendations': recommendations
        }
        
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to cache market conditions: {e}")
    
    def get_cached_conditions(self) -> Optional[Dict]:
        """Get cached market conditions if available and recent."""
        try:
            if os.path.exists(self.cache_path):
                with open(self.cache_path, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is recent (within 1 day)
                cache_date = date.fromisoformat(cache_data['timestamp'])
                if (date.today() - cache_date).days <= 1:
                    return cache_data
        except Exception:
            pass
        
        return None
    
    def get_dynamic_sector_weights(self) -> Dict[str, float]:
        """
        Get dynamic sector weights based on current market conditions.
        This is the main method to be called by the universe selector.
        """
        # Check cache first
        cached_conditions = self.get_cached_conditions()
        if cached_conditions:
            print("📊 Using cached market conditions")
            return cached_conditions['recommendations']['sector_weights']
        
        # Analyze current conditions
        print("🔍 Analyzing fresh market conditions...")
        analysis = self.analyze_market_conditions()
        
        return analysis['recommendations']['sector_weights']
    
    def print_market_analysis(self, analysis: Dict):
        """Print detailed market analysis."""
        condition = analysis['market_condition']
        recommendations = analysis['recommendations']
        
        print(f"\n🎯 MARKET CONDITION ANALYSIS")
        print("=" * 60)
        print(f"Condition: {condition['condition']}")
        print(f"Severity: {condition['severity']}")
        print(f"Tech vs Defensive: {condition['tech_vs_defensive']:.2%}")
        print(f"Tech Momentum: {condition['tech_momentum']:.2%}")
        print(f"Tech Volatility: {condition['tech_volatility']:.2%}")
        
        print(f"\n📊 RECOMMENDATIONS")
        print("=" * 60)
        print(f"Recommendation: {recommendations['recommendation']}")
        print(f"Tech Cap: {recommendations['tech_cap']:.0%}")
        print(f"Diversification: {recommendations['diversification_level']}")
        
        print(f"\n🏢 SECTOR WEIGHTS")
        print("=" * 60)
        for sector, weight in recommendations['sector_weights'].items():
            print(f"  {sector}: {weight:.0%}")
        
        print(f"\n📈 SECTOR PERFORMANCE")
        print("=" * 60)
        print(f"Technology: {analysis['tech_performance']['total_return']:.2%}")
        for sector, perf in analysis['defensive_performance'].items():
            print(f"{sector}: {perf['total_return']:.2%}")


def main():
    """Test the market condition monitor."""
    print("🧪 TESTING MARKET CONDITION MONITOR")
    print("=" * 60)
    
    monitor = MarketConditionMonitor()
    
    # Analyze current market conditions
    analysis = monitor.analyze_market_conditions(lookback_days=30)
    
    # Print detailed analysis
    monitor.print_market_analysis(analysis)
    
    # Test dynamic sector weights
    print(f"\n🔄 TESTING DYNAMIC SECTOR WEIGHTS")
    print("=" * 60)
    sector_weights = monitor.get_dynamic_sector_weights()
    print("Dynamic sector weights:")
    for sector, weight in sector_weights.items():
        print(f"  {sector}: {weight:.0%}")


if __name__ == "__main__":
    main()
