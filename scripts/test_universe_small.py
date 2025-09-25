#!/usr/bin/env python3
"""Test universe selection with a small set of symbols"""

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    # Create provider with optimized settings for comprehensive analysis
    provider = ActiveUniverseProvider()

    # Override _discover_candidates to return a small test set
    original_discover = provider._discover_candidates

    def small_discover():
        # Curated set of 10 highly liquid symbols for comprehensive analysis
        return [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "NVDA",
            "TSLA",
            "META",
            "JPM",
            "V",
            "MA",
        ]

    try:
        provider._discover_candidates = small_discover

        # Get active universe with reduced analysis window
        universe_logger.info("Testing with 10 symbols...", operation="enhanced_logging")
        selected = provider.get_active_universe(
            target_size=5,
            analysis_days=7,  # Just 1 week to reduce API calls
            force_refresh=True,
            prefilter_max_symbols=10,  # Limit prefilter too
        )

        universe_logger.info(f"Selected {len(selected, operation="enhanced_logging")} symbols: {selected}")
    finally:
        # Restore original method to avoid side effects
        provider._discover_candidates = original_discover


if __name__ == "__main__":
    main()
