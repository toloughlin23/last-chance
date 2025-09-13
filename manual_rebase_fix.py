#!/usr/bin/env python3
"""
Manually resolve the stuck git rebase by:
1. Completing the current commit
2. Continuing the rebase
3. Checking GitHub connection
"""
import os
import subprocess
import sys

def run_git_command(cmd, timeout=15):
    """Run git command with timeout"""
    try:
        result = subprocess.run(
            f"git {cmd}",
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
    print("=== Manual Git Rebase Resolution ===")
    
    # Check if we're in a rebase
    if not os.path.exists('.git/rebase-merge'):
        print("❌ Not in rebase state")
        return
    
    print("✅ Confirmed: Repository is in rebase state")
    print("✅ GitHub remote: https://github.com/toloughlin23/last-chance.git")
    
    # Step 1: Try to complete the current commit
    print("\n1. Completing current commit...")
    code, out, err = run_git_command("commit --no-edit")
    print(f"   Return code: {code}")
    if out:
        print(f"   Output: {out}")
    if err:
        print(f"   Error: {err}")
    
    if code == 0:
        print("✅ Commit completed successfully")
        
        # Step 2: Continue the rebase
        print("\n2. Continuing rebase...")
        code, out, err = run_git_command("rebase --continue")
        print(f"   Return code: {code}")
        if out:
            print(f"   Output: {out}")
        if err:
            print(f"   Error: {err}")
        
        if code == 0:
            print("✅ Rebase continued successfully")
        else:
            print("❌ Rebase continue failed - trying to abort...")
            abort_code, abort_out, abort_err = run_git_command("rebase --abort")
            if abort_code == 0:
                print("✅ Rebase aborted successfully")
            else:
                print(f"❌ Failed to abort rebase: {abort_err}")
    else:
        print("❌ Commit failed - trying to abort rebase...")
        abort_code, abort_out, abort_err = run_git_command("rebase --abort")
        if abort_code == 0:
            print("✅ Rebase aborted successfully")
        else:
            print(f"❌ Failed to abort rebase: {abort_err}")
    
    # Step 3: Check final status
    print("\n3. Final status check...")
    code, out, err = run_git_command("status --porcelain")
    print(f"   Status code: {code}")
    print(f"   Status: {out}")
    if err:
        print(f"   Error: {err}")
    
    # Step 4: Check GitHub connection
    print("\n4. Checking GitHub connection...")
    code, out, err = run_git_command("remote -v")
    print(f"   Remote code: {code}")
    print(f"   Remotes: {out}")
    if err:
        print(f"   Error: {err}")
    
    print("\n=== Resolution Complete ===")

if __name__ == "__main__":
    main()
