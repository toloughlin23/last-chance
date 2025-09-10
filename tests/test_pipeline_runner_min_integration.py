import os
import pytest
from pathlib import Path

from pipeline.runner import run_once_min


@pytest.mark.integration
def test_pipeline_run_once_min_skips_without_key(tmp_path):
	if not os.getenv("POLYGON_API_KEY"):
		pytest.skip("POLYGON_API_KEY not set; skipping minimal pipeline test.")

	log_file = tmp_path / "min_log.csv"
	run_once_min(["AAPL"], days=5, log_path=str(log_file))
	assert log_file.exists()
	contents = log_file.read_text(encoding="utf-8")
	assert "AAPL" in contents
