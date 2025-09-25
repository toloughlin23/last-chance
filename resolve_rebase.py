#!/usr/bin/env python3
"""
Resolve the stuck git rebase by completing the current commit
and continuing the rebase process.
"""
import os
import subprocess


def run_command(cmd, timeout=30):
    """Run a command with timeout"""
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
    training_logger.info("=== Resolving Stuck Git Rebase ===", operation="enhanced_logging")

    # Check if we're in a rebase
    if not os.path.exists(".git/rebase-merge"):
        training_logger.error("❌ Not in a rebase state", operation="enhanced_logging")
        return

    training_logger.info("✅ Confirmed: Repository is in rebase state", operation="enhanced_logging")

    # Step 1: Complete the current commit (it's already staged)
    training_logger.info("\n1. Completing current commit...", operation="enhanced_logging")
    code, out, err = run_command("git commit --no-edit")
    training_logger.info(f"Commit result: {code}", operation="enhanced_logging")
    if code == 0:
        training_logger.info("✅ Commit completed successfully", operation="enhanced_logging")
    else:
        training_logger.error(f"❌ Commit failed: {err}", operation="enhanced_logging")
        return

    # Step 2: Continue the rebase
    training_logger.info("\n2. Continuing rebase...", operation="enhanced_logging")
    code, out, err = run_command("git rebase --continue")
    training_logger.info(f"Continue result: {code}", operation="enhanced_logging")
    if code == 0:
        training_logger.info("✅ Rebase continued successfully", operation="enhanced_logging")
    else:
        training_logger.error(f"❌ Rebase continue failed: {err}", operation="enhanced_logging")
        # Try to abort if continue fails
        training_logger.info("\n3. Attempting to abort rebase...", operation="enhanced_logging")
        abort_code, abort_out, abort_err = run_command("git rebase --abort")
        if abort_code == 0:
            training_logger.info("✅ Rebase aborted successfully", operation="enhanced_logging")
        else:
            training_logger.error(f"❌ Failed to abort rebase: {abort_err}", operation="enhanced_logging")
        return

    # Step 3: Check final status
    training_logger.info("\n4. Final status check...", operation="enhanced_logging")
    code, out, err = run_command("git status --porcelain")
    training_logger.info(f"Status: {out}", operation="enhanced_logging")

    # Step 4: Check remote
    training_logger.info("\n5. Checking GitHub remote...", operation="enhanced_logging")
    code, out, err = run_command("git remote -v")
    training_logger.info(f"Remote: {out}", operation="enhanced_logging")

    training_logger.info("\n=== Rebase Resolution Complete ===", operation="enhanced_logging")


if __name__ == "__main__":
    main()
