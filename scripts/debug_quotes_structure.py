#!/usr/bin/env python3
"""Debug the structure of quotes data"""

import json
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from services.quotes_client import QuotesClient


def main():
    load_dotenv()

    client = QuotesClient()

    # Get a recent trading day
    end = datetime.now(timezone.utc)
    days_back = 1
    while (end - timedelta(days=days_back)).weekday() >= 5:
        days_back += 1

    test_date = end - timedelta(days=days_back)
    start_time = test_date.replace(hour=14, minute=30, second=0, microsecond=0)
    end_time = test_date.replace(
        hour=14, minute=35, second=0, microsecond=0
    )  # Just 5 minutes

    training_logger.info(f"Fetching quotes for AAPL from {start_time} to {end_time}", operation="enhanced_logging")

    quotes = client.fetch_quotes_window("AAPL", start_time, end_time, limit=5)

    training_logger.info(f"\nReceived {len(quotes, operation="enhanced_logging")} quotes")

    if quotes:
        training_logger.info("\nStructure of first quote:", operation="enhanced_logging")
        training_logger.info(json.dumps(quotes[0], indent=2, default=str, operation="enhanced_logging"))

        training_logger.info("\nAll available fields:", operation="enhanced_logging")
        training_logger.info(list(quotes[0].keys(, operation="enhanced_logging")))
    else:
        training_logger.info("No quotes received!", operation="enhanced_logging")

        # Try a direct API call to see raw response
        training_logger.info("\nTrying direct API call...", operation="enhanced_logging")
        url = f"{client.base}/v3/quotes/AAPL"
        params = {
            "timestamp.gte": start_time.isoformat().replace("+00:00", "Z"),
            "timestamp.lte": end_time.isoformat().replace("+00:00", "Z"),
            "limit": 5,
            "order": "asc",
        }
        params["apiKey"] = client.api_key

        import requests

        resp = requests.get(url, params=params)
        training_logger.info(f"Status: {resp.status_code}", operation="enhanced_logging")
        if resp.status_code == 200:
            data = resp.json()
            training_logger.info(f"Response keys: {list(data.keys(, operation="enhanced_logging"))}")
            if "results" in data and data["results"]:
                training_logger.info("\nFirst result structure:", operation="enhanced_logging")
                training_logger.info(json.dumps(data["results"][0], indent=2, operation="enhanced_logging"))


if __name__ == "__main__":
    main()
