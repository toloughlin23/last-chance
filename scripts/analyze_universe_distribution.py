"""
Analyze the first-letter distribution of the latest universe file.

Search order:
- data/active_universe_120.json
- Most recent file matching data/snapshots/active_universe_*.json

Prints:
- Total symbol count
- First-letter counts (A..Z, others grouped as '#')

This script is intentionally simple to avoid shell quoting issues.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Sequence


def _load_symbols_from_file(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    # Support either {"symbols": [...]} or raw list
    if isinstance(data, dict) and "symbols" in data:
        symbols = data["symbols"]
    else:
        symbols = data
    if not isinstance(symbols, Sequence):
        raise TypeError(f"Unexpected universe format in {path}")
    # Normalize to strings and strip whitespace
    return [str(s).strip() for s in symbols if str(s).strip()]


def _pick_latest_universe_file() -> Path:
    primary = Path("data/active_universe_120.json")
    if primary.exists():
        return primary
    snap_dir = Path("data/snapshots")
    if snap_dir.exists():
        snapshots = sorted(
            snap_dir.glob("active_universe_*.json"), key=lambda p: p.stat().st_mtime, reverse=True
        )
        if snapshots:
            return snapshots[0]
    raise FileNotFoundError("No universe file found: data/active_universe_120.json or snapshots")


def _first_letter_bucket(symbol: str) -> str:
    if not symbol:
        return "#"
    c = symbol[0].upper()
    return c if "A" <= c <= "Z" else "#"


def analyze_distribution(symbols: Iterable[str]) -> Counter:
    counts: Counter = Counter()
    for s in symbols:
        counts[_first_letter_bucket(s)] += 1
    return counts


def main(argv: List[str]) -> int:
    if len(argv) > 1:
        path = Path(argv[1])
    else:
        path = _pick_latest_universe_file()
    symbols = _load_symbols_from_file(path)

    counts = analyze_distribution(symbols)
    total = len(symbols)

    print(f"File: {path}")
    print(f"Total symbols: {total}")
    for key in [chr(c) for c in range(ord("A"), ord("Z") + 1)] + ["#"]:
        if key in counts:
            pct = 100.0 * counts[key] / total if total else 0.0
            print(f"{key}: {counts[key]} ({pct:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))



