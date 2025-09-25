#!/usr/bin/env python3
import subprocess


def run_git_command(cmd):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(
            f"git {cmd}", shell=True, capture_output=True, text=True, timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


training_logger.info("=== Diagnosing Git Rebase Issue ===", operation="enhanced_logging")

# Check current status
training_logger.info("\n1. Checking git status...", operation="enhanced_logging")
code, out, err = run_git_command("status --porcelain")
training_logger.info(f"Status: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")

# Check if we're in a rebase
training_logger.info("\n2. Checking if in rebase...", operation="enhanced_logging")
code, out, err = run_git_command("rev-parse --git-dir")
if code == 0:
    rebase_dir = f"{out}/rebase-merge"
    import os

    if os.path.exists(rebase_dir):
        training_logger.error("❌ STUCK IN REBASE - This is the problem!", operation="enhanced_logging")
        training_logger.info("Aborting rebase to fix the issue...", operation="enhanced_logging")

        abort_code, abort_out, abort_err = run_git_command("rebase --abort")
        training_logger.info(f"Abort result: {abort_code}", operation="enhanced_logging")
        training_logger.info(f"Abort output: {abort_out}", operation="enhanced_logging")
        training_logger.error(f"Abort error: {abort_err}", operation="enhanced_logging")

        if abort_code == 0:
            training_logger.info("✅ Rebase aborted successfully!", operation="enhanced_logging")
        else:
            training_logger.error("❌ Failed to abort rebase", operation="enhanced_logging")
    else:
        training_logger.info("✅ Not in rebase", operation="enhanced_logging")
else:
    training_logger.error(f"❌ Git error: {err}", operation="enhanced_logging")

# Check final status
training_logger.info("\n3. Final status after fix...", operation="enhanced_logging")
code, out, err = run_git_command("status --porcelain")
training_logger.info(f"Final status: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")

# Check remote
training_logger.info("\n4. Checking GitHub remote...", operation="enhanced_logging")
code, out, err = run_git_command("remote -v")
training_logger.info(f"Remote: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")
