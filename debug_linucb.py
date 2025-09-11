#!/usr/bin/env python3
"""
Debug LinUCB methods issue
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
    
    print("✅ LinUCB imported successfully")
    
    # Create instance
    bandit = OptimizedInstitutionalLinUCB()
    print("✅ LinUCB instance created")
    
    # Check all methods
    methods = [method for method in dir(bandit) if not method.startswith('_')]
    print(f"✅ Available methods: {methods}")
    
    # Check specific methods
    print(f"✅ get_arm_statistics exists: {hasattr(bandit, 'get_arm_statistics')}")
    print(f"✅ reset_arm exists: {hasattr(bandit, 'reset_arm')}")
    print(f"✅ get_confidence_for_context exists: {hasattr(bandit, 'get_confidence_for_context')}")
    
    # Try to call the methods
    try:
        stats = bandit.get_arm_statistics("test_arm")
        print(f"✅ get_arm_statistics call successful: {stats}")
    except Exception as e:
        print(f"❌ get_arm_statistics call failed: {e}")
    
    try:
        reset_result = bandit.reset_arm("test_arm")
        print(f"✅ reset_arm call successful: {reset_result}")
    except Exception as e:
        print(f"❌ reset_arm call failed: {e}")
        
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
