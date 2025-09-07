#!/usr/bin/env python3
import os
import sys
import subprocess


def main() -> int:
    # Disable autoload of 3rd-party plugins to avoid global env interference
    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    # Full test run (includes integration); test will skip if POLYGON_API_KEY missing
    cmd = [sys.executable, "-m", "pytest", "-q"]
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
