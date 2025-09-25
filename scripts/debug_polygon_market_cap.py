#!/usr/bin/env python3
"""
Debug Polygon API market cap access to see what's really happening.
"""

import os
import sys

from dotenv import load_dotenv

try:
    from services.polygon_client import PolygonClient
except ImportError:
    sys.path.insert(0, os.path.abspath("."))
    from services.polygon_client import PolygonClient

load_dotenv()


def debug_polygon_market_cap():
    """Debug how we're accessing Polygon market cap data."""

    polygon_logger.info("🔍 DEBUGGING POLYGON MARKET CAP ACCESS", operation="enhanced_logging")
    polygon_logger.info("=" * 50, operation="enhanced_logging")

    try:
        polygon_client = PolygonClient()

        # Test 1: Check get_tickers endpoint
        polygon_logger.info("\n📊 Test 1: get_tickers endpoint", operation="enhanced_logging")
        polygon_logger.info("-" * 30, operation="enhanced_logging")

        data = polygon_client.get_tickers(market="stocks", active=True, limit=10)
        results = data.get("results", [])

        polygon_logger.info(f"Status: {data.get('status', 'Unknown', operation="enhanced_logging")}")
        polygon_logger.info(f"Count: {data.get('count', 0, operation="enhanced_logging")}")
        polygon_logger.info(f"Results: {len(results, operation="enhanced_logging")}")

        if results:
            polygon_logger.info("\nFirst few tickers:", operation="enhanced_logging")
            for i, ticker in enumerate(results[:3]):
                polygon_logger.info(f"  {i+1}. {ticker}", operation="enhanced_logging")
                # Check if market_cap is in the ticker data
                if "market_cap" in ticker:
                    polygon_logger.info(f"     Market Cap: {ticker['market_cap']}", operation="enhanced_logging")
                else:
                    polygon_logger.info("     Market Cap: NOT IN TICKER DATA", operation="enhanced_logging")

        # Test 2: Check get_ticker_details for specific symbols
        polygon_logger.info("\n📊 Test 2: get_ticker_details for specific symbols", operation="enhanced_logging")
        polygon_logger.info("-" * 40, operation="enhanced_logging")

        test_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "META"]

        for symbol in test_symbols:
            polygon_logger.info(f"\n🔍 Testing {symbol}:", operation="enhanced_logging")
            try:
                details = polygon_client.get_ticker_details(symbol)
                polygon_logger.info(f"   Status: {details.get('status', 'Unknown', operation="enhanced_logging")}")

                if details.get("results"):
                    result = details["results"]
                    polygon_logger.info(f"   Market Cap: {result.get('market_cap', 'NOT FOUND', operation="enhanced_logging")}")
                    polygon_logger.info(f"   Name: {result.get('name', 'NOT FOUND', operation="enhanced_logging")}")
                    polygon_logger.info(f"   Type: {result.get('type', 'NOT FOUND', operation="enhanced_logging")}")
                    polygon_logger.info(f"   Market: {result.get('market', 'NOT FOUND', operation="enhanced_logging")}")
                    polygon_logger.info(f"   Primary Exchange: {result.get('primary_exchange', 'NOT FOUND', operation="enhanced_logging")}"
                    )
                else:
                    polygon_logger.info("   No results found", operation="enhanced_logging")

            except Exception as e:
                polygon_logger.error(f"   ERROR: {e}", operation="enhanced_logging")

        # Test 3: Check if we need different parameters
        polygon_logger.info("\n📊 Test 3: Different get_tickers parameters", operation="enhanced_logging")
        polygon_logger.info("-" * 40, operation="enhanced_logging")

        # Try with different parameters
        test_params = [
            {"market": "stocks", "active": True, "limit": 5},
            {"market": "stocks", "active": "true", "limit": 5},
            {"market": "stocks", "limit": 5},
            {"market": "stocks", "active": True, "limit": 5, "sort": "ticker"},
        ]

        for i, params in enumerate(test_params):
            polygon_logger.info(f"\n  Test 3.{i+1}: {params}", operation="enhanced_logging")
            try:
                data = polygon_client.get_tickers(**params)
                results = data.get("results", [])
                polygon_logger.info(f"    Status: {data.get('status', operation="enhanced_logging")}")
                polygon_logger.info(f"    Count: {data.get('count', operation="enhanced_logging")}")
                polygon_logger.info(f"    Results: {len(results, operation="enhanced_logging")}")

                if results and len(results) > 0:
                    first_ticker = results[0]
                    polygon_logger.info(f"    First ticker keys: {list(first_ticker.keys(, operation="enhanced_logging"))}")
                    if "market_cap" in first_ticker:
                        polygon_logger.info(f"    First ticker market_cap: {first_ticker['market_cap']}", operation="enhanced_logging")
                    else:
                        polygon_logger.info("    First ticker market_cap: NOT FOUND", operation="enhanced_logging")

            except Exception as e:
                polygon_logger.error(f"    ERROR: {e}", operation="enhanced_logging")

        # Test 4: Check API key and permissions
        polygon_logger.info("\n📊 Test 4: API Key and Permissions", operation="enhanced_logging")
        polygon_logger.info("-" * 35, operation="enhanced_logging")

        # Check if we can access basic endpoints with comprehensive validation
        try:
            # 🚀 ENHANCED: Test real market data endpoint with intelligent validation
            market_data_response = polygon_client.get_aggs(
                "AAPL", 1, "day", "2024-01-01", "2024-01-02", limit=1
            )
            
            # Comprehensive response validation
            if market_data_response and 'status' in market_data_response:
                status = market_data_response.get('status')
                polygon_logger.info(f"   Aggs endpoint: {status}", operation="enhanced_logging")
                
                # Additional validation for data quality
                if status == 'OK' and 'results' in market_data_response:
                    results_count = len(market_data_response['results'])
                    polygon_logger.info(f"   Data quality: {results_count} records retrieved", operation="enhanced_logging")
                else:
                    polygon_logger.warning(f"   Data quality: No results in response", operation="enhanced_logging")
            else:
                polygon_logger.warning(f"   Aggs endpoint: Invalid response structure", operation="enhanced_logging")
                
        except Exception as e:
            polygon_logger.error(f"   Aggs endpoint ERROR: {e}", operation="enhanced_logging")

        # Test ticker details endpoint
        try:
            test_details = polygon_client.get_ticker_details("AAPL")
            polygon_logger.info(f"   Ticker details: {test_details.get('status', 'Unknown', operation="enhanced_logging")}")
        except Exception as e:
            polygon_logger.error(f"   Ticker details ERROR: {e}", operation="enhanced_logging")

        polygon_logger.info("\n🎯 SUMMARY:", operation="enhanced_logging")
        polygon_logger.info("=" * 20, operation="enhanced_logging")
        polygon_logger.info("The issue might be:", operation="enhanced_logging")
        polygon_logger.info("1. get_tickers doesn't include market_cap by default", operation="enhanced_logging")
        polygon_logger.info("2. We need to call get_ticker_details for each symbol", operation="enhanced_logging")
        polygon_logger.info("3. Some symbols might not have market_cap data", operation="enhanced_logging")
        polygon_logger.info("4. API key might not have access to market_cap data", operation="enhanced_logging")

        return True

    except Exception as e:
        polygon_logger.error(f"❌ Debug failed: {e}", operation="enhanced_logging")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = debug_polygon_market_cap()
    sys.exit(0 if success else 1)
