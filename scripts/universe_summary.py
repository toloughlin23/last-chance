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

    print("📚 Universe Summary")
    print("==================")
    print("Building active universe with smart batching...\n")

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

    print(f"\nSelected: {len(selected)} symbols (target {target_size})")

    if selected:
        # Show top symbols
        print("\nTop 20 symbols:")
        for i, sym in enumerate(selected[:20], 1):
            print(f"  {i:2d}. {sym}")

        # Show full list if not too long
        if len(selected) <= 150:
            print(f"\nFull universe ({len(selected)} symbols):")
            # Print in columns
            cols = 6
            for i in range(0, len(selected), cols):
                row = selected[i : i + cols]
                print("  " + "  ".join(f"{s:6s}" for s in row))

        # Save to file
        with open("data/universe_output.txt", "w") as f:
            f.write(f"Active Trading Universe - {len(selected)} symbols\n")
            f.write("=" * 50 + "\n")
            f.write(f"Analysis period: {analysis_days} days\n")
            f.write(f"Generated: {date.today()}\n")
            f.write("=" * 50 + "\n\n")

            for i, sym in enumerate(selected, 1):
                f.write(f"{i:3d}. {sym}\n")

        print("\n📄 Full list saved to data/universe_output.txt")
    else:
        print("\n⚠️ No symbols selected")
        print("Please check:")
        print("  1. POLYGON_API_KEY is set in .env file")
        print("  2. Internet connectivity")
        print("  3. Polygon API subscription level")


if __name__ == "__main__":
    main()
