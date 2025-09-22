#!/usr/bin/env python3
"""
Quick test to verify S&P 500 search is working
"""

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    print("🔍 Testing S&P 500 search...")

    provider = ActiveUniverseProvider()

    # Test with very small limit to avoid timeout
    candidates = provider._discover_candidates(limit=5)

    print(f"✅ Found {len(candidates)} candidates")
    print(f"First 5: {candidates}")

    if len(candidates) > 0:
        print("🎉 S&P 500 search is working!")
    else:
        print("❌ S&P 500 search failed")


if __name__ == "__main__":
    main()
