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
    print("🧪 TESTING CORE IMPORTS...")

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
            print(f"  ✅ {description}")
            passed += 1
        except ImportError as e:
            print(f"  ❌ {description} - {e}")
            failed += 1
        except Exception as e:
            print(f"  ⚠️  {description} - {e}")
            failed += 1

    print(f"\n📊 Import Test Results: {passed} passed, {failed} failed")
    return passed, failed


def test_core_functionality():
    """Test core functionality without external dependencies"""
    print("\n🧪 TESTING CORE FUNCTIONALITY...")

    tests = []

    # Test LinUCB Algorithm
    try:
        from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedLinUCB

        bandit = OptimizedLinUCB(n_arms=3, alpha=1.0)
        assert bandit.n_arms == 3
        print("  ✅ LinUCB Algorithm - Basic initialization")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ LinUCB Algorithm - {e}")
        tests.append(False)

    # Test News Sentiment
    try:
        from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis

        AdvancedNewsSentimentAnalysis()
        print("  ✅ News Sentiment Analysis - Initialization")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ News Sentiment Analysis - {e}")
        tests.append(False)

    # Test Infrastructure Manager
    try:
        from services.infrastructure_manager import InstitutionalInfrastructureManager

        InstitutionalInfrastructureManager()
        print("  ✅ Infrastructure Manager - Initialization")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Infrastructure Manager - {e}")
        tests.append(False)

    # Test Compliance System
    try:
        from services.compliance_system import UKROIComplianceSystem

        UKROIComplianceSystem()
        print("  ✅ Compliance System - Initialization")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Compliance System - {e}")
        tests.append(False)

    # Test Feature Builder
    try:
        from services.feature_builder import FeatureBuilder

        FeatureBuilder()
        print("  ✅ Feature Builder - Initialization")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Feature Builder - {e}")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed

    print(f"\n📊 Functionality Test Results: {passed} passed, {failed} failed")
    return passed, failed


def main():
    """Run quick tests"""
    print("🚀 INSTITUTIONAL AI TRADING SYSTEM - QUICK TEST RUNNER")
    print("=" * 60)
    print("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER")
    print("=" * 60)

    # Run import tests
    import_passed, import_failed = test_imports()

    # Run functionality tests
    func_passed, func_failed = test_core_functionality()

    # Summary
    total_passed = import_passed + func_passed
    total_failed = import_failed + func_failed

    print(f"\n{'='*60}")
    print("📊 QUICK TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(
        f"📊 Success Rate: {(total_passed/(total_passed + total_failed)*100):.1f}%"
        if (total_passed + total_failed) > 0
        else "📊 Success Rate: 0%"
    )

    if total_failed == 0:
        print("\n🎉 ALL QUICK TESTS PASSED! CORE SYSTEM IS FUNCTIONAL!")
    else:
        print(f"\n⚠️  {total_failed} TESTS FAILED - REVIEW CORE FUNCTIONALITY")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
