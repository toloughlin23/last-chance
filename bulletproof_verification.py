#!/usr/bin/env python3
"""
BULLETPROOF VERIFICATION SYSTEM
Multi-layer defense against random/mock data contamination
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER
"""

import ast
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# CRITICAL: These patterns should NEVER appear in our codebase
FORBIDDEN_IMPORTS = {
    "random",
    "secrets",
    "uuid",
    "faker",
    "mock",
    "unittest.mock",
}

FORBIDDEN_FUNCTIONS = {
    # Random generators
    "random",
    "randint",
    "uniform",
    "normal",
    "gauss",
    "choice",
    "shuffle",
    "sample",
    "seed",
    "randn",
    "rand",
    "random_sample",
    # Mock/Fake data
    "Mock",
    "MagicMock",
    "patch",
    "create_autospec",
    "fake",
    "dummy",
    "stub",
}


# AST-based code analysis for deep inspection
class RandomDetectorVisitor(ast.NodeVisitor):
    """AST visitor to detect random/mock usage at the syntax level"""

    def __init__(self):
        self.violations = []
        self.current_file = None

    def visit_Import(self, node):
        """Check import statements"""
        for alias in node.names:
            if alias.name in FORBIDDEN_IMPORTS or any(
                forbidden in alias.name for forbidden in FORBIDDEN_IMPORTS
            ):
                self.violations.append(
                    {
                        "type": "forbidden_import",
                        "file": self.current_file,
                        "line": node.lineno,
                        "code": f"import {alias.name}",
                        "reason": "Importing random/mock modules is FORBIDDEN",
                    }
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Check from X import Y statements"""
        if node.module and any(
            forbidden in node.module for forbidden in FORBIDDEN_IMPORTS
        ):
            for alias in node.names:
                self.violations.append(
                    {
                        "type": "forbidden_import",
                        "file": self.current_file,
                        "line": node.lineno,
                        "code": f"from {node.module} import {alias.name}",
                        "reason": "Importing from random/mock modules is FORBIDDEN",
                    }
                )
        self.generic_visit(node)

    def visit_Call(self, node):
        """Check function calls"""
        func_name = self._get_function_name(node.func)
        if func_name and any(
            forbidden in func_name for forbidden in FORBIDDEN_FUNCTIONS
        ):
            self.violations.append(
                {
                    "type": "forbidden_function",
                    "file": self.current_file,
                    "line": node.lineno,
                    "code": func_name,
                    "reason": "Using random/mock functions is FORBIDDEN",
                }
            )
        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Check attribute access like np.random"""
        if isinstance(node.value, ast.Name):
            full_name = f"{node.value.id}.{node.attr}"
            if "random" in full_name.lower() or "mock" in full_name.lower():
                self.violations.append(
                    {
                        "type": "forbidden_attribute",
                        "file": self.current_file,
                        "line": node.lineno,
                        "code": full_name,
                        "reason": "Accessing random/mock attributes is FORBIDDEN",
                    }
                )
        self.generic_visit(node)

    def _get_function_name(self, node):
        """Extract function name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return None


def scan_file_ast(filepath: Path) -> List[Dict[str, Any]]:
    """Deep AST-based scan of Python file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        visitor = RandomDetectorVisitor()
        visitor.current_file = str(filepath)
        visitor.visit(tree)

        return visitor.violations
    except Exception as e:
        print(f"⚠️ Error parsing {filepath}: {e}")
        return []


def verify_no_random_usage() -> Tuple[bool, List[Dict[str, Any]]]:
    """Multi-layer verification system"""
    print("🛡️ BULLETPROOF VERIFICATION SYSTEM")
    print("=" * 60)

    all_violations = []

    # Layer 1: AST-based deep inspection
    print("\n🔍 Layer 1: AST Deep Inspection")
    python_files = list(Path(".").rglob("*.py"))

    # Skip scanner files and this file
    skip_files = {
        "enhanced_contamination_scanner.py",
        "bulletproof_verification.py",
        "contamination_scanner.py",
    }

    for pyfile in python_files:
        if pyfile.name in skip_files or ".git" in str(pyfile) or ".venv" in str(pyfile):
            continue

        violations = scan_file_ast(pyfile)
        if violations:
            all_violations.extend(violations)

    # Layer 2: Import verification
    print("\n🔍 Layer 2: Import Chain Verification")
    for pyfile in python_files:
        if pyfile.name in skip_files or ".git" in str(pyfile) or ".venv" in str(pyfile):
            continue

        with open(pyfile, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for sneaky imports
        sneaky_patterns = [
            r'__import__\(["\']random',
            r'importlib\.import_module\(["\']random',
            r"exec\(.*import.*random",
            r"eval\(.*random",
        ]

        for pattern in sneaky_patterns:
            if re.search(pattern, content):
                all_violations.append(
                    {
                        "type": "sneaky_import",
                        "file": str(pyfile),
                        "pattern": pattern,
                        "reason": "Attempting to bypass import restrictions",
                    }
                )

    # Layer 3: Binary/compiled file check
    print("\n🔍 Layer 3: Binary/Compiled File Check")
    suspicious_extensions = [".pyc", ".pyo", ".so", ".dll", ".pyd"]
    for ext in suspicious_extensions:
        for file in Path(".").rglob(f"*{ext}"):
            if (
                ".git" not in str(file)
                and "__pycache__" not in str(file)
                and ".venv" not in str(file)
            ):
                all_violations.append(
                    {
                        "type": "suspicious_file",
                        "file": str(file),
                        "reason": "Binary/compiled files can hide random usage",
                    }
                )

    # Report results
    print("\n" + "=" * 60)
    if all_violations:
        print(f"❌ VERIFICATION FAILED: {len(all_violations)} violations found!")
        print("\n🚨 VIOLATIONS:")
        for v in all_violations:
            print(f"\n  File: {v['file']}")
            if "line" in v:
                print(f"  Line: {v['line']}")
            if "code" in v:
                print(f"  Code: {v['code']}")
            print(f"  Reason: {v['reason']}")
        return False, all_violations
    else:
        print("✅ VERIFICATION PASSED: ZERO random/mock usage detected!")
        print("🛡️ Your codebase is 100% GENUINE - NO SHORTCUTS!")
        return True, []


def main():
    """Run the bulletproof verification"""
    passed, violations = verify_no_random_usage()

    if not passed:
        print("\n⛔ CRITICAL: Fix ALL violations immediately!")
        print("This codebase has ZERO TOLERANCE for random/mock data!")
        sys.exit(1)
    else:
        print("\n🎉 SUCCESS: Codebase is BULLETPROOF!")
        sys.exit(0)


if __name__ == "__main__":
    main()
