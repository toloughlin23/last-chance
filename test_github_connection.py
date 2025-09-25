#!/usr/bin/env python3
"""
Test GitHub connection and run full test suite
"""
import subprocess


def run_command(cmd, timeout=10):
    """Run command with timeout"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def main():
    training_logger.info("=== GitHub Connection & Test Suite ===", operation="enhanced_logging")

    # Test 1: Check git status
    training_logger.info("\n1. Checking git status...", operation="enhanced_logging")
    code, out, err = run_command("git status --porcelain")
    training_logger.info(f"   Status: {code}", operation="enhanced_logging")
    training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    # Test 2: Check GitHub remote
    training_logger.info("\n2. Checking GitHub remote...", operation="enhanced_logging")
    code, out, err = run_command("git remote -v")
    training_logger.info(f"   Remote: {code}", operation="enhanced_logging")
    training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    # Test 3: Check current branch
    training_logger.info("\n3. Checking current branch...", operation="enhanced_logging")
    code, out, err = run_command("git branch --show-current")
    training_logger.info(f"   Branch: {code}", operation="enhanced_logging")
    training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    # Test 4: Run contamination scan
    training_logger.info("\n4. Running contamination scan...", operation="enhanced_logging")
    code, out, err = run_command("python scripts/check_no_mocks.py")
    training_logger.info(f"   Scan: {code}", operation="enhanced_logging")
    training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    # Test 5: Run pytest with plugins disabled
    training_logger.info("\n5. Running pytest suite...", operation="enhanced_logging")
    code, out, err = run_command("python -m pytest -q --tb=short")
    training_logger.info(f"   Tests: {code}", operation="enhanced_logging")
    training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    training_logger.info("\n=== Test Complete ===", operation="enhanced_logging")


if __name__ == "__main__":
    main()
