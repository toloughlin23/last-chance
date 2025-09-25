#!/usr/bin/env python3
"""
Deep Diagnosis of Test Environment Issues
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import importlib
import os
import subprocess
import sys
from pathlib import Path


def diagnose_python_environment():
    """Diagnose Python environment and dependencies"""
    training_logger.info("🔍 DEEP DIAGNOSIS: PYTHON ENVIRONMENT", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Python version
    training_logger.info(f"Python Version: {sys.version}", operation="enhanced_logging")
    training_logger.info(f"Python Executable: {sys.executable}", operation="enhanced_logging")
    training_logger.info(f"Python Path: {sys.path[:3]}...", operation="enhanced_logging")

    # Check if we're in virtual environment
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        training_logger.info(f"✅ Virtual Environment: {venv}", operation="enhanced_logging")
    else:
        training_logger.warning("⚠️  No Virtual Environment detected", operation="enhanced_logging")

    # Check pip
    try:
        import pip

        training_logger.info(f"✅ pip version: {pip.__version__}", operation="enhanced_logging")
    except ImportError:
        training_logger.error("❌ pip not available", operation="enhanced_logging")

    # Check pytest
    try:
        import pytest

        training_logger.info(f"✅ pytest version: {pytest.__version__}", operation="enhanced_logging")
    except ImportError:
        training_logger.error("❌ pytest not installed", operation="enhanced_logging")

    # Check other critical dependencies
    critical_deps = ["numpy", "pandas", "requests", "dotenv"]

    training_logger.error("\n📦 CRITICAL DEPENDENCIES:", operation="enhanced_logging")
    for dep in critical_deps:
        try:
            module = importlib.import_module(dep)
            version = getattr(module, "__version__", "unknown")
            training_logger.info(f"  ✅ {dep}: {version}", operation="enhanced_logging")
        except ImportError:
            training_logger.error(f"  ❌ {dep}: NOT INSTALLED", operation="enhanced_logging")


def diagnose_project_structure():
    """Diagnose project structure and imports"""
    training_logger.info("\n🔍 DEEP DIAGNOSIS: PROJECT STRUCTURE", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    project_root = Path(__file__).parent.parent

    # Check critical directories
    critical_dirs = [
        "CORE_SUPER_BANDITS",
        "services",
        "pipeline",
        "tests",
        "utils",
        "scripts",
    ]

    training_logger.info("📁 DIRECTORY STRUCTURE:", operation="enhanced_logging")
    for dir_name in critical_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            files = list(dir_path.glob("*.py"))
            training_logger.info(f"  ✅ {dir_name}/ ({len(files, operation="enhanced_logging")} Python files)")
        else:
            training_logger.error(f"  ❌ {dir_name}/ - MISSING", operation="enhanced_logging")

    # Check critical files
    critical_files = [
        "CORE_SUPER_BANDITS/optimized_linucb_institutional.py",
        "services/advanced_news_sentiment.py",
        "services/infrastructure_manager.py",
        "pipeline/enhanced_runner.py",
        "tests/test_pipeline_loop_smoke.py",
    ]

    training_logger.error("\n📄 CRITICAL FILES:", operation="enhanced_logging")
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            training_logger.info(f"  ✅ {file_path} ({size} bytes, operation="enhanced_logging")")
        else:
            training_logger.error(f"  ❌ {file_path} - MISSING", operation="enhanced_logging")


def diagnose_import_issues():
    """Diagnose import issues systematically"""
    training_logger.info("\n🔍 DEEP DIAGNOSIS: IMPORT ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Add project root to path
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Test imports systematically
    import_tests = [
        ("CORE_SUPER_BANDITS.optimized_linucb_institutional", "LinUCB Algorithm"),
        ("services.advanced_news_sentiment", "News Sentiment"),
        ("services.infrastructure_manager", "Infrastructure Manager"),
        ("pipeline.enhanced_runner", "Enhanced Runner"),
        ("utils.universe_selector", "Universe Selector"),
    ]

    training_logger.info("🧪 IMPORT TESTS:", operation="enhanced_logging")
    for module_name, description in import_tests:
        try:
            module = importlib.import_module(module_name)
            training_logger.info(f"  ✅ {description}: {module.__name__}", operation="enhanced_logging")
        except ImportError as e:
            training_logger.error(f"  ❌ {description}: {e}", operation="enhanced_logging")
        except Exception as e:
            training_logger.warning(f"  ⚠️  {description}: {e}", operation="enhanced_logging")


def diagnose_pytest_issues():
    """Diagnose pytest specific issues"""
    training_logger.info("\n🔍 DEEP DIAGNOSIS: PYTEST ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    try:
        # Try to run pytest with version
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            training_logger.info(f"✅ pytest working: {result.stdout.strip(, operation="enhanced_logging")}")
        else:
            training_logger.error(f"❌ pytest error: {result.stderr}", operation="enhanced_logging")

    except subprocess.TimeoutExpired:
        training_logger.error("❌ pytest timeout - possible hanging process", operation="enhanced_logging")
    except FileNotFoundError:
        training_logger.error("❌ pytest not found in PATH", operation="enhanced_logging")
    except Exception as e:
        training_logger.error(f"❌ pytest error: {e}", operation="enhanced_logging")

    # Check pytest configuration
    project_root = Path(__file__).parent.parent
    pytest_ini = project_root / "pytest.ini"
    if pytest_ini.exists():
        training_logger.info(f"✅ pytest.ini found: {pytest_ini}", operation="enhanced_logging")
        training_logger.info(f"Content: {pytest_ini.read_text(, operation="enhanced_logging")[:200]}...")
    else:
        training_logger.warning("⚠️  pytest.ini not found", operation="enhanced_logging")


def diagnose_shell_issues():
    """Diagnose shell and terminal issues"""
    training_logger.info("\n🔍 DEEP DIAGNOSIS: SHELL ISSUES", operation="enhanced_logging")
    training_logger.info("=" * 60, operation="enhanced_logging")

    # Check environment variables
    shell_vars = ["SHELL", "TERM", "PAGER", "LESS"]
    for var in shell_vars:
        value = os.environ.get(var, "Not set")
        training_logger.info(f"  {var}: {value}", operation="enhanced_logging")

    # Check if we're in a pager
    if os.environ.get("PAGER") or os.environ.get("LESS"):
        training_logger.warning("⚠️  Pager environment detected - may cause terminal issues", operation="enhanced_logging")


def main():
    """Run comprehensive diagnosis"""
    training_logger.info("🚀 INSTITUTIONAL AI TRADING SYSTEM - DEEP DIAGNOSIS", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")
    training_logger.info("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER", operation="enhanced_logging")
    training_logger.info("=" * 80, operation="enhanced_logging")

    try:
        diagnose_python_environment()
        diagnose_project_structure()
        diagnose_import_issues()
        diagnose_pytest_issues()
        diagnose_shell_issues()

        training_logger.info("\n" + "=" * 80, operation="enhanced_logging")
        training_logger.info("🎯 DIAGNOSIS COMPLETE", operation="enhanced_logging")
        training_logger.info("=" * 80, operation="enhanced_logging")

    except Exception as e:
        training_logger.error(f"\n💥 DIAGNOSIS FAILED: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
