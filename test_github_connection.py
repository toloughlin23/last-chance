#!/usr/bin/env python3
"""
Test GitHub connection and run full test suite
"""
import subprocess
import os
import sys

def run_command(cmd, timeout=10):
    """Run command with timeout"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def main():
    print("=== GitHub Connection & Test Suite ===")
    
    # Test 1: Check git status
    print("\n1. Checking git status...")
    code, out, err = run_command("git status --porcelain")
    print(f"   Status: {code}")
    print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    # Test 2: Check GitHub remote
    print("\n2. Checking GitHub remote...")
    code, out, err = run_command("git remote -v")
    print(f"   Remote: {code}")
    print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    # Test 3: Check current branch
    print("\n3. Checking current branch...")
    code, out, err = run_command("git branch --show-current")
    print(f"   Branch: {code}")
    print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    # Test 4: Run contamination scan
    print("\n4. Running contamination scan...")
    code, out, err = run_command("python scripts/check_no_mocks.py")
    print(f"   Scan: {code}")
    print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    # Test 5: Run pytest with plugins disabled
    print("\n5. Running pytest suite...")
    code, out, err = run_command("python -m pytest -q --tb=short")
    print(f"   Tests: {code}")
    print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
