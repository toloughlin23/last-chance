#!/usr/bin/env python3
"""
Resolve the stuck git rebase by completing the current commit
and continuing the rebase process.
"""
import subprocess
import os
import sys

def run_command(cmd, timeout=30):
    """Run a command with timeout"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def main():
    print("=== Resolving Stuck Git Rebase ===")
    
    # Check if we're in a rebase
    if not os.path.exists('.git/rebase-merge'):
        print("❌ Not in a rebase state")
        return
    
    print("✅ Confirmed: Repository is in rebase state")
    
    # Step 1: Complete the current commit (it's already staged)
    print("\n1. Completing current commit...")
    code, out, err = run_command('git commit --no-edit')
    print(f"Commit result: {code}")
    if code == 0:
        print("✅ Commit completed successfully")
    else:
        print(f"❌ Commit failed: {err}")
        return
    
    # Step 2: Continue the rebase
    print("\n2. Continuing rebase...")
    code, out, err = run_command('git rebase --continue')
    print(f"Continue result: {code}")
    if code == 0:
        print("✅ Rebase continued successfully")
    else:
        print(f"❌ Rebase continue failed: {err}")
        # Try to abort if continue fails
        print("\n3. Attempting to abort rebase...")
        abort_code, abort_out, abort_err = run_command('git rebase --abort')
        if abort_code == 0:
            print("✅ Rebase aborted successfully")
        else:
            print(f"❌ Failed to abort rebase: {abort_err}")
        return
    
    # Step 3: Check final status
    print("\n4. Final status check...")
    code, out, err = run_command('git status --porcelain')
    print(f"Status: {out}")
    
    # Step 4: Check remote
    print("\n5. Checking GitHub remote...")
    code, out, err = run_command('git remote -v')
    print(f"Remote: {out}")
    
    print("\n=== Rebase Resolution Complete ===")

if __name__ == "__main__":
    main()
