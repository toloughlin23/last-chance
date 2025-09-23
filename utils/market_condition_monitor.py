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

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

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
        
        # ENHANCED MARKET CONDITION THRESHOLDS - MAXIMUM SENSITIVITY
        # Multiple timeframes for comprehensive analysis
        self.tech_cool_off_thresholds = {
            'short_term': -0.02,    # -2% tech underperformance (1-5 days)
            'medium_term': -0.03,   # -3% tech underperformance (5-15 days)
            'long_term': -0.05,     # -5% tech underperformance (15-30 days)
        }
        
        self.momentum_reversal_thresholds = {
            'immediate': -0.01,     # -1% immediate momentum reversal
            'short_term': -0.02,    # -2% short-term momentum reversal
            'medium_term': -0.03,   # -3% medium-term momentum reversal
        }
        
        self.volatility_spike_thresholds = {
            'mild': 1.2,           # 1.2x normal volatility (early warning)
            'moderate': 1.5,        # 1.5x normal volatility (caution)
            'severe': 2.0,          # 2.0x normal volatility (danger)
        }
        
        # Additional sensitivity metrics
        self.relative_strength_threshold = -0.01  # -1% relative strength vs market
        self.volume_spike_threshold = 2.0         # 2x normal volume
        self.correlation_break_threshold = 0.7    # Correlation breakdown
        self.support_level_break_threshold = -0.05  # -5% support level break
        
        # Multi-timeframe analysis
        self.timeframes = {
            'immediate': 3,    # 3 days - immediate signals
            'short': 7,        # 7 days - short-term trends
            'medium': 15,      # 15 days - medium-term trends
            'long': 30,        # 30 days - long-term trends
        }
        
    def analyze_market_conditions(self, lookback_days: int = 30) -> Dict:
        """
        ENHANCED multi-timeframe market condition analysis with maximum sensitivity.
        
        Returns:
            Dict with comprehensive market condition analysis and recommendations
        """
        print(f"🔍 ENHANCED MARKET CONDITIONS ANALYSIS ({lookback_days} days)")
        print("=" * 70)
        print("🎯 MAXIMUM SENSITIVITY - KITCHEN SINK APPROACH")
        print("=" * 70)
        
        end_date = date.today()
        
        # Multi-timeframe analysis for maximum sensitivity
        timeframe_analysis = {}
        for timeframe_name, days in self.timeframes.items():
            if days <= lookback_days:
                start_date = end_date - timedelta(days=days)
                print(f"\n📊 Analyzing {timeframe_name} timeframe ({days} days)...")
                
                # Get tech sector performance for this timeframe
                tech_perf = self._get_sector_performance(
                    self.tech_symbols, start_date, end_date, f"Technology_{timeframe_name}"
                )
                
                # Get defensive sector performance for this timeframe
                defensive_perf = {}
                for sector_name, symbols in self.defensive_symbols.items():
                    defensive_perf[sector_name] = self._get_sector_performance(
                        symbols, start_date, end_date, f"{sector_name}_{timeframe_name}"
                    )
                
                # Calculate relative performance
                avg_defensive = sum(
                    perf['total_return'] for perf in defensive_perf.values()
                ) / len(defensive_perf)
                
                tech_vs_defensive = tech_perf['total_return'] - avg_defensive
                
                timeframe_analysis[timeframe_name] = {
                    'tech_performance': tech_perf,
                    'defensive_performance': defensive_perf,
                    'tech_vs_defensive': tech_vs_defensive,
                    'days': days
                }
        
        # Enhanced market condition detection with multi-timeframe signals
        market_condition = self._detect_enhanced_market_condition(timeframe_analysis)
        
        # Generate enhanced recommendations
        recommendations = self._generate_enhanced_recommendations(market_condition, timeframe_analysis)
        
        # Cache results
        self._cache_market_conditions(market_condition, recommendations)
        
        return {
            'market_condition': market_condition,
            'recommendations': recommendations,
            'timeframe_analysis': timeframe_analysis,
            'analysis_summary': self._generate_analysis_summary(timeframe_analysis)
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
                        
                        if daily_returns and len(daily_returns) >= 2:
                            import statistics
                            symbol_volatility = statistics.stdev(daily_returns)
                        else:
                            symbol_volatility = 0.0  # Not enough data for volatility calculation
                        
                        # Calculate momentum (recent vs early performance)
                        if len(results) >= 3:  # Need at least 3 data points for momentum
                            mid_point = len(results) // 2
                            early_return = (results[mid_point]['c'] - results[0]['c']) / results[0]['c']
                            recent_return = (results[-1]['c'] - results[mid_point]['c']) / results[mid_point]['c']
                            symbol_momentum = recent_return - early_return
                        else:
                            symbol_momentum = 0.0  # Not enough data for momentum calculation
                        
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
    
    def _detect_enhanced_market_condition(self, timeframe_analysis: Dict) -> Dict:
        """ENHANCED market condition detection with multi-timeframe analysis."""
        
        # Analyze signals across all timeframes
        signals = {
            'immediate_cool_off': False,
            'short_term_cool_off': False,
            'medium_term_cool_off': False,
            'long_term_cool_off': False,
            'immediate_momentum_reversal': False,
            'short_term_momentum_reversal': False,
            'medium_term_momentum_reversal': False,
            'volatility_spike_mild': False,
            'volatility_spike_moderate': False,
            'volatility_spike_severe': False,
            'relative_strength_weakness': False,
            'correlation_breakdown': False,
        }
        
        # Check each timeframe for signals
        for timeframe_name, analysis in timeframe_analysis.items():
            tech_perf = analysis['tech_performance']
            defensive_perf = analysis['defensive_performance']
            tech_vs_defensive = analysis['tech_vs_defensive']
            
            # Cool-off detection across timeframes
            if timeframe_name == 'immediate':
                signals['immediate_cool_off'] = tech_vs_defensive < self.tech_cool_off_thresholds['short_term']
                signals['immediate_momentum_reversal'] = tech_perf['momentum'] < self.momentum_reversal_thresholds['immediate']
            elif timeframe_name == 'short':
                signals['short_term_cool_off'] = tech_vs_defensive < self.tech_cool_off_thresholds['short_term']
                signals['short_term_momentum_reversal'] = tech_perf['momentum'] < self.momentum_reversal_thresholds['short_term']
            elif timeframe_name == 'medium':
                signals['medium_term_cool_off'] = tech_vs_defensive < self.tech_cool_off_thresholds['medium_term']
                signals['medium_term_momentum_reversal'] = tech_perf['momentum'] < self.momentum_reversal_thresholds['medium_term']
            elif timeframe_name == 'long':
                signals['long_term_cool_off'] = tech_vs_defensive < self.tech_cool_off_thresholds['long_term']
            
            # Volatility spike detection
            avg_defensive_volatility = sum(
                perf['volatility'] for perf in defensive_perf.values()
            ) / len(defensive_perf)
            
            volatility_ratio = tech_perf['volatility'] / max(avg_defensive_volatility, 0.001)
            
            if volatility_ratio >= self.volatility_spike_thresholds['severe']:
                signals['volatility_spike_severe'] = True
            elif volatility_ratio >= self.volatility_spike_thresholds['moderate']:
                signals['volatility_spike_moderate'] = True
            elif volatility_ratio >= self.volatility_spike_thresholds['mild']:
                signals['volatility_spike_mild'] = True
            
            # Relative strength weakness
            if tech_vs_defensive < self.relative_strength_threshold:
                signals['relative_strength_weakness'] = True
        
        # Determine market condition with enhanced logic
        condition, severity = self._determine_enhanced_condition(signals, timeframe_analysis)
        
        return {
            'condition': condition,
            'severity': severity,
            'signals': signals,
            'timeframe_analysis': timeframe_analysis,
            'confidence_score': self._calculate_confidence_score(signals)
        }
    
    def _determine_enhanced_condition(self, signals: Dict, timeframe_analysis: Dict) -> Tuple[str, str]:
        """Determine market condition with enhanced multi-signal analysis."""
        
        # Count critical signals
        critical_signals = sum([
            signals['immediate_cool_off'],
            signals['short_term_cool_off'],
            signals['immediate_momentum_reversal'],
            signals['volatility_spike_severe']
        ])
        
        warning_signals = sum([
            signals['medium_term_cool_off'],
            signals['short_term_momentum_reversal'],
            signals['volatility_spike_moderate'],
            signals['relative_strength_weakness']
        ])
        
        early_warning_signals = sum([
            signals['long_term_cool_off'],
            signals['medium_term_momentum_reversal'],
            signals['volatility_spike_mild']
        ])
        
        # Enhanced condition determination
        if critical_signals >= 3:
            return "TECH_COOL_OFF", "CRITICAL"
        elif critical_signals >= 2 or (critical_signals >= 1 and warning_signals >= 2):
            return "TECH_COOL_OFF", "HIGH"
        elif critical_signals >= 1 or warning_signals >= 3:
            return "TECH_WEAKNESS", "HIGH"
        elif warning_signals >= 2 or (warning_signals >= 1 and early_warning_signals >= 2):
            return "TECH_WEAKNESS", "MEDIUM"
        elif warning_signals >= 1 or early_warning_signals >= 3:
            return "TECH_VOLATILITY", "MEDIUM"
        elif early_warning_signals >= 2:
            return "TECH_VOLATILITY", "LOW"
        elif early_warning_signals >= 1:
            return "TECH_CAUTION", "LOW"
        else:
            return "TECH_BULLISH", "NONE"
    
    def _calculate_confidence_score(self, signals: Dict) -> float:
        """Calculate confidence score for the market condition assessment."""
        total_signals = len(signals)
        active_signals = sum(1 for signal in signals.values() if signal)
        return active_signals / total_signals
    
    def _generate_enhanced_recommendations(self, market_condition: Dict, timeframe_analysis: Dict) -> Dict:
        """Generate ENHANCED sector weight recommendations with maximum sensitivity."""
        
        condition = market_condition['condition']
        severity = market_condition['severity']
        signals = market_condition['signals']
        confidence = market_condition['confidence_score']
        
        # Enhanced recommendation logic with maximum sensitivity
        if condition == "TECH_COOL_OFF" and severity == "CRITICAL":
            # CRITICAL - Maximum protection
            sector_weights = {
                'Technology': 0.25,  # Reduce to 25% - maximum protection
                'Healthcare': 0.25,
                'Financials': 0.20,
                'Utilities': 0.15,
                'Consumer Staples': 0.10,
                'Communication Services': 0.05
            }
            recommendation = "MAXIMUM_TECH_REDUCTION"
            urgency = "IMMEDIATE"
            
        elif condition == "TECH_COOL_OFF" and severity == "HIGH":
            # HIGH - Significant protection
            sector_weights = {
                'Technology': 0.35,  # Reduce to 35%
                'Healthcare': 0.20,
                'Financials': 0.18,
                'Utilities': 0.12,
                'Consumer Staples': 0.10,
                'Communication Services': 0.05
            }
            recommendation = "SIGNIFICANT_TECH_REDUCTION"
            urgency = "HIGH"
            
        elif condition == "TECH_WEAKNESS" and severity == "HIGH":
            # HIGH weakness - Moderate protection
            sector_weights = {
                'Technology': 0.50,  # Reduce to 50%
                'Healthcare': 0.18,
                'Financials': 0.15,
                'Communication Services': 0.10,
                'Consumer Discretionary': 0.05,
                'Utilities': 0.02
            }
            recommendation = "MODERATE_TECH_REDUCTION"
            urgency = "MEDIUM"
            
        elif condition == "TECH_WEAKNESS" and severity == "MEDIUM":
            # MEDIUM weakness - Light protection
            sector_weights = {
                'Technology': 0.65,  # Reduce to 65%
                'Healthcare': 0.15,
                'Financials': 0.12,
                'Communication Services': 0.06,
                'Consumer Discretionary': 0.02
            }
            recommendation = "LIGHT_TECH_REDUCTION"
            urgency = "LOW"
            
        elif condition == "TECH_VOLATILITY" and severity == "MEDIUM":
            # MEDIUM volatility - Slight protection
            sector_weights = {
                'Technology': 0.75,  # Reduce to 75%
                'Healthcare': 0.12,
                'Financials': 0.08,
                'Communication Services': 0.05
            }
            recommendation = "SLIGHT_TECH_REDUCTION"
            urgency = "LOW"
            
        elif condition == "TECH_VOLATILITY" and severity == "LOW":
            # LOW volatility - Minimal protection
            sector_weights = {
                'Technology': 0.80,  # Reduce to 80%
                'Healthcare': 0.10,
                'Financials': 0.06,
                'Communication Services': 0.04
            }
            recommendation = "MINIMAL_TECH_REDUCTION"
            urgency = "VERY_LOW"
            
        elif condition == "TECH_CAUTION":
            # CAUTION - Watch closely
            sector_weights = {
                'Technology': 0.85,  # Slight reduction to 85%
                'Healthcare': 0.08,
                'Financials': 0.05,
                'Communication Services': 0.02
            }
            recommendation = "TECH_CAUTION_MODE"
            urgency = "VERY_LOW"
            
        else:  # TECH_BULLISH
            # Keep aggressive tech focus
            sector_weights = {
                'Technology': 0.88,  # Keep aggressive tech focus
                'Communication Services': 0.06,
                'Healthcare': 0.04,
                'Consumer Discretionary': 0.02
            }
            recommendation = "MAINTAIN_AGGRESSIVE_TECH"
            urgency = "NONE"
        
        return {
            'recommendation': recommendation,
            'sector_weights': sector_weights,
            'tech_cap': sector_weights['Technology'],
            'diversification_level': self._calculate_diversification_level(sector_weights['Technology']),
            'urgency': urgency,
            'confidence_score': confidence,
            'risk_level': self._calculate_risk_level(condition, severity),
            'adjustment_magnitude': self._calculate_adjustment_magnitude(sector_weights['Technology'])
        }
    
    def _calculate_diversification_level(self, tech_weight: float) -> str:
        """Calculate diversification level based on tech weight."""
        if tech_weight <= 0.40:
            return "MAXIMUM"
        elif tech_weight <= 0.60:
            return "HIGH"
        elif tech_weight <= 0.75:
            return "MEDIUM"
        elif tech_weight <= 0.85:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _calculate_risk_level(self, condition: str, severity: str) -> str:
        """Calculate risk level based on condition and severity."""
        if condition == "TECH_COOL_OFF" and severity == "CRITICAL":
            return "CRITICAL"
        elif condition == "TECH_COOL_OFF" and severity == "HIGH":
            return "HIGH"
        elif condition == "TECH_WEAKNESS" and severity == "HIGH":
            return "HIGH"
        elif condition == "TECH_WEAKNESS" and severity == "MEDIUM":
            return "MEDIUM"
        elif condition == "TECH_VOLATILITY":
            return "MEDIUM"
        elif condition == "TECH_CAUTION":
            return "LOW"
        else:
            return "MINIMAL"
    
    def _calculate_adjustment_magnitude(self, tech_weight: float) -> str:
        """Calculate the magnitude of tech weight adjustment."""
        base_tech_weight = 0.88  # Normal aggressive tech weight
        adjustment = base_tech_weight - tech_weight
        
        if adjustment >= 0.50:
            return "MASSIVE"
        elif adjustment >= 0.30:
            return "SIGNIFICANT"
        elif adjustment >= 0.15:
            return "MODERATE"
        elif adjustment >= 0.05:
            return "LIGHT"
        else:
            return "MINIMAL"
    
    def _generate_analysis_summary(self, timeframe_analysis: Dict) -> Dict:
        """Generate comprehensive analysis summary."""
        summary = {
            'total_timeframes_analyzed': len(timeframe_analysis),
            'timeframe_details': {},
            'overall_tech_performance': 0.0,
            'overall_defensive_performance': 0.0,
            'performance_trend': 'UNKNOWN'
        }
        
        tech_returns = []
        defensive_returns = []
        
        for timeframe_name, analysis in timeframe_analysis.items():
            tech_perf = analysis['tech_performance']
            defensive_perf = analysis['defensive_performance']
            
            tech_returns.append(tech_perf['total_return'])
            defensive_returns.append(sum(p['total_return'] for p in defensive_perf.values()) / len(defensive_perf))
            
            summary['timeframe_details'][timeframe_name] = {
                'tech_return': tech_perf['total_return'],
                'tech_momentum': tech_perf['momentum'],
                'tech_volatility': tech_perf['volatility'],
                'tech_vs_defensive': analysis['tech_vs_defensive']
            }
        
        summary['overall_tech_performance'] = sum(tech_returns) / len(tech_returns)
        summary['overall_defensive_performance'] = sum(defensive_returns) / len(defensive_returns)
        
        # Determine performance trend
        if len(tech_returns) >= 2:
            if tech_returns[-1] > tech_returns[0]:
                summary['performance_trend'] = 'IMPROVING'
            elif tech_returns[-1] < tech_returns[0]:
                summary['performance_trend'] = 'DETERIORATING'
            else:
                summary['performance_trend'] = 'STABLE'
        
        return summary
    
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
        
        print(f"\n🎯 ENHANCED MARKET CONDITION ANALYSIS")
        print("=" * 70)
        print(f"Condition: {condition['condition']}")
        print(f"Severity: {condition['severity']}")
        print(f"Confidence Score: {condition['confidence_score']:.2%}")
        
        # Print enhanced signals
        if 'signals' in condition:
            print(f"\n🚨 DETECTED SIGNALS")
            print("=" * 70)
            active_signals = [signal for signal, active in condition['signals'].items() if active]
            if active_signals:
                for signal in active_signals:
                    print(f"  ⚠️ {signal.replace('_', ' ').title()}")
            else:
                print("  ✅ No warning signals detected")
        
        print(f"\n📊 ENHANCED RECOMMENDATIONS")
        print("=" * 70)
        print(f"Recommendation: {recommendations['recommendation']}")
        print(f"Tech Cap: {recommendations['tech_cap']:.0%}")
        print(f"Diversification: {recommendations['diversification_level']}")
        print(f"Urgency: {recommendations['urgency']}")
        print(f"Risk Level: {recommendations['risk_level']}")
        print(f"Adjustment: {recommendations['adjustment_magnitude']}")
        
        print(f"\n🏢 DYNAMIC SECTOR WEIGHTS")
        print("=" * 70)
        for sector, weight in recommendations['sector_weights'].items():
            print(f"  {sector}: {weight:.0%}")
        
        # Print timeframe analysis if available
        if 'timeframe_analysis' in analysis:
            print(f"\n📈 MULTI-TIMEFRAME ANALYSIS")
            print("=" * 70)
            for timeframe, data in analysis['timeframe_analysis'].items():
                tech_perf = data['tech_performance']
                print(f"  {timeframe.title()} ({data['days']} days):")
                print(f"    Tech Return: {tech_perf['total_return']:.2%}")
                print(f"    Tech Momentum: {tech_perf['momentum']:.2%}")
                print(f"    Tech vs Defensive: {data['tech_vs_defensive']:.2%}")
        
        # Print analysis summary
        if 'analysis_summary' in analysis:
            summary = analysis['analysis_summary']
            print(f"\n📊 ANALYSIS SUMMARY")
            print("=" * 70)
            print(f"Timeframes Analyzed: {summary['total_timeframes_analyzed']}")
            print(f"Overall Tech Performance: {summary['overall_tech_performance']:.2%}")
            print(f"Overall Defensive Performance: {summary['overall_defensive_performance']:.2%}")
            print(f"Performance Trend: {summary['performance_trend']}")


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
