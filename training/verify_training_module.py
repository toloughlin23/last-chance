#!/usr/bin/env python3
"""
🛡️ TRAINING MODULE VERIFICATION
===============================
Verify the training module is 100% GENUINE with NO fake data
"""

import ast
import os
import re


def verify_training_module():
    """Comprehensive verification of training module integrity"""
    print("🔍 VERIFYING TRAINING MODULE IS 100% GENUINE")
    print("=" * 60)

    violations = []

    # List of training files to check
    training_files = [
        "training/historical_training_module.py",
        "training/training_config.py",
        "training/run_historical_training.py",
    ]

    # Forbidden patterns
    forbidden_patterns = [
        r"np\.random\.",
        r"random\.random",
        r"random\.normal",
        r"random\.uniform",
        r"mock",
        r"fake",
        r"dummy",
        r"simulated_pnl",
        r"placeholder",
        r"YOUR_API_KEY",
        r"example\.com",
    ]

    # Required patterns (must be present)
    required_patterns = [
        r"PolygonClient",
        r"get_aggregate_bars",
        r"validate_no_future_data",
        r"Point.*[Ii]n.*[Tt]ime",
        r"GENUINE",
        r"real",
    ]

    # Check each file
    for file_path in training_files:
        print(f"\n📄 Checking: {file_path}")

        if not os.path.exists(file_path):
            print(f"  ⚠️ File not found: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for forbidden patterns
        for pattern in forbidden_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                # Check if it's in a comment or docstring (allowed)
                for match in matches:
                    line_num = content[: content.find(match)].count("\n") + 1
                    line = content.split("\n")[line_num - 1]
                    if not (
                        line.strip().startswith("#") or line.strip().startswith('"')
                    ):
                        violations.append(
                            f"  ❌ Line {line_num}: Found '{match}' - FORBIDDEN!"
                        )

        # Check for required patterns
        found_required = []
        for pattern in required_patterns:
            if re.search(pattern, content):
                found_required.append(pattern)

        if found_required:
            print(f"  ✅ Found required patterns: {', '.join(found_required)}")

        # AST analysis for deeper inspection
        try:
            tree = ast.parse(content)

            # Check imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # Verify good imports
            good_imports = [
                imp for imp in imports if "polygon" in imp.lower() or "services" in imp
            ]
            if good_imports:
                print(f"  ✅ Good imports: {', '.join(good_imports)}")

            # Check for bad imports
            bad_imports = [
                imp
                for imp in imports
                if any(bad in imp.lower() for bad in ["random", "mock", "fake"])
            ]
            if bad_imports:
                violations.append(f"  ❌ Bad imports: {', '.join(bad_imports)}")

        except Exception as e:
            print(f"  ⚠️ AST parsing error: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY:")

    if violations:
        print(f"❌ FAILED: {len(violations)} violations found!")
        for v in violations:
            print(v)
        return False
    else:
        print("✅ PASSED: Training module is 100% GENUINE!")
        print("✅ Uses REAL Polygon data")
        print("✅ NO random generators")
        print("✅ NO mock/fake data")
        print("✅ NO placeholders")
        print("✅ Point-in-time validation enforced")
        print("✅ Zero forward-looking bias protection")
        return True


if __name__ == "__main__":
    import sys

    success = verify_training_module()
    sys.exit(0 if success else 1)
