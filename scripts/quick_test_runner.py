#!/usr/bin/env python3
"""
Quick Test Runner for Institutional AI Trading System
Tests core functionality without full pytest suite
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all core modules can be imported"""
    training_logger.info("🧪 TESTING CORE IMPORTS...", operation="enhanced_logging")

    tests = [
        ("CORE_SUPER_BANDITS.optimized_linucb_institutional", "LinUCB Algorithm"),
        (
            "CORE_SUPER_BANDITS.optimized_neural_bandit_institutional",
            "Neural Bandit Algorithm",
        ),
        ("CORE_SUPER_BANDITS.optimized_ucbv_institutional", "UCBV Algorithm"),
        ("services.advanced_news_sentiment", "Advanced News Sentiment"),
        ("services.infrastructure_manager", "Infrastructure Manager"),
        ("services.compliance_system", "Compliance System"),
        ("services.execution_bridge", "Execution Bridge"),
        ("services.alpaca_client", "Alpaca Client"),
        ("services.polygon_client", "Polygon Client"),
        ("services.feature_builder", "Feature Builder"),
        ("pipeline.enhanced_runner", "Enhanced Pipeline Runner"),
        ("pipeline.hygiene", "Hygiene System"),
        ("utils.universe_selector", "Universe Selector"),
        ("utils.sp500_cache", "S&P 500 Cache"),
        ("utils.symbols_validator", "Symbols Validator"),
    ]

    passed = 0
    failed = 0

    for module_name, description in tests:
        try:
            __import__(module_name)
            training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
            passed += 1
        except ImportError as e:
            training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
            failed += 1
        except Exception as e:
            training_logger.warning(f"  ⚠️  {description} - {e}", operation="enhanced_logging")
            failed += 1

    training_logger.error(f"\n📊 Import Test Results: {passed} passed, {failed} failed", operation="enhanced_logging")
    return passed, failed


def test_core_functionality():
    """Test core functionality without external dependencies"""
    training_logger.info("\n🧪 TESTING CORE FUNCTIONALITY...", operation="enhanced_logging")

    tests = []

    # Test LinUCB Algorithm
    try:
        from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedLinUCB

        bandit = OptimizedLinUCB(n_arms=3, alpha=1.0)
        assert bandit.n_arms == 3
        training_logger.info("  ✅ LinUCB Algorithm - Basic initialization", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ LinUCB Algorithm - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test News Sentiment
    try:
        from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis

        AdvancedNewsSentimentAnalysis()
        training_logger.info("  ✅ News Sentiment Analysis - Initialization", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ News Sentiment Analysis - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Infrastructure Manager
    try:
        from services.infrastructure_manager import InstitutionalInfrastructureManager

        InstitutionalInfrastructureManager()
        training_logger.info("  ✅ Infrastructure Manager - Initialization", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Infrastructure Manager - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Compliance System
    try:
        from services.compliance_system import UKROIComplianceSystem

        UKROIComplianceSystem()
        training_logger.info("  ✅ Compliance System - Initialization", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Compliance System - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Feature Builder
    try:
        from services.feature_builder import FeatureBuilder

        FeatureBuilder()
        training_logger.info("  ✅ Feature Builder - Initialization", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Feature Builder - {e}", operation="enhanced_logging")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed

    training_logger.error(f"\n📊 Functionality Test Results: {passed} passed, {failed} failed", operation="enhanced_logging")
    return passed, failed


def main():
    """Run quick tests"""
    training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - QUICK TEST RUNNER", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")
    training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Run import tests
    import_passed, import_failed = test_imports()

    # Run functionality tests
    func_passed, func_failed = test_core_functionality()

    # Summary
    total_passed = import_passed + func_passed
    total_failed = import_failed + func_failed

    training_logger.info(f"\n{'='*60}", operation="enhanced_logging")
    training_logger.info("📊 QUICK TEST SUMMARY", operation="enhanced_logging")
    training_logger.info(f"{'='*60}", operation="enhanced_logging")
    training_logger.error(f"Total Tests: {total_passed + total_failed}", operation="enhanced_logging")
    training_logger.info(f"✅ Passed: {total_passed}", operation="enhanced_logging")
    training_logger.error(f"❌ Failed: {total_failed}", operation="enhanced_logging")
    training_logger.error(f"📊 Success Rate: {(total_passed/(total_passed + total_failed, operation="enhanced_logging")*100):.1f}%"
        if (total_passed + total_failed) > 0
        else "📊 Success Rate: 0%"
    )

    if total_failed == 0:
        training_logger.info("\n🎉 ALL QUICK TESTS PASSED! CORE SYSTEM IS FUNCTIONAL!", operation="enhanced_logging")
    else:
        training_logger.error(f"\n⚠️  {total_failed} TESTS FAILED - REVIEW CORE FUNCTIONALITY", operation="enhanced_logging")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
