import os
import pytest

from services.news_client import NewsClient


@pytest.mark.integration
def test_news_client_fetch_symbol_news():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping news client test.")

    client = NewsClient()
    items = client.fetch_symbol_news("AAPL", limit=5, order="desc")
    assert isinstance(items, list)
    if items:
        first = items[0]
        assert isinstance(first, dict)
        assert "title" in first

