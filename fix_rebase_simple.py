#!/usr/bin/env python3
import os
import subprocess

# Check if we're in a rebase
if os.path.exists('.git/rebase-merge'):
    print("Repository is in rebase state. Attempting to resolve...")
    
    # Try to complete the current commit
    try:
        result = subprocess.run(['git', 'commit', '--no-edit'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Commit result: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Commit failed: {e}")
    
    # Try to continue the rebase
    try:
        result = subprocess.run(['git', 'rebase', '--continue'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Continue result: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Continue failed: {e}")
        
    # Check final status
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, timeout=5)
        print(f"Final status: {result.returncode}")
        print(f"Status: {result.stdout}")
    except Exception as e:
        print(f"Status check failed: {e}")
else:
    print("Not in rebase state")
