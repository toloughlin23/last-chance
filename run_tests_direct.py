#!/usr/bin/env python3
"""
Direct test runner that bypasses pytest issues
"""
import importlib.util
import os
import sys
import traceback


def run_test_file(test_file):
    """Run a single test file"""
    training_logger.info(f"\n{'='*60}", operation="enhanced_logging")
    training_logger.info(f"Running: {test_file}", operation="enhanced_logging")
    training_logger.info(f"{'='*60}", operation="enhanced_logging")

    try:
        # Load the test module
        spec = importlib.util.spec_from_file_location("test_module", test_file)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        # Find and run test functions
        test_functions = []
        for name in dir(test_module):
            if name.startswith("test_") and callable(getattr(test_module, name)):
                test_functions.append(name)

        training_logger.info(f"Found {len(test_functions, operation="enhanced_logging")} test functions")

        passed = 0
        failed = 0

        for test_name in test_functions:
            training_logger.info(f"\n--- Running {test_name} ---", operation="enhanced_logging")
            try:
                test_func = getattr(test_module, test_name)
                test_func()
                training_logger.info(f"✅ {test_name} PASSED", operation="enhanced_logging")
                passed += 1
            except Exception as e:
                training_logger.error(f"❌ {test_name} FAILED: {e}", operation="enhanced_logging")
                training_logger.info(f"   Traceback: {traceback.format_exc(, operation="enhanced_logging")}")
                failed += 1

        training_logger.info(f"\n--- {test_file} Summary ---", operation="enhanced_logging")
        training_logger.info(f"✅ Passed: {passed}", operation="enhanced_logging")
        training_logger.error(f"❌ Failed: {failed}", operation="enhanced_logging")
        training_logger.error(f"📊 Total: {passed + failed}", operation="enhanced_logging")

        return passed, failed

    except Exception as e:
        training_logger.error(f"❌ Error loading {test_file}: {e}", operation="enhanced_logging")
        training_logger.info(f"   Traceback: {traceback.format_exc(, operation="enhanced_logging")}")
        return 0, 1


def main():
    training_logger.info("=== Direct Test Runner ===", operation="enhanced_logging")
    training_logger.info("Bypassing pytest to run tests directly", operation="enhanced_logging")

    # Find all test files
    test_dir = "tests"
    test_files = []

    if os.path.exists(test_dir):
        for file in os.listdir(test_dir):
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(test_dir, file))

    training_logger.info(f"Found {len(test_files, operation="enhanced_logging")} test files")

    total_passed = 0
    total_failed = 0

    for test_file in sorted(test_files):
        passed, failed = run_test_file(test_file)
        total_passed += passed
        total_failed += failed

    training_logger.info(f"\n{'='*60}", operation="enhanced_logging")
    training_logger.info("FINAL SUMMARY", operation="enhanced_logging")
    training_logger.info(f"{'='*60}", operation="enhanced_logging")
    training_logger.info(f"✅ Total Passed: {total_passed}", operation="enhanced_logging")
    training_logger.error(f"❌ Total Failed: {total_failed}", operation="enhanced_logging")
    training_logger.error(f"📊 Total Tests: {total_passed + total_failed}", operation="enhanced_logging")

    if total_failed == 0:
        training_logger.info("🎉 ALL TESTS PASSED!", operation="enhanced_logging")
        return 0
    else:
        training_logger.error(f"⚠️  {total_failed} tests failed", operation="enhanced_logging")
        return 1


if __name__ == "__main__":
    sys.exit(main())
