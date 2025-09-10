import os
from datetime import date, timedelta

import pytest

from services.polygon_client import PolygonClient


@pytest.mark.integration
def test_polygon_aggregates_daily_integration():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("Set POLYGON_API_KEY in environment to run this test")

    client = PolygonClient()
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=7)
    data = client.get_aggregates_daily("AAPL", start=start, end=end)

    assert isinstance(data, dict)
    # Expect a status and results array when data exists.
    assert data.get("status") in {"OK", "DELAYED"}
    assert "results" in data

import os
import pytest

from services.polygon_client import PolygonClient


@pytest.mark.integration
def test_polygon_client_aggs_real_api():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping PolygonClient integration test.")

    client = PolygonClient()
    data = client.get_aggs("AAPL", 1, "day", "2023-01-03", "2023-01-10", limit=5, adjusted=True, sort="asc")

    assert isinstance(data, dict)
    assert data.get("ticker") == "AAPL"
    results = data.get("results")
    assert isinstance(results, list) and len(results) > 0
    first = results[0]
    for field in ("o", "h", "l", "c", "v", "t"):
        assert field in first

