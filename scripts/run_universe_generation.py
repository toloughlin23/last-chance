#!/usr/bin/env python3
"""
Run Universe Generation - Bypass terminal tool issues
This script runs the universe generation directly without terminal dependencies
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command_safely(command):
    """Run a command safely with proper error handling."""
    try:
        print(f"🔄 Running: {command}")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            print("✅ Command completed successfully")
            if result.stdout:
                print(f"📤 Output:\n{result.stdout}")
            return True, result.stdout
        else:
            print(f"❌ Command failed with return code {result.returncode}")
            if result.stderr:
                print(f"📤 Error:\n{result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out after 5 minutes")
        return False, "Timeout"
    except Exception as e:
        print(f"💥 Command failed with exception: {e}")
        return False, str(e)

def main():
    print("🚀 UNIVERSE GENERATION - BYPASS MODE")
    print("=" * 50)
    print("Running commands directly to bypass terminal tool issues")
    print("=" * 50)
    
    # Set environment
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'
    
    # Test 1: Basic Python test
    print("\n📊 Test 1: Basic Python functionality")
    success, output = run_command_safely("python -c \"print('Python is working')\"")
    if not success:
        print("❌ Basic Python test failed")
        return
    
    # Test 2: Import test
    print("\n📊 Test 2: Module imports")
    success, output = run_command_safely("python -c \"from dotenv import load_dotenv; print('Imports working')\"")
    if not success:
        print("❌ Import test failed")
        return
    
    # Test 3: Provider test
    print("\n📊 Test 3: Provider initialization")
    success, output = run_command_safely("python -c \"from dotenv import load_dotenv; load_dotenv(); from utils.active_universe_provider import ActiveUniverseProvider; provider = ActiveUniverseProvider(); print('Provider initialized')\"")
    if not success:
        print("❌ Provider test failed")
        return
    
    # Test 4: Quick universe generation
    print("\n📊 Test 4: Quick universe generation")
    success, output = run_command_safely("python scripts/quick_universe_test.py")
    if not success:
        print("❌ Quick universe test failed")
        return
    
    print("\n🎯 ALL TESTS PASSED!")
    print("The system is working correctly despite terminal tool issues")

if __name__ == "__main__":
    main()


