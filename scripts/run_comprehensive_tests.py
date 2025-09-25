#!/usr/bin/env python3
"""
Comprehensive Test Runner for Institutional AI Trading System
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class InstitutionalTestRunner:
    def __init__(self):
        self.project_root = project_root
        self.test_dir = project_root / "tests"
        self.results = {}
        self.start_time = time.time()

    def run_test_category(self, category_name, test_files):
        """Run a specific category of tests"""
        training_logger.info(f"\n{'='*60}", operation="enhanced_logging")
        training_logger.info(f"🧪 RUNNING {category_name.upper(, operation="enhanced_logging")} TESTS")
        training_logger.info(f"{'='*60}", operation="enhanced_logging")

        results = {}
        for test_file in test_files:
            test_path = self.test_dir / test_file
            if test_path.exists():
                training_logger.info(f"\n📋 Testing: {test_file}", operation="enhanced_logging")
                try:
                    # Run individual test file
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "pytest",
                            str(test_path),
                            "-v",
                            "--tb=short",
                            "--no-header",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )

                    results[test_file] = {
                        "returncode": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "success": result.returncode == 0,
                    }

                    if result.returncode == 0:
                        training_logger.info(f"✅ {test_file} - PASSED", operation="enhanced_logging")
                    else:
                        training_logger.error(f"❌ {test_file} - FAILED", operation="enhanced_logging")
                        training_logger.error(f"Error: {result.stderr[:200]}...", operation="enhanced_logging")

                except subprocess.TimeoutExpired:
                    training_logger.info(f"⏰ {test_file} - TIMEOUT", operation="enhanced_logging")
                    results[test_file] = {"success": False, "error": "Timeout"}
                except Exception as e:
                    training_logger.error(f"💥 {test_file} - ERROR: {e}", operation="enhanced_logging")
                    results[test_file] = {"success": False, "error": str(e)}
            else:
                training_logger.warning(f"⚠️  {test_file} - NOT FOUND", operation="enhanced_logging")
                results[test_file] = {"success": False, "error": "File not found"}

        return results

    def run_all_tests(self):
        """Run comprehensive test suite"""
        training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - COMPREHENSIVE TEST SUITE", operation="enhanced_logging")
        training_logger.info("=" * 80, operation="enhanced_logging")
        training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
        training_logger.info("=" * 80, operation="enhanced_logging")

        # Test Categories
        test_categories = {
            "CORE ALGORITHMS": [
                "test_linucb_day1_foundation.py",
                "test_neural_day2_foundation.py",
                "test_ucbv_day3_foundation.py",
                "test_day7_single_bandit_diversity.py",
            ],
            "INFRASTRUCTURE": [
                "test_enhanced_infrastructure_integration.py",
                "test_redis_institutional.py",
            ],
            "DATA SERVICES": [
                "test_alpaca_client_integration.py",
                "test_polygon_client_integration.py",
                "test_polygon_integration.py",
                "test_quotes_client_integration.py",
                "test_news_client_integration.py",
                "test_sentiment_unit.py",
                "test_advanced_news_sentiment_integration.py",
            ],
            "COMPLIANCE & EXECUTION": [
                "test_compliance.py",
                "test_compliance_fixed.py",
                "test_compliance_final.py",
                "test_execution_bridge.py",
            ],
            "PIPELINE INTEGRATION": [
                "test_pipeline_loop_smoke.py",
                "test_pipeline_runner_integration.py",
                "test_pipeline_runner_min_integration.py",
                "test_pipeline_integration.py",
                "test_enhanced_pipeline_verification.py",
                "test_complete_pipeline_verification.py",
                "test_fixed_pipeline.py",
            ],
            "SYSTEM INTEGRATION": [
                "test_hygiene_integrations.py",
                "test_universe_selector_integration.py",
                "test_day4_personality_integration.py",
            ],
        }

        # Run each category
        for category, test_files in test_categories.items():
            self.results[category] = self.run_test_category(category, test_files)

        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate comprehensive test summary"""
        end_time = time.time()
        duration = end_time - self.start_time

        training_logger.info(f"\n{'='*80}", operation="enhanced_logging")
        training_logger.info("📊 COMPREHENSIVE TEST SUMMARY", operation="enhanced_logging")
        training_logger.info(f"{'='*80}", operation="enhanced_logging")

        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        for category, results in self.results.items():
            training_logger.info(f"\n📁 {category}:", operation="enhanced_logging")
            for test_file, result in results.items():
                total_tests += 1
                if result.get("success", False):
                    passed_tests += 1
                    training_logger.info(f"  ✅ {test_file}", operation="enhanced_logging")
                else:
                    failed_tests += 1
                    training_logger.error(f"  ❌ {test_file}", operation="enhanced_logging")
                    if "error" in result:
                        training_logger.error(f"      Error: {result['error']}", operation="enhanced_logging")

        training_logger.info(f"\n{'='*60}", operation="enhanced_logging")
        training_logger.info("📈 OVERALL RESULTS:", operation="enhanced_logging")
        training_logger.info(f"   Total Tests: {total_tests}", operation="enhanced_logging")
        training_logger.info(f"   ✅ Passed: {passed_tests}", operation="enhanced_logging")
        training_logger.error(f"   ❌ Failed: {failed_tests}", operation="enhanced_logging")
        training_logger.info(f"   📊 Success Rate: {(passed_tests/total_tests*100, operation="enhanced_logging"):.1f}%"
            if total_tests > 0
            else "   📊 Success Rate: 0%"
        )
        training_logger.info(f"   ⏱️  Duration: {duration:.2f} seconds", operation="enhanced_logging")
        training_logger.info(f"{'='*60}", operation="enhanced_logging")

        if failed_tests == 0:
            training_logger.info("🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!", operation="enhanced_logging")
        else:
            training_logger.error(f"⚠️  {failed_tests} TESTS FAILED - REVIEW AND FIX BEFORE PRODUCTION", operation="enhanced_logging")

        return passed_tests, failed_tests


def main():
    """Main test runner"""
    runner = InstitutionalTestRunner()

    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        training_logger.warning("\n\n⚠️  Test run interrupted by user", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"\n\n💥 Test runner error: {e}", operation="enhanced_logging")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
