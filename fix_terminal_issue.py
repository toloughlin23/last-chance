#!/usr/bin/env python3
"""
Fix Terminal Issue - Direct execution
This bypasses the broken run_terminal_cmd tool
"""

import subprocess
import sys
import os

def execute_universe_generation():
    """Execute universe generation directly."""
    
    print("🚀 FIXING TERMINAL ISSUE - DIRECT EXECUTION")
    print("=" * 60)
    
    # Set environment
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'
    
    # Run the universe generation directly
    try:
        print("🔄 Running universe generation...")
        
        # Use subprocess to run the command directly
        result = subprocess.run([
            sys.executable,  # Use current Python interpreter
            "scripts/generate_training_universe.py"
        ], 
        env=env,
        capture_output=True,
        text=True,
        timeout=600  # 10 minute timeout
        )
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("📤 STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("📤 STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Universe generation completed successfully!")
        else:
            print("❌ Universe generation failed")
            
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    execute_universe_generation()


