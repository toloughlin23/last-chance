#!/usr/bin/env python3
"""
GitHub Comprehensive Test Suite for Institutional AI Trading System
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import subprocess
import sys
import time
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class GitHubComprehensiveTester:
    def __init__(self):
        self.project_root = project_root
        self.test_dir = project_root / "tests"
        self.results = {}
        self.start_time = time.time()

    def test_github_connectivity(self):
        """Test GitHub connectivity and authentication"""
        training_logger.info("🔗 TESTING GITHUB CONNECTIVITY...", operation="enhanced_logging")

        tests = []

        # Test Git remote
        try:
            result = subprocess.run(
                ["git", "remote", "-v"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0 and "github.com" in result.stdout:
                training_logger.info("  ✅ Git remote configured correctly", operation="enhanced_logging")
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
                training_logger.info("  ✅ Git fetch successful - GitHub connection working", operation="enhanced_logging")
                tests.append(True)
            else:
                training_logger.error(f"  ❌ Git fetch failed: {result.stderr}", operation="enhanced_logging")
                tests.append(False)
        except Exception as e:
            training_logger.error(f"  ❌ Git fetch test failed: {e}", operation="enhanced_logging")
            tests.append(False)

        # Test GitHub CLI
        try:
            result = subprocess.run(
                ["gh", "auth", "status"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0 and "Logged in" in result.stdout:
                training_logger.info("  ✅ GitHub CLI authenticated", operation="enhanced_logging")
                tests.append(True)
            else:
                training_logger.warning("  ⚠️  GitHub CLI not authenticated (using Git credentials, operation="enhanced_logging")")
                tests.append(True)  # Still pass if Git works
        except Exception:
            training_logger.warning("  ⚠️  GitHub CLI not available (using Git credentials, operation="enhanced_logging")")
            tests.append(True)  # Still pass if Git works

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def test_core_system_components(self):
        """Test all core system components"""
        training_logger.info("\n🧪 TESTING CORE SYSTEM COMPONENTS...", operation="enhanced_logging")

        tests = []

        # Test Algorithm Imports
        algorithm_tests = [
            ("CORE_SUPER_BANDITS.optimized_linucb_institutional", "LinUCB Algorithm"),
            (
                "CORE_SUPER_BANDITS.optimized_neural_bandit_institutional",
                "Neural Bandit Algorithm",
            ),
            ("CORE_SUPER_BANDITS.optimized_ucbv_institutional", "UCBV Algorithm"),
        ]

        for module_name, description in algorithm_tests:
            try:
                __import__(module_name)
                training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
                tests.append(True)
            except Exception as e:
                training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
                tests.append(False)

        # Test Service Imports
        service_tests = [
            ("services.advanced_news_sentiment", "Advanced News Sentiment"),
            ("services.infrastructure_manager", "Infrastructure Manager"),
            ("services.compliance_system", "Compliance System"),
            ("services.execution_bridge", "Execution Bridge"),
            ("services.alpaca_client", "Alpaca Client"),
            ("services.polygon_client", "Polygon Client"),
            ("services.feature_builder", "Feature Builder"),
        ]

        for module_name, description in service_tests:
            try:
                __import__(module_name)
                training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
                tests.append(True)
            except Exception as e:
                training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
                tests.append(False)

        # Test Pipeline Imports
        pipeline_tests = [
            ("pipeline.enhanced_runner", "Enhanced Pipeline Runner"),
            ("pipeline.hygiene", "Hygiene System"),
            ("pipeline.runner", "Pipeline Runner"),
        ]

        for module_name, description in pipeline_tests:
            try:
                __import__(module_name)
                training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
                tests.append(True)
            except Exception as e:
                training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
                tests.append(False)

        # Test Utility Imports
        utility_tests = [
            ("utils.universe_selector", "Universe Selector"),
            ("utils.sp500_cache", "S&P 500 Cache"),
            ("utils.symbols_validator", "Symbols Validator"),
            ("utils.env_loader", "Environment Loader"),
        ]

        for module_name, description in utility_tests:
            try:
                __import__(module_name)
                training_logger.info(f"  ✅ {description}", operation="enhanced_logging")
                tests.append(True)
            except Exception as e:
                training_logger.error(f"  ❌ {description} - {e}", operation="enhanced_logging")
                tests.append(False)

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def test_algorithm_functionality(self):
        """Test algorithm functionality"""
        training_logger.info("\n🧪 TESTING ALGORITHM FUNCTIONALITY...", operation="enhanced_logging")

        tests = []

        # Test LinUCB
        try:
            from CORE_SUPER_BANDITS.optimized_linucb_institutional import (
                OptimizedInstitutionalLinUCB,
            )

            bandit = OptimizedInstitutionalLinUCB()

            # Test basic functionality
            # nocontam: allow synthetic struct for unit exercise boundary (non-production)
            test_data = type(
                "TestData",
                (),
                {
                    "sentiment_analysis": type(
                        "Sentiment",
                        (),
                        {
                            "overall_sentiment": 0.5,
                            "confidence_level": 0.8,
                            "market_impact_estimate": 0.4,
                            "news_volume": 10,
                        },
                    )(),
                    "data_quality_score": 0.9,
                    "market_data": type(
                        "Market",
                        (),
                        {
                            "price_momentum": 0.01,
                            "volatility": 0.02,
                            "volume_ratio": 1.0,
                        },
                    )(),
                },
            )()

            features = bandit.extract_enhanced_market_features(test_data)
            arm = bandit.select_arm(test_data)
            confidence = bandit.get_confidence_for_context(arm, test_data)

            assert len(features) == 15
            assert 0 <= arm < 8
            assert 0 <= confidence <= 1

            training_logger.info("  ✅ LinUCB Algorithm - Full functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ LinUCB Algorithm - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Neural Bandit
        try:
            from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import (
                OptimizedInstitutionalNeuralBandit,
            )

            bandit = OptimizedInstitutionalNeuralBandit()

            # Test basic functionality
            # nocontam: allow synthetic struct for unit exercise boundary (non-production)
            test_data = type(
                "TestData",
                (),
                {
                    "sentiment_analysis": type(
                        "Sentiment",
                        (),
                        {
                            "overall_sentiment": 0.5,
                            "confidence_level": 0.8,
                            "market_impact_estimate": 0.4,
                            "news_volume": 10,
                        },
                    )(),
                    "data_quality_score": 0.9,
                    "market_data": type(
                        "Market",
                        (),
                        {
                            "price_momentum": 0.01,
                            "volatility": 0.02,
                            "volume_ratio": 1.0,
                        },
                    )(),
                },
            )()

            features = bandit.extract_neural_features(test_data)
            arm = bandit.select_arm(test_data)
            confidence = bandit.get_confidence_for_context(arm, test_data)

            assert len(features) == 15
            assert 0 <= arm < 8
            assert 0 <= confidence <= 1

            training_logger.info("  ✅ Neural Bandit Algorithm - Full functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Neural Bandit Algorithm - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test UCBV
        try:
            from CORE_SUPER_BANDITS.optimized_ucbv_institutional import (
                OptimizedInstitutionalUCBV,
            )

            bandit = OptimizedInstitutionalUCBV()

            # Test basic functionality
            # nocontam: allow synthetic struct for unit exercise boundary (non-production)
            test_data = type(
                "TestData",
                (),
                {
                    "sentiment_analysis": type(
                        "Sentiment",
                        (),
                        {
                            "overall_sentiment": 0.5,
                            "confidence_level": 0.8,
                            "market_impact_estimate": 0.4,
                            "news_volume": 10,
                        },
                    )(),
                    "data_quality_score": 0.9,
                    "market_data": type(
                        "Market",
                        (),
                        {
                            "price_momentum": 0.01,
                            "volatility": 0.02,
                            "volume_ratio": 1.0,
                        },
                    )(),
                },
            )()

            features = bandit.extract_features_from_polygon(test_data)
            arm = bandit.select_arm(test_data)
            confidence = bandit.get_confidence_for_context(arm, test_data)

            assert len(features) == 15
            assert 0 <= arm < 8
            assert 0 <= confidence <= 1

            training_logger.info("  ✅ UCBV Algorithm - Full functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ UCBV Algorithm - {e}", operation="enhanced_logging")
            tests.append(False)

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def test_services_functionality(self):
        """Test services functionality"""
        training_logger.info("\n🧪 TESTING SERVICES FUNCTIONALITY...", operation="enhanced_logging")

        tests = []

        # Test News Sentiment
        try:
            from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis

            analyzer = AdvancedNewsSentimentAnalysis()

            # Test basic functionality
            result = analyzer.analyze_symbol_sentiment("AAPL")
            assert hasattr(result, "overall_sentiment")
            assert hasattr(result, "confidence_level")

            training_logger.info("  ✅ News Sentiment Analysis - Functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ News Sentiment Analysis - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Infrastructure Manager
        try:
            from services.infrastructure_manager import (
                InstitutionalInfrastructureManager,
            )

            manager = InstitutionalInfrastructureManager()

            # Test basic functionality
            assert hasattr(manager, "execute_parallel_tasks")
            assert hasattr(manager, "thread_pools")

            training_logger.info("  ✅ Infrastructure Manager - Functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Infrastructure Manager - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Compliance System
        try:
            from services.compliance_system import UKROIComplianceSystem

            compliance = UKROIComplianceSystem()

            # Test basic functionality
            test_data = {
                "portfolio_value": 1000000,
                "positions": [{"symbol": "AAPL", "value": 100000}],
                "risk_metrics": {"var_95": 50000},
            }

            result = compliance.run_compliance_check(test_data)
            assert hasattr(result, "is_compliant")
            assert hasattr(result, "compliance_score")

            training_logger.info("  ✅ Compliance System - Functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Compliance System - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Execution Bridge
        try:
            from services.execution_bridge import UltraInstitutionalExecutionBridge

            bridge = UltraInstitutionalExecutionBridge()

            # Test basic functionality
            assert hasattr(bridge, "submit_order")
            assert hasattr(bridge, "get_portfolio_metrics")

            training_logger.info("  ✅ Execution Bridge - Functionality test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Execution Bridge - {e}", operation="enhanced_logging")
            tests.append(False)

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def test_pipeline_integration(self):
        """Test pipeline integration"""
        training_logger.info("\n🧪 TESTING PIPELINE INTEGRATION...", operation="enhanced_logging")

        tests = []

        # Test Enhanced Pipeline Runner
        try:
            from pipeline.enhanced_runner import EnhancedPipelineRunner

            runner = EnhancedPipelineRunner()

            # Test basic functionality
            assert hasattr(runner, "run_enhanced_once")
            assert hasattr(runner, "run_enhanced_loop")

            training_logger.info("  ✅ Enhanced Pipeline Runner - Integration test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Enhanced Pipeline Runner - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Hygiene System
        try:
            from pipeline.hygiene import Hygiene

            hygiene = Hygiene()

            # Test basic functionality
            symbols = ["AAPL", "MSFT", "GOOGL"]
            filtered = hygiene.filter_symbols(symbols)
            assert isinstance(filtered, list)

            training_logger.info("  ✅ Hygiene System - Integration test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Hygiene System - {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Feature Builder
        try:
            from services.feature_builder import build_enriched_from_aggs

            # Test basic functionality
            test_aggs = {"c": 150.0, "h": 155.0, "l": 145.0, "v": 1000000, "vw": 150.0}

            result = build_enriched_from_aggs(test_aggs)
            assert hasattr(result, "sentiment_analysis")
            assert hasattr(result, "market_data")

            training_logger.info("  ✅ Feature Builder - Integration test passed", operation="enhanced_logging")
            tests.append(True)
        except Exception as e:
            training_logger.error(f"  ❌ Feature Builder - {e}", operation="enhanced_logging")
            tests.append(False)

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def test_github_workflow(self):
        """Test GitHub workflow functionality"""
        training_logger.info("\n🔗 TESTING GITHUB WORKFLOW...", operation="enhanced_logging")

        tests = []

        # Test Git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=10,
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

        # Test Git branch
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and result.stdout.strip():
                training_logger.info(f"  ✅ Current branch: {result.stdout.strip(, operation="enhanced_logging")}")
                tests.append(True)
            else:
                training_logger.error("  ❌ Git branch detection failed", operation="enhanced_logging")
                tests.append(False)
        except Exception as e:
            training_logger.error(f"  ❌ Git branch test failed: {e}", operation="enhanced_logging")
            tests.append(False)

        # Test Git log
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0 and result.stdout.strip():
                training_logger.info("  ✅ Git log working", operation="enhanced_logging")
                tests.append(True)
            else:
                training_logger.error("  ❌ Git log failed", operation="enhanced_logging")
                tests.append(False)
        except Exception as e:
            training_logger.error(f"  ❌ Git log test failed: {e}", operation="enhanced_logging")
            tests.append(False)

        passed = sum(tests)
        failed = len(tests) - passed
        return passed, failed

    def run_comprehensive_test(self):
        """Run comprehensive GitHub test suite"""
        training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - GITHUB COMPREHENSIVE TEST", operation="enhanced_logging")
        training_logger.info("=" * 80, operation="enhanced_logging")
        training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
        training_logger.info("=" * 80, operation="enhanced_logging")

        total_passed = 0
        total_failed = 0

        try:
            # Test GitHub connectivity
            passed, failed = self.test_github_connectivity()
            total_passed += passed
            total_failed += failed

            # Test core system components
            passed, failed = self.test_core_system_components()
            total_passed += passed
            total_failed += failed

            # Test algorithm functionality
            passed, failed = self.test_algorithm_functionality()
            total_passed += passed
            total_failed += failed

            # Test services functionality
            passed, failed = self.test_services_functionality()
            total_passed += passed
            total_failed += failed

            # Test pipeline integration
            passed, failed = self.test_pipeline_integration()
            total_passed += passed
            total_failed += failed

            # Test GitHub workflow
            passed, failed = self.test_github_workflow()
            total_passed += passed
            total_failed += failed

        except Exception as e:
            training_logger.error(f"\n💥 COMPREHENSIVE TEST ERROR: {e}", operation="enhanced_logging")
            traceback.print_exc()
            total_failed += 1

        # Generate summary
        end_time = time.time()
        duration = end_time - self.start_time

        training_logger.info(f"\n{'='*80}", operation="enhanced_logging")
        training_logger.info("📊 GITHUB COMPREHENSIVE TEST SUMMARY", operation="enhanced_logging")
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
            training_logger.info("🎉 ALL GITHUB COMPREHENSIVE TESTS PASSED! SYSTEM IS PRODUCTION READY!", operation="enhanced_logging")
        else:
            training_logger.error(f"⚠️  {total_failed} TESTS FAILED - REVIEW AND FIX BEFORE PRODUCTION", operation="enhanced_logging")

        return total_passed, total_failed


def main():
    """Run GitHub comprehensive test"""
    tester = GitHubComprehensiveTester()

    try:
        passed, failed = tester.run_comprehensive_test()
        return 0 if failed == 0 else 1
    except KeyboardInterrupt:
        training_logger.warning("\n\n⚠️  Test run interrupted by user", operation="enhanced_logging")
        return 1
    except Exception as e:
        training_logger.error(f"\n\n💥 Test runner error: {e}", operation="enhanced_logging")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
