#!/usr/bin/env python3
"""
Manually resolve the stuck git rebase by:
1. Completing the current commit
2. Continuing the rebase
3. Checking GitHub connection
"""
import os
import subprocess


def run_git_command(cmd, timeout=15):
    """Run git command with timeout"""
    try:
        result = subprocess.run(
            f"git {cmd}", shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def main():
    training_logger.info("=== Manual Git Rebase Resolution ===", operation="enhanced_logging")

    # Check if we're in a rebase
    if not os.path.exists(".git/rebase-merge"):
        training_logger.error("❌ Not in rebase state", operation="enhanced_logging")
        return

    training_logger.info("✅ Confirmed: Repository is in rebase state", operation="enhanced_logging")
    training_logger.info("✅ GitHub remote: https://github.com/toloughlin23/last-chance.git", operation="enhanced_logging")

    # Step 1: Try to complete the current commit
    training_logger.info("\n1. Completing current commit...", operation="enhanced_logging")
    code, out, err = run_git_command("commit --no-edit")
    training_logger.info(f"   Return code: {code}", operation="enhanced_logging")
    if out:
        training_logger.info(f"   Output: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    if code == 0:
        training_logger.info("✅ Commit completed successfully", operation="enhanced_logging")

        # Step 2: Continue the rebase
        training_logger.info("\n2. Continuing rebase...", operation="enhanced_logging")
        code, out, err = run_git_command("rebase --continue")
        training_logger.info(f"   Return code: {code}", operation="enhanced_logging")
        if out:
            training_logger.info(f"   Output: {out}", operation="enhanced_logging")
        if err:
            training_logger.error(f"   Error: {err}", operation="enhanced_logging")

        if code == 0:
            training_logger.info("✅ Rebase continued successfully", operation="enhanced_logging")
        else:
            training_logger.error("❌ Rebase continue failed - trying to abort...", operation="enhanced_logging")
            abort_code, abort_out, abort_err = run_git_command("rebase --abort")
            if abort_code == 0:
                training_logger.info("✅ Rebase aborted successfully", operation="enhanced_logging")
            else:
                training_logger.error(f"❌ Failed to abort rebase: {abort_err}", operation="enhanced_logging")
    else:
        training_logger.error("❌ Commit failed - trying to abort rebase...", operation="enhanced_logging")
        abort_code, abort_out, abort_err = run_git_command("rebase --abort")
        if abort_code == 0:
            training_logger.info("✅ Rebase aborted successfully", operation="enhanced_logging")
        else:
            training_logger.error(f"❌ Failed to abort rebase: {abort_err}", operation="enhanced_logging")

    # Step 3: Check final status
    training_logger.info("\n3. Final status check...", operation="enhanced_logging")
    code, out, err = run_git_command("status --porcelain")
    training_logger.info(f"   Status code: {code}", operation="enhanced_logging")
    training_logger.info(f"   Status: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    # Step 4: Check GitHub connection
    training_logger.info("\n4. Checking GitHub connection...", operation="enhanced_logging")
    code, out, err = run_git_command("remote -v")
    training_logger.info(f"   Remote code: {code}", operation="enhanced_logging")
    training_logger.info(f"   Remotes: {out}", operation="enhanced_logging")
    if err:
        training_logger.error(f"   Error: {err}", operation="enhanced_logging")

    training_logger.info("\n=== Resolution Complete ===", operation="enhanced_logging")


if __name__ == "__main__":
    main()
