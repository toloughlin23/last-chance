#!/usr/bin/env python3
"""
🧪 ADVANCED NEWS SENTIMENT INTEGRATION TEST
==========================================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Test the enhanced Advanced News Sentiment Analysis system
- Real API integration testing
- Multi-source sentiment validation
- Confidence scoring verification
- Real-time processing testing
"""

import os
import pytest
from datetime import datetime, UTC

from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis, SentimentResult


@pytest.mark.integration
def test_advanced_news_sentiment_initialization():
    """Test Advanced News Sentiment Analysis initialization"""
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Verify initialization
    assert analyzer is not None
    assert len(analyzer.sources) == 3  # Polygon, AlphaVantage, NewsAPI
    assert analyzer.cache_ttl == 300  # 5 minutes
    assert 'confidence_weights' in analyzer.__dict__
    assert 'market_conditions' in analyzer.__dict__


@pytest.mark.integration
def test_advanced_sentiment_analysis_with_real_polygon():
    """Test sentiment analysis with real Polygon API data"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping advanced sentiment test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test with a single symbol
    result = analyzer.analyze_symbol_sentiment("AAPL", lookback_hours=24, use_cache=False)
    
    # Verify result structure
    assert isinstance(result, SentimentResult)
    assert result.symbol == "AAPL"
    assert -1.0 <= result.sentiment_score <= 1.0
    assert 0.0 <= result.confidence <= 1.0
    assert 0.0 <= result.market_impact <= 1.0
    assert result.source_count >= 0
    assert result.article_count >= 0
    assert isinstance(result.sources_used, list)
    assert isinstance(result.timestamp, datetime)


@pytest.mark.integration
def test_multi_symbol_sentiment_analysis():
    """Test sentiment analysis for multiple symbols"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping multi-symbol test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test with multiple symbols
    symbols = ["AAPL", "MSFT", "GOOGL"]
    results = analyzer.analyze_multiple_symbols(symbols, lookback_hours=24)
    
    # Verify results
    assert len(results) == len(symbols)
    for symbol in symbols:
        assert symbol in results
        result = results[symbol]
        assert isinstance(result, SentimentResult)
        assert result.symbol == symbol
        assert -1.0 <= result.sentiment_score <= 1.0
        assert 0.0 <= result.confidence <= 1.0


@pytest.mark.integration
def test_sentiment_prioritization():
    """Test symbol prioritization by sentiment"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping prioritization test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test prioritization
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    prioritized = analyzer.get_priority_symbols(symbols, lookback_hours=24, min_confidence=0.1)
    
    # Verify prioritization
    assert isinstance(prioritized, list)
    assert len(prioritized) <= len(symbols)
    assert all(symbol in symbols for symbol in prioritized)


@pytest.mark.integration
def test_real_time_sentiment_summary():
    """Test real-time sentiment summary generation"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping real-time summary test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test real-time summary
    symbols = ["AAPL", "MSFT"]
    summary = analyzer.get_real_time_sentiment_summary(symbols, lookback_hours=1)
    
    # Verify summary structure
    assert isinstance(summary, dict)
    assert "timestamp" in summary
    assert "symbol_count" in summary
    assert "analyzed_count" in summary
    assert "average_sentiment" in summary
    assert "average_confidence" in summary
    assert "average_market_impact" in summary
    assert "high_confidence_count" in summary
    assert "positive_sentiment_count" in summary
    assert "negative_sentiment_count" in summary
    assert "high_impact_count" in summary
    
    # Verify summary values
    assert summary["symbol_count"] == len(symbols)
    assert summary["analyzed_count"] >= 0
    assert -1.0 <= summary["average_sentiment"] <= 1.0
    assert 0.0 <= summary["average_confidence"] <= 1.0
    assert 0.0 <= summary["average_market_impact"] <= 1.0


