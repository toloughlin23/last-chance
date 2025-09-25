#!/usr/bin/env python3
"""
Check optimal update timing for universe list
"""

from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def main():
    load_dotenv()

    training_logger.info("🕐 UNIVERSE UPDATE TIMING ANALYSIS", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    provider = ActiveUniverseProvider()
    timing_info = provider.get_optimal_update_time()

    training_logger.info(f"Current Time: {timing_info['current_time']}", operation="enhanced_logging")
    training_logger.info(f"Status: {timing_info['status']}", operation="enhanced_logging")
    training_logger.info(f"Next Optimal: {timing_info['next_optimal']}", operation="enhanced_logging")

    training_logger.info("\n📅 RECOMMENDED UPDATE WINDOWS:", operation="enhanced_logging")
    for window, description in timing_info["recommended_windows"].items():
        training_logger.info(f"  • {window}: {description}", operation="enhanced_logging")

    training_logger.info("\n💡 WHY THESE TIMES?", operation="enhanced_logging")
    training_logger.info("  • Pre-market (6-7 AM, operation="enhanced_logging"): Fresh data, before trading starts")
    training_logger.info("  • Post-market (4:30-5 PM, operation="enhanced_logging"): Complete day's data available")
    training_logger.info("  • Overnight (2-4 AM, operation="enhanced_logging"): Low API usage, fresh for next day")
    training_logger.info("  • Mid-day (12-1 PM, operation="enhanced_logging"): Optional refresh for major changes")

    training_logger.info("\n⚙️ CURRENT CACHE SETTINGS:", operation="enhanced_logging")
    training_logger.info("  • Cache Duration: 18 hours", operation="enhanced_logging")
    training_logger.info("  • Update Frequency: Daily", operation="enhanced_logging")
    training_logger.info("  • Cache Location: data/active_universe_120.json", operation="enhanced_logging")

    training_logger.info("\n🎯 RECOMMENDATION:", operation="enhanced_logging")
    training_logger.info("  Update the universe list at 6:00 AM ET daily for optimal day trading performance!", operation="enhanced_logging")


if __name__ == "__main__":
    main()
