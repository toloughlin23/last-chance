#!/usr/bin/env python3
import subprocess
import sys

def run_git_command(cmd):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(
            f"git {cmd}", 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

print("=== Diagnosing Git Rebase Issue ===")

# Check current status
print("\n1. Checking git status...")
code, out, err = run_git_command("status --porcelain")
print(f"Status: {code}")
print(f"Output: {out}")
print(f"Error: {err}")

# Check if we're in a rebase
print("\n2. Checking if in rebase...")
code, out, err = run_git_command("rev-parse --git-dir")
if code == 0:
    rebase_dir = f"{out}/rebase-merge"
    import os
    if os.path.exists(rebase_dir):
        print("❌ STUCK IN REBASE - This is the problem!")
        print("Aborting rebase to fix the issue...")
        
        abort_code, abort_out, abort_err = run_git_command("rebase --abort")
        print(f"Abort result: {abort_code}")
        print(f"Abort output: {abort_out}")
        print(f"Abort error: {abort_err}")
        
        if abort_code == 0:
            print("✅ Rebase aborted successfully!")
        else:
            print("❌ Failed to abort rebase")
    else:
        print("✅ Not in rebase")
else:
    print(f"❌ Git error: {err}")

# Check final status
print("\n3. Final status after fix...")
code, out, err = run_git_command("status --porcelain")
print(f"Final status: {code}")
print(f"Output: {out}")
print(f"Error: {err}")

# Check remote
print("\n4. Checking GitHub remote...")
code, out, err = run_git_command("remote -v")
print(f"Remote: {code}")
print(f"Output: {out}")
print(f"Error: {err}")
