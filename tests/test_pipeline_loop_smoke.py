import os
import pytest
from pipeline.runner import run_loop


@pytest.mark.integration
def test_pipeline_run_loop_single_iteration(tmp_path):
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping pipeline loop test.")

    log_file = tmp_path / "loop.csv"
    run_loop(["AAPL"], lookback_days=7, interval_seconds=0, execute=False, log_path=str(log_file), iterations=1)
    assert log_file.exists()
    text = log_file.read_text(encoding="utf-8")
    assert "AAPL" in text

