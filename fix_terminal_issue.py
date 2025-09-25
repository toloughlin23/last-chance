#!/usr/bin/env python3
"""
Fix Terminal Issue - Direct execution
This bypasses the broken run_terminal_cmd tool
"""

import os
import subprocess
import sys


def execute_universe_generation():
    """Execute universe generation directly."""

    training_logger.info("🚀 FIXING TERMINAL ISSUE - DIRECT EXECUTION", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Set environment
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    # Run the universe generation directly
    try:
        training_logger.info("🔄 Running universe generation...", operation="enhanced_logging")

        # Use subprocess to run the command directly
        result = subprocess.run(
            [
                sys.executable,  # Use current Python interpreter
                "scripts/generate_training_universe.py",
            ],
            env=env,
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
        )

        training_logger.info(f"Return code: {result.returncode}", operation="enhanced_logging")

        if result.stdout:
            training_logger.info("📤 STDOUT:", operation="enhanced_logging")
            training_logger.info(result.stdout, operation="enhanced_logging")

        if result.stderr:
            training_logger.info("📤 STDERR:", operation="enhanced_logging")
            training_logger.info(result.stderr, operation="enhanced_logging")

        if result.returncode == 0:
            training_logger.info("✅ Universe generation completed successfully!", operation="enhanced_logging")
        else:
            training_logger.error("❌ Universe generation failed", operation="enhanced_logging")

    except subprocess.TimeoutExpired:
        training_logger.info("⏰ Command timed out", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"💥 Error: {e}", operation="enhanced_logging")


if __name__ == "__main__":
    execute_universe_generation()
