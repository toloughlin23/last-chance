#!/usr/bin/env python3
import os
import subprocess

# Check if we're in a rebase
if os.path.exists(".git/rebase-merge"):
    training_logger.info("Repository is in rebase state. Attempting to resolve...", operation="enhanced_logging")

    # Try to complete the current commit
    try:
        result = subprocess.run(
            ["git", "commit", "--no-edit"], capture_output=True, text=True, timeout=10
        )
        training_logger.info(f"Commit result: {result.returncode}", operation="enhanced_logging")
        if result.stdout:
            training_logger.info(f"Output: {result.stdout}", operation="enhanced_logging")
        if result.stderr:
            training_logger.error(f"Error: {result.stderr}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"Commit failed: {e}", operation="enhanced_logging")

    # Try to continue the rebase
    try:
        result = subprocess.run(
            ["git", "rebase", "--continue"], capture_output=True, text=True, timeout=10
        )
        training_logger.info(f"Continue result: {result.returncode}", operation="enhanced_logging")
        if result.stdout:
            training_logger.info(f"Output: {result.stdout}", operation="enhanced_logging")
        if result.stderr:
            training_logger.error(f"Error: {result.stderr}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"Continue failed: {e}", operation="enhanced_logging")

    # Check final status
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5
        )
        training_logger.info(f"Final status: {result.returncode}", operation="enhanced_logging")
        training_logger.info(f"Status: {result.stdout}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"Status check failed: {e}", operation="enhanced_logging")
else:
    training_logger.info("Not in rebase state", operation="enhanced_logging")
