#!/usr/bin/env python3
"""
Diagnose the critical issues in the system
"""

import sys
sys.path.append('.')

from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis
from services.feature_builder import build_enriched_from_aggs
from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB

def diagnose_news_sentiment():
    """Diagnose news sentiment issues"""
    print("🔍 DIAGNOSING NEWS SENTIMENT ISSUES")
    print("=" * 50)
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    # Test with real symbol
    print("Testing news sentiment with AAPL...")
    result = analyzer.analyze_symbol_sentiment('AAPL', lookback_hours=24)
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    print(f"Has sentiment_score: {hasattr(result, 'sentiment_score')}")
    print(f"Has confidence: {hasattr(result, 'confidence')}")
    
    if hasattr(result, 'sentiment_score'):
        print(f"Sentiment Score: {result.sentiment_score}")
        print(f"Confidence: {result.confidence}")
    else:
        print("❌ Result object missing required attributes!")

def diagnose_algorithm_issues():
    """Diagnose algorithm processing issues"""
    print("\n🔍 DIAGNOSING ALGORITHM PROCESSING ISSUES")
    print("=" * 50)
    
    # Test feature builder
    print("Testing feature builder...")
    # nocontam: allow diagnostic example for structure explanation (no execution path relies on it)
    example_aggs = {
        "results": [
            {
                "p": 150.0,
                "s": 1000000,
                "t": 1640995200000,
                "c": [1],
                "o": 145.0,
                "h": 155.0,
                "l": 140.0,
                "v": 1000000,
                "vw": 150.0
            }
        ]
    }
    
    try:
        enriched = build_enriched_from_aggs(example_aggs)
        print(f"Enriched type: {type(enriched)}")
        print(f"Enriched: {enriched}")
        print(f"Has market_data: {hasattr(enriched, 'market_data')}")
        
        if hasattr(enriched, 'market_data'):
            print(f"Market data: {enriched.market_data}")
            print(f"Price: {getattr(enriched.market_data, 'price', 'NO PRICE')}")
    except Exception as e:
        print(f"❌ Feature builder failed: {e}")
        return
    
    # Test LinUCB algorithm
    print("\nTesting LinUCB algorithm...")
    try:
        algorithm = OptimizedInstitutionalLinUCB()
        print(f"Algorithm type: {type(algorithm)}")
        
        # Test arm selection
        arm = algorithm.select_arm(enriched)
        print(f"Selected arm: {arm}")
        print(f"Arm type: {type(arm)}")
        
        # Test confidence calculation
        confidence = algorithm.get_confidence_for_context(arm, enriched)
        print(f"Confidence: {confidence}")
        print(f"Confidence type: {type(confidence)}")
        
    except Exception as e:
        print(f"❌ LinUCB algorithm failed: {e}")

def diagnose_news_sources():
    """Diagnose news source issues"""
    print("\n🔍 DIAGNOSING NEWS SOURCE ISSUES")
    print("=" * 50)
    
    analyzer = AdvancedNewsSentimentAnalysis()
    
    print("Testing individual news sources...")
    for source_name, source in analyzer.news_sources.items():
        print(f"\nTesting {source_name}:")
        print(f"  URL: {source.url}")
        print(f"  Weight: {source.weight}")
        print(f"  Reliability: {source.reliability}")
        
        # Test if source has API key
        if hasattr(source, 'api_key'):
            print(f"  API Key: {'SET' if source.api_key else 'NOT SET'}")
        else:
            print(f"  API Key: NOT FOUND")

def main():
    """Main diagnosis function"""
    print("🚨 DIAGNOSING CRITICAL SYSTEM ISSUES")
    print("=" * 60)
    
    diagnose_news_sentiment()
    diagnose_algorithm_issues()
    diagnose_news_sources()
    
    print("\n✅ Diagnosis completed")

if __name__ == "__main__":
    main()
