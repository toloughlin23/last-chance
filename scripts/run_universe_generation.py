#!/usr/bin/env python3
"""
Run Universe Generation - Bypass terminal tool issues
This script runs the universe generation directly without terminal dependencies
"""

import os
import subprocess
from pathlib import Path


def run_command_safely(command):
    """Run a command safely with proper error handling."""
    try:
        universe_logger.info(f"🔄 Running: {command}", operation="enhanced_logging")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=Path.cwd(),
        )

        if result.returncode == 0:
            universe_logger.info("✅ Command completed successfully", operation="enhanced_logging")
            if result.stdout:
                universe_logger.info(f"📤 Output:\n{result.stdout}", operation="enhanced_logging")
            return True, result.stdout
        else:
            universe_logger.error(f"❌ Command failed with return code {result.returncode}", operation="enhanced_logging")
            if result.stderr:
                universe_logger.error(f"📤 Error:\n{result.stderr}", operation="enhanced_logging")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        universe_logger.info("⏰ Command timed out after 5 minutes", operation="enhanced_logging")
        return False, "Timeout"
    except Exception as e:
        universe_logger.error(f"💥 Command failed with exception: {e}", operation="enhanced_logging")
        return False, str(e)


def main():
    universe_logger.info("🚀 UNIVERSE GENERATION - BYPASS MODE", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")
    universe_logger.info("Running commands directly to bypass terminal tool issues", operation="enhanced_logging")
    universe_logger.info("=" * 50, operation="enhanced_logging")

    # Set environment
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    # Test 1: Basic Python test
    universe_logger.info("\n📊 Test 1: Basic Python functionality", operation="enhanced_logging")
    success, output = run_command_safely("python -c \"universe_logger.info('Python is working', operation="enhanced_logging")\"")
    if not success:
        universe_logger.error("❌ Basic Python test failed", operation="enhanced_logging")
        return

    # Test 2: Import test
    universe_logger.info("\n📊 Test 2: Module imports", operation="enhanced_logging")
    success, output = run_command_safely(
        "python -c \"from dotenv import load_dotenv; universe_logger.info('Imports working', operation="enhanced_logging")\""
    )
    if not success:
        universe_logger.error("❌ Import test failed", operation="enhanced_logging")
        return

    # Test 3: Provider test
    universe_logger.info("\n📊 Test 3: Provider initialization", operation="enhanced_logging")
    success, output = run_command_safely(
        "python -c \"from dotenv import load_dotenv; load_dotenv(); from utils.active_universe_provider import ActiveUniverseProvider; provider = ActiveUniverseProvider(); universe_logger.info('Provider initialized', operation="enhanced_logging")\""
    )
    if not success:
        universe_logger.error("❌ Provider test failed", operation="enhanced_logging")
        return

    # Test 4: Quick universe generation
    universe_logger.info("\n📊 Test 4: Quick universe generation", operation="enhanced_logging")
    success, output = run_command_safely("python scripts/quick_universe_test.py")
    if not success:
        universe_logger.error("❌ Quick universe test failed", operation="enhanced_logging")
        return

    universe_logger.info("\n🎯 ALL TESTS PASSED!", operation="enhanced_logging")
    universe_logger.info("The system is working correctly despite terminal tool issues", operation="enhanced_logging")


if __name__ == "__main__":
    main()
