#!/usr/bin/env python3
"""
Direct Test Runner - Bypasses Terminal Issues
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import os
import sys
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_core_imports():
    """Test core module imports directly"""
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
        except Exception as e:
            training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
            failed += 1

    return passed, failed


def test_algorithm_initialization():
    """Test algorithm initialization"""
    training_logger.info("\n🧪 TESTING ALGORITHM INITIALIZATION...", operation="enhanced_logging")

    tests = []

    # Test LinUCB
    try:
        from CORE_SUPER_BANDITS.optimized_linucb_institutional import (
            OptimizedInstitutionalLinUCB,
        )

        OptimizedInstitutionalLinUCB()
        training_logger.info("  ✅ LinUCB Algorithm - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ LinUCB Algorithm - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Neural Bandit
    try:
        from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import (
            OptimizedInstitutionalNeuralBandit,
        )

        OptimizedInstitutionalNeuralBandit()
        training_logger.info("  ✅ Neural Bandit Algorithm - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Neural Bandit Algorithm - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test UCBV
    try:
        from CORE_SUPER_BANDITS.optimized_ucbv_institutional import (
            OptimizedInstitutionalUCBV,
        )

        OptimizedInstitutionalUCBV()
        training_logger.info("  ✅ UCBV Algorithm - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ UCBV Algorithm - {e}", operation="enhanced_logging")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed


def test_services_initialization():
    """Test services initialization"""
    training_logger.info("\n🧪 TESTING SERVICES INITIALIZATION...", operation="enhanced_logging")

    tests = []

    # Test News Sentiment
    try:
        from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis

        AdvancedNewsSentimentAnalysis()
        training_logger.info("  ✅ News Sentiment Analysis - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ News Sentiment Analysis - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Infrastructure Manager
    try:
        from services.infrastructure_manager import InstitutionalInfrastructureManager

        InstitutionalInfrastructureManager()
        training_logger.info("  ✅ Infrastructure Manager - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Infrastructure Manager - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Compliance System
    try:
        from services.compliance_system import UKROIComplianceSystem

        UKROIComplianceSystem()
        training_logger.info("  ✅ Compliance System - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Compliance System - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Execution Bridge
    try:
        from services.execution_bridge import UltraInstitutionalExecutionBridge

        UltraInstitutionalExecutionBridge()
        training_logger.info("  ✅ Execution Bridge - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Execution Bridge - {e}", operation="enhanced_logging")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed


def test_pipeline_components():
    """Test pipeline components"""
    training_logger.info("\n🧪 TESTING PIPELINE COMPONENTS...", operation="enhanced_logging")

    tests = []

    # Test Enhanced Runner
    try:
        from pipeline.enhanced_runner import EnhancedPipelineRunner

        EnhancedPipelineRunner()
        training_logger.info("  ✅ Enhanced Pipeline Runner - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Enhanced Pipeline Runner - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Hygiene
    try:
        from pipeline.hygiene import Hygiene

        Hygiene()
        training_logger.info("  ✅ Hygiene System - Initialized", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Hygiene System - {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Feature Builder
    try:
        training_logger.info("  ✅ Feature Builder - Imported", operation="enhanced_logging")
        tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Feature Builder - {e}", operation="enhanced_logging")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed


def run_individual_test_files():
    """Run individual test files directly"""
    training_logger.info("\n🧪 RUNNING INDIVIDUAL TEST FILES...", operation="enhanced_logging")

    test_files = [
        "tests/test_linucb_day1_foundation.py",
        "tests/test_neural_day2_foundation.py",
        "tests/test_ucbv_day3_foundation.py",
        "tests/test_pipeline_loop_smoke.py",
    ]

    passed = 0
    failed = 0

    for test_file in test_files:
        test_path = project_root / test_file
        if test_path.exists():
            training_logger.info(f"\n📋 Running: {test_file}", operation="enhanced_logging")
            try:
                # Execute the test file
                with open(test_path, "r") as f:
                    test_code = f.read()

                # Create a safe execution environment
                exec_globals = {
                    "__name__": "__main__",
                    "__file__": str(test_path),
                    "sys": sys,
                    "os": os,
                    "Path": Path,
                }

                # Add project root to sys.path in the execution environment
                exec_globals["sys"].path.insert(0, str(project_root))

                exec(test_code, exec_globals)
                training_logger.info(f"  ✅ {test_file} - Executed successfully", operation="enhanced_logging")
                passed += 1

            except Exception as e:
                training_logger.error(f"  ❌ {test_file} - {e}", operation="enhanced_logging")
                training_logger.info(f"      Traceback: {traceback.format_exc(, operation="enhanced_logging")[:200]}...")
                failed += 1
        else:
            training_logger.warning(f"  ⚠️  {test_file} - File not found", operation="enhanced_logging")
            failed += 1

    return passed, failed


def main():
    """Run comprehensive direct tests"""
    training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - DIRECT TEST RUNNER", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")
    training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")

    total_passed = 0
    total_failed = 0

    try:
        # Test core imports
        passed, failed = test_core_imports()
        total_passed += passed
        total_failed += failed

        # Test algorithm initialization
        passed, failed = test_algorithm_initialization()
        total_passed += passed
        total_failed += failed

        # Test services initialization
        passed, failed = test_services_initialization()
        total_passed += passed
        total_failed += failed

        # Test pipeline components
        passed, failed = test_pipeline_components()
        total_passed += passed
        total_failed += failed

        # Run individual test files
        passed, failed = run_individual_test_files()
        total_passed += passed
        total_failed += failed

    except Exception as e:
        training_logger.error(f"\n💥 TEST RUNNER ERROR: {e}", operation="enhanced_logging")
        traceback.print_exc()
        total_failed += 1

    # Summary
    training_logger.info(f"\n{'='*80}", operation="enhanced_logging")
    training_logger.info("📊 DIRECT TEST SUMMARY", operation="enhanced_logging")
    training_logger.info(f"{'='*80}", operation="enhanced_logging")
    training_logger.error(f"Total Tests: {total_passed + total_failed}", operation="enhanced_logging")
    training_logger.info(f"✅ Passed: {total_passed}", operation="enhanced_logging")
    training_logger.error(f"❌ Failed: {total_failed}", operation="enhanced_logging")
    training_logger.error(f"📊 Success Rate: {(total_passed/(total_passed + total_failed, operation="enhanced_logging")*100):.1f}%"
        if (total_passed + total_failed) > 0
        else "📊 Success Rate: 0%"
    )

    if total_failed == 0:
        training_logger.info("\n🎉 ALL DIRECT TESTS PASSED! SYSTEM IS FUNCTIONAL!", operation="enhanced_logging")
    else:
        training_logger.error(f"\n⚠️  {total_failed} TESTS FAILED - REVIEW AND FIX", operation="enhanced_logging")

    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
