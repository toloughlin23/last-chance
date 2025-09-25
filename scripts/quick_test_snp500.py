#!/usr/bin/env python3
"""
Quick test to verify S&P 500 search is working
"""

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    training_logger.info("🔍 Testing S&P 500 search...", operation="enhanced_logging")

    provider = ActiveUniverseProvider()

    # Test with very small limit to avoid timeout
    candidates = provider._discover_candidates(limit=5)

    training_logger.info(f"✅ Found {len(candidates, operation="enhanced_logging")} candidates")
    training_logger.info(f"First 5: {candidates}", operation="enhanced_logging")

    if len(candidates) > 0:
        training_logger.info("🎉 S&P 500 search is working!", operation="enhanced_logging")
    else:
        training_logger.error("❌ S&P 500 search failed", operation="enhanced_logging")


if __name__ == "__main__":
    main()
