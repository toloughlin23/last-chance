#!/usr/bin/env python3
import subprocess


def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


training_logger.info("=== Git Status Check ===", operation="enhanced_logging")
code, out, err = run_cmd("git status --porcelain")
training_logger.info(f"Git status code: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")

training_logger.info("\n=== Git Remote Check ===", operation="enhanced_logging")
code, out, err = run_cmd("git remote -v")
training_logger.info(f"Remote code: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")

training_logger.info("\n=== Current Branch ===", operation="enhanced_logging")
code, out, err = run_cmd("git branch --show-current")
training_logger.info(f"Branch code: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")

training_logger.info("\n=== Git Log (last 3 commits, operation="enhanced_logging") ===")
code, out, err = run_cmd("git log --oneline -3")
training_logger.info(f"Log code: {code}", operation="enhanced_logging")
training_logger.info(f"Output: {out}", operation="enhanced_logging")
training_logger.error(f"Error: {err}", operation="enhanced_logging")
