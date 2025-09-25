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
        universe_logger.error("❌ POLYGON_API_KEY not found in environment/.env", operation="enhanced_logging")
        return 1

    try:
        from utils.active_universe_provider import ActiveUniverseProvider
    except Exception as e:
        universe_logger.error(f"❌ Failed to import provider: {e}", operation="enhanced_logging")
        return 1

    try:
        provider = ActiveUniverseProvider()
        universe_logger.info("🚀 Running provider → selector (live, operation="enhanced_logging")...")
        symbols: List[str] = provider.get_active_universe(
            target_size=120,
            analysis_days=60,
            force_refresh=True,
            batch_size=10,
        )
    except Exception as e:
        universe_logger.error(f"❌ Universe generation failed: {e}", operation="enhanced_logging")
        return 1

    if not symbols:
        universe_logger.warning("⚠️ No symbols returned. Check API access, rate limits, or try again later.", operation="enhanced_logging")
        return 2

    universe_logger.info(f"✅ Selector picks: {len(symbols, operation="enhanced_logging")} symbols")
    head = symbols[:20]
    universe_logger.info(f"Top 20: {head}", operation="enhanced_logging")
    universe_logger.info("💾 Cached result should be at data/active_universe_120.json", operation="enhanced_logging")
    return 0


if __name__ == "__main__":
    sys.exit(main())