@pytest.mark.integration
def test_sentiment_caching():
    """Test sentiment analysis caching functionality"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping caching test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test cache stats before analysis
    initial_stats = analyzer.get_cache_stats()
    assert initial_stats["total_entries"] == 0
    
    # Perform analysis with caching
    result1 = analyzer.analyze_symbol_sentiment("AAPL", lookback_hours=24, use_cache=True)
    
    # Check cache stats after analysis
    stats_after = analyzer.get_cache_stats()
    assert stats_after["total_entries"] == 1
    assert stats_after["active_entries"] == 1
    
    # Perform same analysis again (should use cache)
    result2 = analyzer.analyze_symbol_sentiment("AAPL", lookback_hours=24, use_cache=True)
    
    # Results should be identical (from cache)
    assert result1.symbol == result2.symbol
    assert result1.sentiment_score == result2.sentiment_score
    assert result1.confidence == result2.confidence
    
    # Test cache clearing
    analyzer.clear_cache()
    final_stats = analyzer.get_cache_stats()
    assert final_stats["total_entries"] == 0


@pytest.mark.integration
def test_advanced_sentiment_patterns():
    """Test advanced sentiment pattern recognition"""
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test positive sentiment patterns
    positive_text = "Apple beats earnings expectations with record revenue growth and strong guidance"
    sentiment, confidence = analyzer._analyze_sentiment_advanced(positive_text)
    assert sentiment > 0.0  # Should be positive
    assert confidence > 0.0  # Should have some confidence
    
    # Test negative sentiment patterns
    negative_text = "Company misses earnings targets and cuts guidance due to market challenges"
    sentiment, confidence = analyzer._analyze_sentiment_advanced(negative_text)
    assert sentiment < 0.0  # Should be negative
    assert confidence > 0.0  # Should have some confidence
    
    # Test neutral text
    neutral_text = "The company reported quarterly results as expected"
    sentiment, confidence = analyzer._analyze_sentiment_advanced(neutral_text)
    assert abs(sentiment) < 0.5  # Should be relatively neutral


@pytest.mark.integration
def test_market_impact_calculation():
    """Test market impact calculation"""
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test high impact articles
    high_impact_articles = [
        {"title": "Apple reports record earnings", "description": "CEO announces major acquisition"},
        {"title": "SEC investigation launched", "description": "Company faces regulatory scrutiny"}
    ]
    high_impact = analyzer._calculate_market_impact(high_impact_articles)
    assert high_impact > 0.0
    
    # Test low impact articles
    low_impact_articles = [
        {"title": "Regular trading day", "description": "Normal market activity"},
        {"title": "Weather update", "description": "Sunny day forecast"}
    ]
    low_impact = analyzer._calculate_market_impact(low_impact_articles)
    assert low_impact < high_impact


@pytest.mark.integration
def test_sentiment_analysis_save_load():
    """Test saving and loading sentiment analysis results"""
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping save/load test.")
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Perform analysis
    symbols = ["AAPL", "MSFT"]
    results = analyzer.analyze_multiple_symbols(symbols, lookback_hours=24)
    
    # Test saving
    test_file = "test_sentiment_results.json"
    analyzer.save_sentiment_analysis(results, test_file)
    
    # Verify file was created
    assert os.path.exists(test_file)
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)


def test_advanced_sentiment_confidence_weights():
    """Test confidence weight configuration"""
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Verify confidence weights are properly configured
    weights = analyzer.confidence_weights
    assert "source_reliability" in weights
    assert "article_count" in weights
    assert "pattern_matches" in weights
    assert "text_quality" in weights
    
    # Verify weights sum to reasonable value
    total_weight = sum(weights.values())
    assert 0.8 <= total_weight <= 1.2  # Should be close to 1.0


def test_market_conditions_configuration():
    """Test market conditions configuration"""
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Verify market conditions are properly configured
    conditions = analyzer.market_conditions
    assert "volatility_threshold" in conditions
    assert "high_impact_multiplier" in conditions
    assert "low_confidence_penalty" in conditions
    
    # Verify reasonable values
    assert 0.0 <= conditions["volatility_threshold"] <= 1.0
    assert conditions["high_impact_multiplier"] >= 1.0
    assert 0.0 <= conditions["low_confidence_penalty"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

