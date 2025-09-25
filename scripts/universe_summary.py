#!/usr/bin/env python3
"""
Universe Summary Reporter - Optimized Version
Uses the enhanced ActiveUniverseProvider with smart batching
"""

from __future__ import annotations

from datetime import date

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main() -> None:
    # Load environment variables from .env (e.g., POLYGON_API_KEY)
    load_dotenv()

    universe_logger.info("📚 Universe Summary", operation="enhanced_logging")
    universe_logger.info("==================", operation="enhanced_logging")
    universe_logger.info("Building active universe with smart batching...\n", operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Configuration
    target_size = 120
    analysis_days = 60

    # Get active universe with enhanced batching
    selected = provider.get_active_universe(
        target_size=target_size,
        analysis_days=analysis_days,
        force_refresh=True,
        batch_size=20,  # Process in batches of 20 to avoid timeouts
        adv_prefilter_min_dollar=100_000_000,  # $100M ADV minimum
    )

    universe_logger.info(f"\nSelected: {len(selected, operation="enhanced_logging")} symbols (target {target_size})")

    if selected:
        # Show top symbols
        universe_logger.info("\nTop 20 symbols:", operation="enhanced_logging")
        for i, sym in enumerate(selected[:20], 1):
            universe_logger.info(f"  {i:2d}. {sym}", operation="enhanced_logging")

        # Show full list if not too long
        if len(selected) <= 150:
            universe_logger.info(f"\nFull universe ({len(selected, operation="enhanced_logging")} symbols):")
            # Print in columns
            cols = 6
            for i in range(0, len(selected), cols):
                row = selected[i : i + cols]
                universe_logger.info("  " + "  ".join(f"{s:6s}" for s in row, operation="enhanced_logging"))

        # Save to file
        with open("data/universe_output.txt", "w") as f:
            f.write(f"Active Trading Universe - {len(selected)} symbols\n")
            f.write("=" * 50 + "\n")
            f.write(f"Analysis period: {analysis_days} days\n")
            f.write(f"Generated: {date.today()}\n")
            f.write("=" * 50 + "\n\n")

            for i, sym in enumerate(selected, 1):
                f.write(f"{i:3d}. {sym}\n")

        universe_logger.info("\n📄 Full list saved to data/universe_output.txt", operation="enhanced_logging")
    else:
        universe_logger.warning("\n⚠️ No symbols selected", operation="enhanced_logging")
        universe_logger.info("Please check:", operation="enhanced_logging")
        universe_logger.info("  1. POLYGON_API_KEY is set in .env file", operation="enhanced_logging")
        universe_logger.info("  2. Internet connectivity", operation="enhanced_logging")
        universe_logger.info("  3. Polygon API subscription level", operation="enhanced_logging")


if __name__ == "__main__":
    main()
