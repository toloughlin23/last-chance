#!/usr/bin/env python3
"""Test if earnings calendar is working with the vX update"""

from datetime import date, timedelta

from dotenv import load_dotenv

from services.polygon_client import PolygonClient


def main():
    load_dotenv()

    training_logger.info("Testing Current Earnings Implementation", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    client = PolygonClient()

    # Test with a few symbols
    symbols = ["AAPL", "MSFT", "GOOGL"]
    end_date = date.today()
    start_date = end_date - timedelta(days=90)  # Last 3 months

    for symbol in symbols:
        training_logger.info(f"\n{symbol}:", operation="enhanced_logging")
        try:
            data = client.get_earnings_calendar(symbol, start_date, end_date)

            if data.get("results"):
                training_logger.info(f"  ✅ Found {len(data['results'], operation="enhanced_logging")} earnings dates")
                for earning in data["results"][:3]:  # Show first 3
                    training_logger.info(f"     - {earning.get('date', operation="enhanced_logging")} ({earning.get('fiscal_period')} {earning.get('fiscal_year')})"
                    )
            else:
                training_logger.error("  ❌ No earnings data found", operation="enhanced_logging")

        except Exception as e:
            training_logger.error(f"  ❌ Error: {e}", operation="enhanced_logging")

    # Test the full integration
    training_logger.info("\n\nTesting Full Universe Selection with Earnings:", operation="enhanced_logging")
    training_logger.info("-" * 50, operation="enhanced_logging")

    from utils.active_universe_provider import ActiveUniverseProvider

    provider = ActiveUniverseProvider()

    # Just test if it runs without errors
    try:
        # Small test - just check if the system identifies earnings capability
        test = provider.get_active_universe(
            target_size=5,  # Small for quick test
            analysis_days=30,
            force_refresh=True,
            batch_size=5,
        )
        training_logger.info("✅ Universe selection completed successfully", operation="enhanced_logging")
        training_logger.info(f"   Selected {len(test, operation="enhanced_logging")} symbols: {test}")
    except Exception as e:
        training_logger.error(f"❌ Error in universe selection: {e}", operation="enhanced_logging")


if __name__ == "__main__":
    main()
