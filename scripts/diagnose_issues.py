#!/usr/bin/env python3
"""
Diagnose the critical issues in the system
"""

import sys

sys.path.append(".")

from CORE_SUPER_BANDITS.optimized_linucb_institutional import (
    OptimizedInstitutionalLinUCB,
)
from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis
from services.feature_builder import build_enriched_from_aggs


def diagnose_news_sentiment():
    """Diagnose news sentiment issues"""
    training_logger.info("🔍 DIAGNOSING NEWS SENTIMENT ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    analyzer = AdvancedNewsSentimentAnalysis()

    # Test with real symbol
    training_logger.info("Testing news sentiment with AAPL...", operation="enhanced_logging")
    result = analyzer.analyze_symbol_sentiment("AAPL", lookback_hours=24)

    training_logger.info(f"Result type: {type(result, operation="enhanced_logging")}")
    training_logger.info(f"Result: {result}", operation="enhanced_logging")
    training_logger.info(f"Has sentiment_score: {hasattr(result, 'sentiment_score', operation="enhanced_logging")}")
    training_logger.info(f"Has confidence: {hasattr(result, 'confidence', operation="enhanced_logging")}")

    if hasattr(result, "sentiment_score"):
        training_logger.info(f"Sentiment Score: {result.sentiment_score}", operation="enhanced_logging")
        training_logger.info(f"Confidence: {result.confidence}", operation="enhanced_logging")
    else:
        training_logger.error("❌ Result object missing required attributes!", operation="enhanced_logging")


def diagnose_algorithm_issues():
    """Diagnose algorithm processing issues"""
    training_logger.info("\n🔍 DIAGNOSING ALGORITHM PROCESSING ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    # Test feature builder
    training_logger.info("Testing feature builder...", operation="enhanced_logging")
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
                "vw": 150.0,
            }
        ]
    }

    try:
        enriched = build_enriched_from_aggs(example_aggs)
        training_logger.info(f"Enriched type: {type(enriched, operation="enhanced_logging")}")
        training_logger.info(f"Enriched: {enriched}", operation="enhanced_logging")
        training_logger.info(f"Has market_data: {hasattr(enriched, 'market_data', operation="enhanced_logging")}")

        if hasattr(enriched, "market_data"):
            training_logger.info(f"Market data: {enriched.market_data}", operation="enhanced_logging")
            training_logger.info(f"Price: {getattr(enriched.market_data, 'price', 'NO PRICE', operation="enhanced_logging")}")
    except Exception as e:
        training_logger.error(f"❌ Feature builder failed: {e}", operation="enhanced_logging")
        return

    # Test LinUCB algorithm
    training_logger.info("\nTesting LinUCB algorithm...", operation="enhanced_logging")
    try:
        algorithm = OptimizedInstitutionalLinUCB()
        training_logger.info(f"Algorithm type: {type(algorithm, operation="enhanced_logging")}")

        # Test arm selection
        arm = algorithm.select_arm(enriched)
        training_logger.info(f"Selected arm: {arm}", operation="enhanced_logging")
        training_logger.info(f"Arm type: {type(arm, operation="enhanced_logging")}")

        # Test confidence calculation
        confidence = algorithm.get_confidence_for_context(arm, enriched)
        training_logger.info(f"Confidence: {confidence}", operation="enhanced_logging")
        training_logger.info(f"Confidence type: {type(confidence, operation="enhanced_logging")}")

    except Exception as e:
        training_logger.error(f"❌ LinUCB algorithm failed: {e}", operation="enhanced_logging")


def diagnose_news_sources():
    """Diagnose news source issues"""
    training_logger.info("\n🔍 DIAGNOSING NEWS SOURCE ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    analyzer = AdvancedNewsSentimentAnalysis()

    training_logger.info("Testing individual news sources...", operation="enhanced_logging")
    for source_name, source in analyzer.news_sources.items():
        training_logger.info(f"\nTesting {source_name}:", operation="enhanced_logging")
        training_logger.info(f"  URL: {source.url}", operation="enhanced_logging")
        training_logger.info(f"  Weight: {source.weight}", operation="enhanced_logging")
        training_logger.info(f"  Reliability: {source.reliability}", operation="enhanced_logging")

        # Test if source has API key
        if hasattr(source, "api_key"):
            training_logger.info(f"  API Key: {'SET' if source.api_key else 'NOT SET'}", operation="enhanced_logging")
        else:
            training_logger.info("  API Key: NOT FOUND", operation="enhanced_logging")


def main():
    """Main diagnosis function"""
    training_logger.error("🚨 DIAGNOSING CRITICAL SYSTEM ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    diagnose_news_sentiment()
    diagnose_algorithm_issues()
    diagnose_news_sources()

    training_logger.info("\n✅ Diagnosis completed", operation="enhanced_logging")


if __name__ == "__main__":
    main()
