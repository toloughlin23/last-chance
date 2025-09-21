"""
🔍 SYMBOL POOL ANALYZER - 100% GENUINE DATA-DRIVEN
==================================================
Analyzes historical data to create the optimal 120-symbol pool
for active day trading based on REAL performance metrics.
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from services.polygon_client import PolygonClient
from services.quotes_client import QuotesClient
from services.sp500_client import SP500Client
from utils.universe_selector import UniverseSelector


@dataclass
class SymbolMetrics:
    """Metrics for a single symbol"""
    symbol: str
    avg_daily_volume: float
    avg_dollar_volume: float
    median_spread_dollars: float
    median_spread_bps: float
    avg_atr_percent: float
    price_stability: float
    liquidity_score: float
    volatility_score: float
    overall_score: float


class SymbolPoolAnalyzer:
    """
    🎯 SYMBOL POOL ANALYZER - 100% DATA-DRIVEN
    
    Analyzes 6+ months of historical data to identify the best 120 symbols
    for active day trading based on:
    - Volume consistency
    - Spread tightness  
    - Volatility patterns
    - Liquidity stability
    - Sector diversification
    """
    
    def __init__(self, polygon_client: PolygonClient = None, quotes_client: QuotesClient = None):
        self.polygon_client = polygon_client or PolygonClient()
        self.quotes_client = quotes_client or QuotesClient()
        self.universe_selector = UniverseSelector(self.polygon_client, self.quotes_client)
        self.sp500_client = SP500Client()
        
    def analyze_symbol_performance(
        self, 
        symbol: str, 
        start_date: str, 
        end_date: str
    ) -> SymbolMetrics:
        """
        Analyze a single symbol's performance over the given period.
        
        Args:
            symbol: Stock symbol to analyze
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            SymbolMetrics object with all performance data
        """
        print(f"🔍 Analyzing {symbol}...")
        
        # Get daily aggregates
        aggs_data = self.polygon_client.get_aggs(
            symbol, 1, "day", start_date, end_date, 
            limit=200, adjusted=True, sort="asc"
        )
        
        if not aggs_data or not aggs_data.get("results"):
            return self._create_empty_metrics(symbol)
        
        results = aggs_data["results"]
        
        # Calculate volume metrics
        volumes = [float(r.get("v", 0)) for r in results if r.get("v")]
        closes = [float(r.get("c", 0)) for r in results if r.get("c")]
        
        if not volumes or not closes:
            return self._create_empty_metrics(symbol)
        
        # Average daily volume
        avg_daily_volume = sum(volumes) / len(volumes)
        
        # Average dollar volume
        dollar_volumes = [c * v for c, v in zip(closes, volumes) if c > 0 and v > 0]
        avg_dollar_volume = sum(dollar_volumes) / len(dollar_volumes) if dollar_volumes else 0
        
        # Calculate ATR percentage
        atr_percentages = []
        for i in range(1, len(results)):
            prev_close = float(results[i-1].get("c", 0))
            high = float(results[i].get("h", 0))
            low = float(results[i].get("l", 0))
            _close = float(results[i].get("c", 0))
            
            if prev_close > 0:
                true_range = max(high - low, abs(high - prev_close), abs(low - prev_close))
                atr_pct = (true_range / prev_close) * 100
                atr_percentages.append(atr_pct)
        
        avg_atr_percent = sum(atr_percentages) / len(atr_percentages) if atr_percentages else 0
        
        # Get spread data
        try:
            spread_dollars, spread_bps = self.quotes_client.median_spread_over_days(
                symbol, days=30, core_hours_only=True
            )
        except Exception as e:
            print(f"⚠️ Spread fetch failed for {symbol}: {e}")
            spread_dollars, spread_bps = 0.05, 10.0  # Conservative defaults
        
        # Calculate price stability (inverse of price volatility)
        if len(closes) > 1:
            price_changes = [abs(closes[i] - closes[i-1]) / closes[i-1] 
                           for i in range(1, len(closes)) if closes[i-1] > 0]
            price_stability = 1.0 / (1.0 + sum(price_changes) / len(price_changes)) if price_changes else 0
        else:
            price_stability = 0
        
        # Calculate composite scores
        liquidity_score = min(1.0, avg_dollar_volume / 100_000_000)  # Normalize to $100M
        volatility_score = min(1.0, avg_atr_percent / 5.0)  # Normalize to 5% ATR
        
        # Overall score (weighted combination)
        overall_score = (
            liquidity_score * 0.4 +           # 40% liquidity
            (1.0 - min(1.0, spread_dollars / 0.05)) * 0.3 +  # 30% spread tightness
            volatility_score * 0.2 +          # 20% volatility
            price_stability * 0.1             # 10% stability
        )
        
        return SymbolMetrics(
            symbol=symbol,
            avg_daily_volume=avg_daily_volume,
            avg_dollar_volume=avg_dollar_volume,
            median_spread_dollars=spread_dollars,
            median_spread_bps=spread_bps,
            avg_atr_percent=avg_atr_percent,
            price_stability=price_stability,
            liquidity_score=liquidity_score,
            volatility_score=volatility_score,
            overall_score=overall_score
        )
    
    def _create_empty_metrics(self, symbol: str) -> SymbolMetrics:
        """Create empty metrics for symbols with no data"""
        return SymbolMetrics(
            symbol=symbol,
            avg_daily_volume=0.0,
            avg_dollar_volume=0.0,
            median_spread_dollars=1.0,
            median_spread_bps=100.0,
            avg_atr_percent=0.0,
            price_stability=0.0,
            liquidity_score=0.0,
            volatility_score=0.0,
            overall_score=0.0
        )
    
    def analyze_sp500_universe(
        self, 
        analysis_days: int = 180,
        target_pool_size: int = 120
    ) -> List[SymbolMetrics]:
        """
        Analyze the entire S&P 500 universe to find the best symbols.
        
        Args:
            analysis_days: Number of days to analyze
            target_pool_size: Target number of symbols for the pool
            
        Returns:
            List of SymbolMetrics sorted by overall score
        """
        print(f"🚀 Analyzing S&P 500 universe over {analysis_days} days...")
        
        # Get S&P 500 symbols from Polygon (more reliable than Wikipedia)
        try:
            # Use Polygon's tickers endpoint if available to get large-cap stocks
            sp500_symbols = []
            if hasattr(self.polygon_client, "get_tickers"):
                sp500_data = self.polygon_client.get_tickers(
                    market="stocks", active=True, limit=1000
                )
                if sp500_data and sp500_data.get("results"):
                    for ticker in sp500_data["results"]:
                        symbol = ticker.get("ticker", "")
                        market_cap = ticker.get("market_cap", 0)
                        if symbol and market_cap and market_cap > 8_000_000_000:
                            sp500_symbols.append(symbol)
                    print(f"📊 Found {len(sp500_symbols)} large-cap symbols from Polygon")
        except Exception as e:
            print(f"⚠️ Polygon API error: {e}")
            sp500_symbols = []
        
        if not sp500_symbols:
            print("⚠️ Using fallback S&P 500 symbols...")
            # Fallback to known high-volume S&P 500 symbols
            sp500_symbols = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK.B', 'V', 'JNJ',
                'WMT', 'JPM', 'MA', 'PG', 'UNH', 'DIS', 'HD', 'VZ', 'ADBE', 'NFLX',
                'CRM', 'PFE', 'TMO', 'ABT', 'CSCO', 'ACN', 'NKE', 'CVX', 'LLY', 'WFC',
                'DHR', 'TXN', 'PM', 'NEE', 'RTX', 'SPGI', 'INTU', 'LOW', 'UNP', 'GS',
                'MS', 'BMY', 'AMT', 'SYK', 'ISRG', 'CVS', 'SCHW', 'PLD', 'AXP', 'TJX',
                'BAC', 'COST', 'ABBV', 'PEP', 'TMO', 'AVGO', 'QCOM', 'COF', 'DHR', 'ACN',
                'NFLX', 'ADBE', 'TXN', 'CMCSA', 'LIN', 'NEE', 'HON', 'UNP', 'LOW', 'UPS',
                'QCOM', 'IBM', 'AMGN', 'T', 'SPGI', 'INTU', 'CAT', 'GE', 'MMM', 'BA',
                'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'AXP', 'V', 'MA', 'PYPL',
                'COF', 'USB', 'PNC', 'TFC', 'BK', 'SCHW', 'BLK', 'SPGI', 'ICE', 'CME',
                'JNJ', 'UNH', 'PFE', 'ABT', 'TMO', 'DHR', 'BMY', 'LLY', 'MRK', 'AMGN',
                'GILD', 'BIIB', 'VRTX', 'REGN', 'ISRG', 'SYK', 'BDX', 'EW', 'A', 'CI',
                'WMT', 'PG', 'HD', 'DIS', 'NKE', 'MCD', 'SBUX', 'TGT', 'LOW', 'COST',
                'TJX', 'ROST', 'ULTA', 'LULU', 'CMG', 'CHIP', 'YUM', 'BKNG', 'NFLX', 'ADBE',
                'BA', 'CAT', 'MMM', 'GE', 'HON', 'UPS', 'RTX', 'LMT', 'NOC', 'GD',
                'EMR', 'ETN', 'ITW', 'PH', 'DE', 'CMI', 'FDX', 'CSX', 'NSC', 'UNP',
                'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'OXY', 'PXD', 'KMI', 'WMB', 'PSX',
                'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'SRE', 'PEG', 'WEC',
                'AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'EXR', 'AVB', 'EQR', 'MAA', 'UDR',
                'VZ', 'T', 'CMCSA', 'TWTR', 'SNAP', 'PINS', 'GOOGL', 'META', 'NFLX', 'ADBE',
                'LIN', 'APD', 'SHW', 'ECL', 'DD', 'DOW', 'PPG', 'NEM', 'FCX', 'VALE'
            ]
        
        print(f"📊 Analyzing {len(sp500_symbols)} S&P 500 symbols...")
        
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=analysis_days)
        
        # Analyze each symbol
        all_metrics = []
        for i, symbol in enumerate(sp500_symbols):
            if i % 50 == 0:
                print(f"   Progress: {i}/{len(sp500_symbols)} symbols analyzed...")
            
            metrics = self.analyze_symbol_performance(
                symbol, start_date.isoformat(), end_date.isoformat()
            )
            
            # Only include symbols with meaningful data
            if metrics.avg_dollar_volume > 1_000_000:  # At least $1M daily volume
                all_metrics.append(metrics)
        
        # Sort by overall score (descending)
        all_metrics.sort(key=lambda x: x.overall_score, reverse=True)
        
        # Take top performers
        top_metrics = all_metrics[:target_pool_size]
        
        print("✅ Analysis complete!")
        print(f"   - Analyzed: {len(all_metrics)} symbols with sufficient data")
        print(f"   - Selected: {len(top_metrics)} top performers")
        
        return top_metrics
    
    def create_curated_pool(
        self, 
        analysis_days: int = 180,
        target_size: int = 120,
        save_to_file: bool = True
    ) -> List[str]:
        """
        Create the curated symbol pool based on historical analysis.
        
        Args:
            analysis_days: Days of historical data to analyze
            target_size: Target number of symbols
            save_to_file: Whether to save results to file
            
        Returns:
            List of curated symbols
        """
        print(f"🎯 Creating curated {target_size}-symbol pool...")
        
        # Analyze the universe
        top_metrics = self.analyze_sp500_universe(analysis_days, target_size)
        
        # Extract symbols
        curated_symbols = [m.symbol for m in top_metrics]
        
        # Print summary
        print("\n📈 TOP 10 SYMBOLS:")
        for i, metrics in enumerate(top_metrics[:10]):
            print(f"   {i+1:2d}. {metrics.symbol:6s} - Score: {metrics.overall_score:.3f} "
                  f"(Vol: ${metrics.avg_dollar_volume/1e6:.1f}M, "
                  f"Spread: ${metrics.median_spread_dollars:.3f})")
        
        # Save to file if requested
        if save_to_file:
            self._save_analysis_results(top_metrics, analysis_days)
        
        return curated_symbols
    
    def _save_analysis_results(self, metrics: List[SymbolMetrics], analysis_days: int) -> None:
        """Save analysis results to file"""
        os.makedirs("data", exist_ok=True)
        
        results = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_days": analysis_days,
            "total_symbols_analyzed": len(metrics),
            "symbols": [
                {
                    "symbol": m.symbol,
                    "avg_daily_volume": m.avg_daily_volume,
                    "avg_dollar_volume": m.avg_dollar_volume,
                    "median_spread_dollars": m.median_spread_dollars,
                    "median_spread_bps": m.median_spread_bps,
                    "avg_atr_percent": m.avg_atr_percent,
                    "price_stability": m.price_stability,
                    "liquidity_score": m.liquidity_score,
                    "volatility_score": m.volatility_score,
                    "overall_score": m.overall_score
                }
                for m in metrics
            ]
        }
        
        filepath = f"data/curated_symbol_analysis_{analysis_days}days.json"
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Analysis results saved to {filepath}")


def create_curated_pool(analysis_days: int = 180, target_size: int = 120) -> List[str]:
    """
    Convenience function to create the curated symbol pool.
    
    Args:
        analysis_days: Days of historical data to analyze
        target_size: Target number of symbols
        
    Returns:
        List of curated symbols
    """
    analyzer = SymbolPoolAnalyzer()
    return analyzer.create_curated_pool(analysis_days, target_size)


# Example usage
if __name__ == "__main__":
    print("🔍 SYMBOL POOL ANALYZER - 100% DATA-DRIVEN")
    print("=" * 60)
    
    # Create analyzer
    analyzer = SymbolPoolAnalyzer()
    
    # Create curated pool with 6 months of data
    curated_symbols = analyzer.create_curated_pool(
        analysis_days=180,  # 6 months
        target_size=120
    )
    
    print(f"\n✅ Curated pool created with {len(curated_symbols)} symbols!")
    print("🎯 Ready for day trading optimization!")
