import os
import pytest
from datetime import datetime, UTC, timedelta

from services.quotes_client import QuotesClient


@pytest.mark.integration
def test_quotes_client_median_spread():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping quotes client test.")

    qc = QuotesClient()
    # Use a small 1-day window for test
    end = datetime.now(UTC)
    start = end - timedelta(hours=2)
    quotes = qc.fetch_quotes_window("AAPL", start, end, limit=5000)
    med_dollar, med_bps = qc.compute_median_spreads(quotes)
    assert med_dollar > 0
    assert med_bps > 0
