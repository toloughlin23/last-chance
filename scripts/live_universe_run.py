#!/usr/bin/env python3
"""
Live Universe Run - Provider → Selector end-to-end using real Polygon data

Requirements:
- POLYGON_API_KEY in .env
- Uses ActiveUniverseProvider.get_active_universe (which runs the selector)

Outputs:
- Prints final selection count and a sample of symbols
- Saves JSON via provider's internal cache (data/active_universe_120.json)
"""

from __future__ import annotations

import os
import sys
from typing import List

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        print("❌ POLYGON_API_KEY not found in environment/.env")
        return 1

    try:
        from utils.active_universe_provider import ActiveUniverseProvider
    except Exception as e:
        print(f"❌ Failed to import provider: {e}")
        return 1

    try:
        provider = ActiveUniverseProvider()
        print("🚀 Running provider → selector (live)...")
        symbols: List[str] = provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,
        )
    except Exception as e:
        print(f"❌ Universe generation failed: {e}")
        return 1

    if not symbols:
        print("⚠️ No symbols returned. Check API access, rate limits, or try again later.")
        return 2

    print(f"✅ Selector picks: {len(symbols)} symbols")
    head = symbols[:20]
    print(f"Top 20: {head}")
    print("💾 Cached result should be at data/active_universe_120.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())



