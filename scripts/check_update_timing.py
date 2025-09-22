#!/usr/bin/env python3
"""
Check optimal update timing for universe list
"""

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    print("🕐 UNIVERSE UPDATE TIMING ANALYSIS")
    print("=" * 50)

    provider = ActiveUniverseProvider()
    timing_info = provider.get_optimal_update_time()

    print(f"Current Time: {timing_info['current_time']}")
    print(f"Status: {timing_info['status']}")
    print(f"Next Optimal: {timing_info['next_optimal']}")

    print("\n📅 RECOMMENDED UPDATE WINDOWS:")
    for window, description in timing_info["recommended_windows"].items():
        print(f"  • {window}: {description}")

    print("\n💡 WHY THESE TIMES?")
    print("  • Pre-market (6-7 AM): Fresh data, before trading starts")
    print("  • Post-market (4:30-5 PM): Complete day's data available")
    print("  • Overnight (2-4 AM): Low API usage, fresh for next day")
    print("  • Mid-day (12-1 PM): Optional refresh for major changes")

    print("\n⚙️ CURRENT CACHE SETTINGS:")
    print("  • Cache Duration: 18 hours")
    print("  • Update Frequency: Daily")
    print("  • Cache Location: data/active_universe_120.json")

    print("\n🎯 RECOMMENDATION:")
    print(
        "  Update the universe list at 6:00 AM ET daily for optimal day trading performance!"
    )


if __name__ == "__main__":
    main()
