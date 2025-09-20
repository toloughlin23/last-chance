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
    print("🔍 DEEP DIAGNOSIS: PYTHON ENVIRONMENT")
    print("=" * 60)

    # Python version
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Path: {sys.path[:3]}...")

    # Check if we're in virtual environment
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        print(f"✅ Virtual Environment: {venv}")
    else:
        print("⚠️  No Virtual Environment detected")

    # Check pip
    try:
        import pip

        print(f"✅ pip version: {pip.__version__}")
    except ImportError:
        print("❌ pip not available")

    # Check pytest
    try:
        import pytest

        print(f"✅ pytest version: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not installed")

    # Check other critical dependencies
    critical_deps = ["numpy", "pandas", "requests", "dotenv"]

    print("\n📦 CRITICAL DEPENDENCIES:")
    for dep in critical_deps:
        try:
            module = importlib.import_module(dep)
            version = getattr(module, "__version__", "unknown")
            print(f"  ✅ {dep}: {version}")
        except ImportError:
            print(f"  ❌ {dep}: NOT INSTALLED")


def diagnose_project_structure():
    """Diagnose project structure and imports"""
    print("\n🔍 DEEP DIAGNOSIS: PROJECT STRUCTURE")
    print("=" * 60)

    project_root = Path(__file__).parent.parent

    # Check critical directories
    critical_dirs = ["CORE_SUPER_BANDITS", "services", "pipeline", "tests", "utils", "scripts"]

    print("📁 DIRECTORY STRUCTURE:")
    for dir_name in critical_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            files = list(dir_path.glob("*.py"))
            print(f"  ✅ {dir_name}/ ({len(files)} Python files)")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")

    # Check critical files
    critical_files = [
        "CORE_SUPER_BANDITS/optimized_linucb_institutional.py",
        "services/advanced_news_sentiment.py",
        "services/infrastructure_manager.py",
        "pipeline/enhanced_runner.py",
        "tests/test_pipeline_loop_smoke.py",
    ]

    print("\n📄 CRITICAL FILES:")
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"  ✅ {file_path} ({size} bytes)")
        else:
            print(f"  ❌ {file_path} - MISSING")


def diagnose_import_issues():
    """Diagnose import issues systematically"""
    print("\n🔍 DEEP DIAGNOSIS: IMPORT ISSUES")
    print("=" * 60)

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

    print("🧪 IMPORT TESTS:")
    for module_name, description in import_tests:
        try:
            module = importlib.import_module(module_name)
            print(f"  ✅ {description}: {module.__name__}")
        except ImportError as e:
            print(f"  ❌ {description}: {e}")
        except Exception as e:
            print(f"  ⚠️  {description}: {e}")


def diagnose_pytest_issues():
    """Diagnose pytest specific issues"""
    print("\n🔍 DEEP DIAGNOSIS: PYTEST ISSUES")
    print("=" * 60)

    try:
        # Try to run pytest with version
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            print(f"✅ pytest working: {result.stdout.strip()}")
        else:
            print(f"❌ pytest error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ pytest timeout - possible hanging process")
    except FileNotFoundError:
        print("❌ pytest not found in PATH")
    except Exception as e:
        print(f"❌ pytest error: {e}")

    # Check pytest configuration
    project_root = Path(__file__).parent.parent
    pytest_ini = project_root / "pytest.ini"
    if pytest_ini.exists():
        print(f"✅ pytest.ini found: {pytest_ini}")
        print(f"Content: {pytest_ini.read_text()[:200]}...")
    else:
        print("⚠️  pytest.ini not found")


def diagnose_shell_issues():
    """Diagnose shell and terminal issues"""
    print("\n🔍 DEEP DIAGNOSIS: SHELL ISSUES")
    print("=" * 60)

    # Check environment variables
    shell_vars = ["SHELL", "TERM", "PAGER", "LESS"]
    for var in shell_vars:
        value = os.environ.get(var, "Not set")
        print(f"  {var}: {value}")

    # Check if we're in a pager
    if os.environ.get("PAGER") or os.environ.get("LESS"):
        print("⚠️  Pager environment detected - may cause terminal issues")


def main():
    """Run comprehensive diagnosis"""
    print("🚀 INSTITUTIONAL AI TRADING SYSTEM - DEEP DIAGNOSIS")
    print("=" * 80)
    print("100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER")
    print("=" * 80)

    try:
        diagnose_python_environment()
        diagnose_project_structure()
        diagnose_import_issues()
        diagnose_pytest_issues()
        diagnose_shell_issues()

        print("\n" + "=" * 80)
        print("🎯 DIAGNOSIS COMPLETE")
        print("=" * 80)

    except Exception as e:
        print(f"\n💥 DIAGNOSIS FAILED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
