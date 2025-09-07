#!/usr/bin/env python3
import os
import sys
import subprocess


def main() -> int:
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    cmd = [sys.executable, "-m", "pytest", "-q", "-m", "not integration"]
    rc = subprocess.call(cmd)
    # Pytest exit code 5 means 'no tests collected' — treat as success for quick hook
    if rc == 5:
        return 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
