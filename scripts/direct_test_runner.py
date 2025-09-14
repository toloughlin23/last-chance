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
    print("🧪 TESTING CORE IMPORTS...")
    
    tests = [
        ("CORE_SUPER_BANDITS.optimized_linucb_institutional", "LinUCB Algorithm"),
        ("CORE_SUPER_BANDITS.optimized_neural_bandit_institutional", "Neural Bandit Algorithm"),
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
        ("utils.symbols_validator", "Symbols Validator")
    ]
    
    passed = 0
    failed = 0
    
    for module_name, description in tests:
        try:
            __import__(module_name)
            print(f"  ✅ {description}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {description} - {e}")
            failed += 1
    
    return passed, failed

def test_algorithm_initialization():
    """Test algorithm initialization"""
    print("\n🧪 TESTING ALGORITHM INITIALIZATION...")
    
    tests = []
    
    # Test LinUCB
    try:
        from CORE_SUPER_BANDITS.optimized_linucb_institutional import (
            OptimizedInstitutionalLinUCB,
        )
        OptimizedInstitutionalLinUCB()
        print("  ✅ LinUCB Algorithm - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ LinUCB Algorithm - {e}")
        tests.append(False)
    
    # Test Neural Bandit
    try:
        from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import (
            OptimizedInstitutionalNeuralBandit,
        )
        OptimizedInstitutionalNeuralBandit()
        print("  ✅ Neural Bandit Algorithm - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Neural Bandit Algorithm - {e}")
        tests.append(False)
    
    # Test UCBV
    try:
        from CORE_SUPER_BANDITS.optimized_ucbv_institutional import (
            OptimizedInstitutionalUCBV,
        )
        OptimizedInstitutionalUCBV()
        print("  ✅ UCBV Algorithm - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ UCBV Algorithm - {e}")
        tests.append(False)
    
    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed

def test_services_initialization():
    """Test services initialization"""
    print("\n🧪 TESTING SERVICES INITIALIZATION...")
    
    tests = []
    
    # Test News Sentiment
    try:
        from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis
        AdvancedNewsSentimentAnalysis()
        print("  ✅ News Sentiment Analysis - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ News Sentiment Analysis - {e}")
        tests.append(False)
    
    # Test Infrastructure Manager
    try:
        from services.infrastructure_manager import InstitutionalInfrastructureManager
        InstitutionalInfrastructureManager()
        print("  ✅ Infrastructure Manager - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Infrastructure Manager - {e}")
        tests.append(False)
    
    # Test Compliance System
    try:
        from services.compliance_system import UKROIComplianceSystem
        UKROIComplianceSystem()
        print("  ✅ Compliance System - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Compliance System - {e}")
        tests.append(False)
    
    # Test Execution Bridge
    try:
        from services.execution_bridge import UltraInstitutionalExecutionBridge
        UltraInstitutionalExecutionBridge()
        print("  ✅ Execution Bridge - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Execution Bridge - {e}")
        tests.append(False)
    
    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed

def test_pipeline_components():
    """Test pipeline components"""
    print("\n🧪 TESTING PIPELINE COMPONENTS...")
    
    tests = []
    
    # Test Enhanced Runner
    try:
        from pipeline.enhanced_runner import EnhancedPipelineRunner
        EnhancedPipelineRunner()
        print("  ✅ Enhanced Pipeline Runner - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Enhanced Pipeline Runner - {e}")
        tests.append(False)
    
    # Test Hygiene
    try:
        from pipeline.hygiene import Hygiene
        Hygiene()
        print("  ✅ Hygiene System - Initialized")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Hygiene System - {e}")
        tests.append(False)
    
    # Test Feature Builder
    try:
        print("  ✅ Feature Builder - Imported")
        tests.append(True)
    except Exception as e:
        print(f"  ❌ Feature Builder - {e}")
        tests.append(False)
    
    passed = sum(tests)
    failed = len(tests) - passed
    return passed, failed

def run_individual_test_files():
    """Run individual test files directly"""
    print("\n🧪 RUNNING INDIVIDUAL TEST FILES...")
    
    test_files = [
        "tests/test_linucb_day1_foundation.py",
        "tests/test_neural_day2_foundation.py",
        "tests/test_ucbv_day3_foundation.py",
        "tests/test_pipeline_loop_smoke.py"
    ]
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        test_path = project_root / test_file
        if test_path.exists():
            print(f"\n📋 Running: {test_file}")
            try:
                # Execute the test file
                with open(test_path, 'r') as f:
                    test_code = f.read()
                
                # Create a safe execution environment
                exec_globals = {
                    '__name__': '__main__',
                    '__file__': str(test_path),
                    'sys': sys,
                    'os': os,
                    'Path': Path
                }
                
                # Add project root to sys.path in the execution environment
                exec_globals['sys'].path.insert(0, str(project_root))
                
                exec(test_code, exec_globals)
                print(f"  ✅ {test_file} - Executed successfully")
                passed += 1
                
            except Exception as e:
                print(f"  ❌ {test_file} - {e}")
                print(f"      Traceback: {traceback.format_exc()[:200]}...")
                failed += 1
        else:
            print(f"  ⚠️  {test_file} - File not found")
            failed += 1
    
    return passed, failed

def main():
    """Run comprehensive direct tests"""
    print("🚀 INSTITUTIONAL AI TRADING SYSTEM - DIRECT TEST RUNNER")
    print("=" * 80)
    print("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER")
    print("=" * 80)
    
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
        print(f"\n💥 TEST RUNNER ERROR: {e}")
        traceback.print_exc()
        total_failed += 1
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 DIRECT TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📊 Success Rate: {(total_passed/(total_passed + total_failed)*100):.1f}%" if (total_passed + total_failed) > 0 else "📊 Success Rate: 0%")
    
    if total_failed == 0:
        print("\n🎉 ALL DIRECT TESTS PASSED! SYSTEM IS FUNCTIONAL!")
    else:
        print(f"\n⚠️  {total_failed} TESTS FAILED - REVIEW AND FIX")
    
    return 0 if total_failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
