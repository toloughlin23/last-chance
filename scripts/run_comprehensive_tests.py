#!/usr/bin/env python3
"""
Comprehensive Test Runner for Institutional AI Trading System
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import sys
import os
import subprocess
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
        print(f"\n{'='*60}")
        print(f"🧪 RUNNING {category_name.upper()} TESTS")
        print(f"{'='*60}")
        
        results = {}
        for test_file in test_files:
            test_path = self.test_dir / test_file
            if test_path.exists():
                print(f"\n📋 Testing: {test_file}")
                try:
                    # Run individual test file
                    result = subprocess.run([
                        sys.executable, "-m", "pytest", 
                        str(test_path), 
                        "-v", 
                        "--tb=short",
                        "--no-header"
                    ], capture_output=True, text=True, timeout=60)
                    
                    results[test_file] = {
                        'returncode': result.returncode,
                        'stdout': result.stdout,
                        'stderr': result.stderr,
                        'success': result.returncode == 0
                    }
                    
                    if result.returncode == 0:
                        print(f"✅ {test_file} - PASSED")
                    else:
                        print(f"❌ {test_file} - FAILED")
                        print(f"Error: {result.stderr[:200]}...")
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ {test_file} - TIMEOUT")
                    results[test_file] = {'success': False, 'error': 'Timeout'}
                except Exception as e:
                    print(f"💥 {test_file} - ERROR: {e}")
                    results[test_file] = {'success': False, 'error': str(e)}
            else:
                print(f"⚠️  {test_file} - NOT FOUND")
                results[test_file] = {'success': False, 'error': 'File not found'}
        
        return results
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 INSTITUTIONAL AI TRADING SYSTEM - COMPREHENSIVE TEST SUITE")
        print("=" * 80)
        print("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER")
        print("=" * 80)
        
        # Test Categories
        test_categories = {
            "CORE ALGORITHMS": [
                "test_linucb_day1_foundation.py",
                "test_neural_day2_foundation.py", 
                "test_ucbv_day3_foundation.py",
                "test_day7_single_bandit_diversity.py"
            ],
            "INFRASTRUCTURE": [
                "test_enhanced_infrastructure_integration.py",
                "test_redis_institutional.py"
            ],
            "DATA SERVICES": [
                "test_alpaca_client_integration.py",
                "test_polygon_client_integration.py",
                "test_polygon_integration.py",
                "test_quotes_client_integration.py",
                "test_news_client_integration.py",
                "test_sentiment_unit.py",
                "test_advanced_news_sentiment_integration.py"
            ],
            "COMPLIANCE & EXECUTION": [
                "test_compliance.py",
                "test_compliance_fixed.py",
                "test_compliance_final.py",
                "test_execution_bridge.py"
            ],
            "PIPELINE INTEGRATION": [
                "test_pipeline_loop_smoke.py",
                "test_pipeline_runner_integration.py",
                "test_pipeline_runner_min_integration.py",
                "test_pipeline_integration.py",
                "test_enhanced_pipeline_verification.py",
                "test_complete_pipeline_verification.py",
                "test_fixed_pipeline.py"
            ],
            "SYSTEM INTEGRATION": [
                "test_hygiene_integrations.py",
                "test_universe_selector_integration.py",
                "test_day4_personality_integration.py"
            ]
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
        
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print(f"{'='*80}")
        
        total_tests = 0
        passed_tests = 0
        failed_tests = 0
        
        for category, results in self.results.items():
            print(f"\n📁 {category}:")
            for test_file, result in results.items():
                total_tests += 1
                if result.get('success', False):
                    passed_tests += 1
                    print(f"  ✅ {test_file}")
                else:
                    failed_tests += 1
                    print(f"  ❌ {test_file}")
                    if 'error' in result:
                        print(f"      Error: {result['error']}")
        
        print(f"\n{'='*60}")
        print(f"📈 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📊 Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "   📊 Success Rate: 0%")
        print(f"   ⏱️  Duration: {duration:.2f} seconds")
        print(f"{'='*60}")
        
        if failed_tests == 0:
            print("🎉 ALL TESTS PASSED! SYSTEM IS READY FOR PRODUCTION!")
        else:
            print(f"⚠️  {failed_tests} TESTS FAILED - REVIEW AND FIX BEFORE PRODUCTION")
        
        return passed_tests, failed_tests

def main():
    """Main test runner"""
    runner = InstitutionalTestRunner()
    
    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test run interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Test runner error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
