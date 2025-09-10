import os
import pytest

from utils.universe_selector import UniverseSelector


@pytest.mark.integration
def test_universe_selector_basic():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping universe selector test.")

    # small candidate set for test
    candidates = ["AAPL", "MSFT", "NVDA", "TSLA"]
    us = UniverseSelector()
    selected = us.select_universe(candidates, start_date="2023-01-03", end_date="2023-01-20", target_size=2)
    assert isinstance(selected, list)
    assert len(selected) <= 2
    for s in selected:
        assert s in candidates


