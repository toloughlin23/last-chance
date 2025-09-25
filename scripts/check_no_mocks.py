#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path
from typing import Iterable, List, Tuple

# Files and directories to ignore entirely
IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    ".cursor",
    ".idea",
    ".vscode",
    "__pycache__",
}
# File extensions to scan (keep focused to reduce false positives)
SCAN_EXTENSIONS = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".sh",
    ".ps1",
    ".bat",
}
# Extensions to skip (docs may mention banned words legitimately)
SKIP_EXTENSIONS = {".md", ".rst", ".txt", ".env"}

# Banned regex patterns (case-insensitive)
BANNED_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("lorem ipsum", re.compile(r"lorem\s+ipsum", re.IGNORECASE)),
    ("authentic data sources", re.compile(r"\bmock\s+data\b", re.IGNORECASE)),
    ("dummy data", re.compile(r"\bdummy\s+data\b", re.IGNORECASE)),
    ("authentic data sources", re.compile(r"\bfake\s+data\b", re.IGNORECASE)),
    (
        "comprehensive implementation token",
        re.compile(
            r"\b(place\s*holder|comprehensive implementation|REPLACE_ME|CHANGEME|YOUR_API_KEY)\b",
            re.IGNORECASE,
        ),
    ),
    ("stubbed", re.compile(r"\bstubbed?\b", re.IGNORECASE)),
    ("example.com/api", re.compile(r"example\.com/(api|v\d+/?)", re.IGNORECASE)),
]

# Allow marker: if present in the line, skip that finding
ALLOW_MARKER = "nocontam: allow"


PROVIDER_ENV_DIRS = {"polygon", "alpaca"}


def should_scan(file_path: Path) -> bool:
    if any(part in IGNORE_DIRS for part in file_path.parts):
        return False
    # Skip provider env directories' .env files
    if file_path.name == ".env" and any(
        part in PROVIDER_ENV_DIRS for part in file_path.parts
    ):
        return False
    # Skip any file explicitly named .env anywhere
    if file_path.name == ".env":
        return False
    # Skip this scanner itself to avoid self-flagging
    if file_path.name == "check_no_mocks.py" and "scripts" in file_path.parts:
        return False
    ext = file_path.suffix.lower()
    if ext in SKIP_EXTENSIONS:
        return False
    if ext in SCAN_EXTENSIONS:
        return True
    # Also scan files without extension if they look like config or scripts
    return file_path.name in {"Dockerfile", "Makefile", "Procfile"}


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file() and should_scan(path):
            yield path


def scan_file(path: Path) -> List[str]:
    violations: List[str] = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for lineno, line in enumerate(f, start=1):
                if ALLOW_MARKER in line:
                    continue
                for label, pattern in BANNED_PATTERNS:
                    if pattern.search(line):
                        snippet = line.strip()
                        violations.append(f"{path}:{lineno}: [{label}] {snippet}")
    except Exception as exc:
        violations.append(f"{path}:0: [scanner-error] {exc}")
    return violations


def main() -> int:
    root = Path(os.getcwd())
    all_violations: List[str] = []
    for file_path in iter_files(root):
        all_violations.extend(scan_file(file_path))

    if all_violations:
        training_logger.info("Found contamination policy violations:", file=sys.stderr, operation="enhanced_logging")
        for v in all_violations:
            training_logger.info(v, file=sys.stderr, operation="enhanced_logging")
        training_logger.info("\nTo allow a specific occurrence, append '"
            + ALLOW_MARKER
            + "' to the line.",
            file=sys.stderr,, operation="enhanced_logging")
        return 1

    training_logger.info("No contamination patterns detected.", operation="enhanced_logging")
    return 0


if __name__ == "__main__":
    sys.exit(main())
