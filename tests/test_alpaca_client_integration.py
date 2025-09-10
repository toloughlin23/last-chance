import os
import pytest

from services.alpaca_client import AlpacaClient


@pytest.mark.integration
def test_alpaca_account_paper_mode():
    if not os.getenv("ALPACA_API_KEY") or not os.getenv("ALPACA_SECRET_KEY"):
        pytest.skip("Alpaca creds not set; skipping Alpaca client test.")

    client = AlpacaClient(paper=True)
    acct = client.get_account()
    assert isinstance(acct, dict)
    assert "id" in acct and "status" in acct

