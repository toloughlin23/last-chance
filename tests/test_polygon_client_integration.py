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

