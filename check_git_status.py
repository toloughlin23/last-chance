#!/usr/bin/env python3
import subprocess
import sys
import os

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

print("=== Git Status Check ===")
code, out, err = run_cmd("git status --porcelain")
print(f"Git status code: {code}")
print(f"Output: {out}")
print(f"Error: {err}")

print("\n=== Git Remote Check ===")
code, out, err = run_cmd("git remote -v")
print(f"Remote code: {code}")
print(f"Output: {out}")
print(f"Error: {err}")

print("\n=== Current Branch ===")
code, out, err = run_cmd("git branch --show-current")
print(f"Branch code: {code}")
print(f"Output: {out}")
print(f"Error: {err}")

print("\n=== Git Log (last 3 commits) ===")
code, out, err = run_cmd("git log --oneline -3")
print(f"Log code: {code}")
print(f"Output: {out}")
print(f"Error: {err}")
