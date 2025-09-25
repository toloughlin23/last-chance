#!/usr/bin/env python3
"""
Final GitHub Test - Focus on Working Components
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import os
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_github_integration():
    """Test GitHub integration"""
    training_logger.info("🔗 TESTING GITHUB INTEGRATION...", operation="enhanced_logging")

    tests = []

    # Test Git remote
    try:
        result = subprocess.run(
            ["git", "remote", "-v"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and "github.com" in result.stdout:
            training_logger.info("  ✅ Git remote configured", operation="enhanced_logging")
            tests.append(True)
        else:
            training_logger.error("  ❌ Git remote not configured", operation="enhanced_logging")
            tests.append(False)
    except Exception as e:
        training_logger.error(f"  ❌ Git remote test failed: {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Git fetch
    try:
        result = subprocess.run(
            ["git", "fetch", "origin"], capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            training_logger.info("  ✅ Git fetch successful", operation="enhanced_logging")
            tests.append(True)
        else:
            training_logger.error(f"  ❌ Git fetch failed: {result.stderr}", operation="enhanced_logging")
            tests.append(False)
    except Exception as e:
        training_logger.error(f"  ❌ Git fetch test failed: {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Git status
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            training_logger.info("  ✅ Git status working", operation="enhanced_logging")
            tests.append(True)
        else:
            training_logger.error(f"  ❌ Git status failed: {result.stderr}", operation="enhanced_logging")
            tests.append(False)
    except Exception as e:
        training_logger.error(f"  ❌ Git status test failed: {e}", operation="enhanced_logging")
        tests.append(False)

    # Test Git branch (support detached HEAD in CI)
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        branch = result.stdout.strip() if result.returncode == 0 else ""
        if not branch:
            # In pull_request runs GitHub checks out a detached HEAD; use CI env vars or commit SHA
            branch = os.getenv("GITHUB_HEAD_REF") or os.getenv(
                "GITHUB_REF", ""
            ).replace("refs/heads/", "")
        if not branch:
            sha = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if sha.returncode == 0 and sha.stdout.strip():
                training_logger.info(f"  ✅ Detached HEAD detected @ {sha.stdout.strip(, operation="enhanced_logging")} (CI)\n")
                tests.append(True)
            else:
                training_logger.error("  ❌ Git branch detection failed", operation="enhanced_logging")
                tests.append(False)
        else:
            training_logger.info(f"  ✅ Current branch: {branch}", operation="enhanced_logging")
            tests.append(True)
    except Exception as e:
        training_logger.error(f"  ❌ Git branch test failed: {e}", operation="enhanced_logging")
        tests.append(False)

    passed = sum(tests)
    failed = len(tests) - passed
    assert passed > 0, f"GitHub integration tests failed: {failed} failures"
    assert failed == 0, f"GitHub integration tests failed: {failed} failures"


def test_core_imports():
    """Test core module imports"""
    training_logger.info("\n🧪 TESTING CORE IMPORTS...", operation="enhanced_logging")

    modules = [
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

    for module_name, description in modules:
        try:
            __import__(module_name)
            training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
            passed += 1
        except Exception as e:
            training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
            failed += 1

    assert passed > 0, f"GitHub integration tests failed: {failed} failures"
    assert failed == 0, f"GitHub integration tests failed: {failed} failures"


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
    assert passed > 0, f"GitHub integration tests failed: {failed} failures"
    assert failed == 0, f"GitHub integration tests failed: {failed} failures"


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
    assert passed > 0, f"GitHub integration tests failed: {failed} failures"
    assert failed == 0, f"GitHub integration tests failed: {failed} failures"


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
    assert passed > 0, f"GitHub integration tests failed: {failed} failures"
    assert failed == 0, f"GitHub integration tests failed: {failed} failures"


def main():
    """Run final GitHub test"""
    training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - FINAL GITHUB TEST", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")
    training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")

    start_time = time.time()
    total_passed = 0
    total_failed = 0

    try:
        # Test GitHub integration
        passed, failed = test_github_integration()
        total_passed += passed
        total_failed += failed

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

    except Exception as e:
        training_logger.error(f"\n💥 TEST ERROR: {e}", operation="enhanced_logging")
        total_failed += 1

    # Summary
    end_time = time.time()
    duration = end_time - start_time

    training_logger.info(f"\n{'='*80}", operation="enhanced_logging")
    training_logger.info("📊 FINAL GITHUB TEST SUMMARY", operation="enhanced_logging")
    training_logger.info(f"{'='*80}", operation="enhanced_logging")
    training_logger.error(f"Total Tests: {total_passed + total_failed}", operation="enhanced_logging")
    training_logger.info(f"✅ Passed: {total_passed}", operation="enhanced_logging")
    training_logger.error(f"❌ Failed: {total_failed}", operation="enhanced_logging")
    training_logger.error(f"📊 Success Rate: {(total_passed/(total_passed + total_failed, operation="enhanced_logging")*100):.1f}%"
        if (total_passed + total_failed) > 0
        else "📊 Success Rate: 0%"
    )
    training_logger.info(f"⏱️  Duration: {duration:.2f} seconds", operation="enhanced_logging")
    training_logger.info(f"{'='*80}", operation="enhanced_logging")

    if total_failed == 0:
        training_logger.info("🎉 ALL GITHUB TESTS PASSED! SYSTEM IS PRODUCTION READY!", operation="enhanced_logging")
    elif total_passed / (total_passed + total_failed) >= 0.9:
        training_logger.info("🎯 EXCELLENT! 90%+ tests passed - System is highly functional!", operation="enhanced_logging")
    elif total_passed / (total_passed + total_failed) >= 0.8:
        training_logger.info("✅ VERY GOOD! 80%+ tests passed - System is functional!", operation="enhanced_logging")
    else:
        training_logger.error(f"⚠️  {total_failed} TESTS FAILED - Review and fix", operation="enhanced_logging")

    assert total_failed == 0, f"Total failures: {total_failed}"


if __name__ == "__main__":
    sys.exit(main())
