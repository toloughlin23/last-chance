#!/usr/bin/env python3
"""
Direct test runner that bypasses pytest issues
"""
import sys
import os
import importlib.util
import traceback

def run_test_file(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print(f"{'='*60}")
    
    try:
        # Load the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        # Find and run test functions
        test_functions = []
        for name in dir(test_module):
            if name.startswith('test_') and callable(getattr(test_module, name)):
                test_functions.append(name)
        
        print(f"Found {len(test_functions)} test functions")
        
        passed = 0
        failed = 0
        
        for test_name in test_functions:
            print(f"\n--- Running {test_name} ---")
            try:
                test_func = getattr(test_module, test_name)
                test_func()
                print(f"✅ {test_name} PASSED")
                passed += 1
            except Exception as e:
                print(f"❌ {test_name} FAILED: {e}")
                print(f"   Traceback: {traceback.format_exc()}")
                failed += 1
        
        print(f"\n--- {test_file} Summary ---")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Total: {passed + failed}")
        
        return passed, failed
        
    except Exception as e:
        print(f"❌ Error loading {test_file}: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
        return 0, 1

def main():
    print("=== Direct Test Runner ===")
    print("Bypassing pytest to run tests directly")
    
    # Find all test files
    test_dir = "tests"
    test_files = []
    
    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(test_dir, file))
    
    print(f"Found {len(test_files)} test files")
    
    total_passed = 0
    total_failed = 0
    
    for test_file in sorted(test_files):
        passed, failed = run_test_file(test_file)
        total_passed += passed
        total_failed += failed
    
    print(f"\n{'='*60}")
    print(f"FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Total Passed: {total_passed}")
    print(f"❌ Total Failed: {total_failed}")
    print(f"📊 Total Tests: {total_passed + total_failed}")
    
    if total_failed == 0:
        print(f"🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"⚠️  {total_failed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
