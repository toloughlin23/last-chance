import os
import pytest

from pipeline.hygiene import Hygiene


pytestmark = pytest.mark.integration


def _have_polygon_key() -> bool:
    return bool(os.getenv("POLYGON_API_KEY"))


@pytest.mark.skipif(not _have_polygon_key(), reason="POLYGON_API_KEY not set; see polygon/.env or project .env")
def test_halts_filter_runs_without_error():
    h = Hygiene()
    # Use a couple of liquid symbols; we only assert that the call executes
    out = h.filter_symbols(["AAPL", "MSFT"], strategy_profile="mean_reversion")
    assert isinstance(out, list)


@pytest.mark.skipif(not _have_polygon_key(), reason="POLYGON_API_KEY not set; see polygon/.env or project .env")
def test_earnings_filter_runs_without_error():
    h = Hygiene()
    # We force earnings_exclude True to exercise the path
    out = h.filter_symbols(["AAPL", "MSFT"], strategy_profile="mean_reversion", earnings_exclude=True)
    assert isinstance(out, list)


@pytest.mark.skipif(not _have_polygon_key(), reason="POLYGON_API_KEY not set; see polygon/.env or project .env")
def test_ssr_filter_runs_without_error():
    h = Hygiene()
    out = h.filter_symbols(["AAPL", "MSFT"], strategy_profile="mean_reversion", ssr_exclude=True)
    assert isinstance(out, list)



