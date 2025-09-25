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
    from CORE_SUPER_BANDITS.optimized_linucb_institutional import (
        OptimizedInstitutionalLinUCB,
    )

    training_logger.info("✅ LinUCB imported successfully", operation="enhanced_logging")

    # Create instance
    bandit = OptimizedInstitutionalLinUCB()
    training_logger.info("✅ LinUCB instance created", operation="enhanced_logging")

    # Check all methods
    methods = [method for method in dir(bandit) if not method.startswith("_")]
    training_logger.info(f"✅ Available methods: {methods}", operation="enhanced_logging")

    # Check specific methods
    training_logger.info(f"✅ get_arm_statistics exists: {hasattr(bandit, 'get_arm_statistics', operation="enhanced_logging")}")
    training_logger.info(f"✅ reset_arm exists: {hasattr(bandit, 'reset_arm', operation="enhanced_logging")}")
    training_logger.info(f"✅ get_confidence_for_context exists: {hasattr(bandit, 'get_confidence_for_context', operation="enhanced_logging")}"
    )

    # Try to call the methods
    try:
        stats = bandit.get_arm_statistics("test_arm")
        training_logger.info(f"✅ get_arm_statistics call successful: {stats}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"❌ get_arm_statistics call failed: {e}", operation="enhanced_logging")

    try:
        reset_result = bandit.reset_arm("test_arm")
        training_logger.info(f"✅ reset_arm call successful: {reset_result}", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"❌ reset_arm call failed: {e}", operation="enhanced_logging")

except Exception as e:
    training_logger.error(f"❌ Import failed: {e}", operation="enhanced_logging")
    import traceback

    traceback.print_exc()
