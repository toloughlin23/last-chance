import os
import pytest
from pipeline.runner import run_once


@pytest.mark.integration
def test_pipeline_run_once_no_execute(tmp_path):
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping pipeline orchestrator test.")

    log_file = tmp_path / "log.csv"
    run_once(["AAPL"], "2023-01-03", "2023-01-10", execute=False, log_path=str(log_file))
    assert log_file.exists()
    contents = log_file.read_text(encoding="utf-8")
    assert "AAPL" in contents

