#!/usr/bin/env python3
"""Debug Polygon API connection"""


from dotenv import load_dotenv

from services.polygon_client import PolygonClient


def main():
    load_dotenv()

    polygon_logger.info("Testing Polygon API connection...", operation="enhanced_logging")
    client = PolygonClient()

    # Test get_tickers
    polygon_logger.info("\n1. Testing get_tickers endpoint:", operation="enhanced_logging")
    try:
        data = client.get_tickers(market="stocks", active=True, limit=5)
        polygon_logger.info(f"   Status: {data.get('status', operation="enhanced_logging")}")
        polygon_logger.info(f"   Count: {data.get('count', operation="enhanced_logging")}")
        polygon_logger.info(f"   Results length: {len(data.get('results', [], operation="enhanced_logging"))}")

        if data.get("results"):
            first = data["results"][0]
            polygon_logger.info(f"   First ticker: {first.get('ticker', operation="enhanced_logging")}")
            polygon_logger.info(f"   Market cap: {first.get('market_cap', operation="enhanced_logging")}")
            polygon_logger.info(f"   Fields available: {list(first.keys(, operation="enhanced_logging"))[:10]}...")
    except Exception as e:
        polygon_logger.error(f"   Error: {e}", operation="enhanced_logging")

    # Test get_aggs
    polygon_logger.info("\n2. Testing get_aggs endpoint:", operation="enhanced_logging")
    try:
        data = client.get_aggs("AAPL", 1, "day", "2025-09-15", "2025-09-20", limit=5)
        polygon_logger.info(f"   Status: {data.get('status', operation="enhanced_logging")}")
        polygon_logger.info(f"   Results length: {len(data.get('results', [], operation="enhanced_logging"))}")
    except Exception as e:
        polygon_logger.error(f"   Error: {e}", operation="enhanced_logging")


if __name__ == "__main__":
    main()
