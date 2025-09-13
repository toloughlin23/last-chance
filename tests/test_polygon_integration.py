import os
import time
import pytest
import requests  # type: ignore[import-untyped]

from utils.env_loader import load_env_from_known_locations


@pytest.mark.integration
def test_polygon_aggs_historical_data_real_api():
    # Load env from known locations: polygon/.env, alpaca/.env, project .env
    load_env_from_known_locations()

    api_key = os.getenv("POLYGON_API_KEY")
    if not api_key:
        pytest.skip("POLYGON_API_KEY not set; set it in polygon/.env or .env and retry.")

    # Use a narrow historical window to minimize rate limit/usage
    url = (
        "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-03/2023-01-10"
        "?adjusted=true&sort=asc&limit=5&apiKey=" + api_key
    )

    response = requests.get(url, timeout=30)
    assert response.status_code == 200, f"Unexpected status: {response.status_code} {response.text}"

    data = response.json()
    assert isinstance(data, dict)
    assert data.get("ticker") == "AAPL"

    results = data.get("results")
    assert isinstance(results, list) and len(results) > 0

    # Basic field checks on first result
    first = results[0]
    for field in ("o", "h", "l", "c", "v", "t"):
        assert field in first

    # Respect polite rate limits for CI/local reruns
    time.sleep(0.5)
