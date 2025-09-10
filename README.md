## Zero-Contamination Build with Real Polygon Data

This project forbids mocks, placeholders, fake files, and fake data. All tests that touch market data use real Polygon historical endpoints.

### Setup (Windows)
- Install Python 3.11+
- In `polygon/.env`, set your Polygon API key as `POLYGON_API_KEY=...`
- Optionally add `alpaca/.env` with your Alpaca credentials for future use
- Install dependencies:
  ```powershell
  pip install -r requirements.txt
  ```
- (Optional) Enable pre-commit locally:
  ```powershell
  pip install pre-commit
  pre-commit install
  pre-commit install --hook-type pre-push
  ```

### Run contamination scanner
```powershell
python scripts/check_no_mocks.py
```

### Run tests
```powershell
pytest -q
```
- The Polygon integration test will automatically skip if `POLYGON_API_KEY` is not set.

### CI
- CI runs the scanner and tests. To enable real-data Polygon test in CI, add a repository secret named `POLYGON_API_KEY`.

### Enforcement & Governance
- PR template: `.github/PULL_REQUEST_TEMPLATE.md`
- Code owners: `.github/CODEOWNERS`
- Branch protection guide: `docs/BRANCH_PROTECTION.md`
- Policy: `NO_MOCKS_POLICY.md` and `.cursorrules`

### Hygiene (halts, earnings, SSR)
- What it does:
  - Halts: Removes symbols flagged as `tradingHalted` via Polygon snapshots.
  - Earnings: Optionally excludes symbols with an earnings announcement on the current US trading date.
  - SSR: Optionally excludes symbols that triggered short-sale restriction (≥10% intraday decline vs prior close, inferred from Polygon aggs).
- Auto toggles (by strategy_profile):
  - momentum: earnings_exclude = false, halts_exclude = true, ssr_exclude = true
  - mean_reversion: earnings_exclude = true, halts_exclude = true, ssr_exclude = true
  - long_only: earnings_exclude = true, halts_exclude = true, ssr_exclude = false
- How to use in the scheduler loop:
  ```python
  from pipeline.runner import run_loop

 chore/ci-smoke-pr
<!-- CI trigger: ensuring workflow runs to select required checks -->

CI: smoke PR to verify checks after rules fix.

  # Example: apply hygiene automatically for a momentum profile
  run_loop(
      symbols=["AAPL","MSFT","NVDA"],
      lookback_days=20,
      interval_seconds=60,
      market_hours_only=True,
      batch_size=20,
      strategy_profile="momentum",
      news_booster_enabled=True,
      prioritize_by_news=True,
  )
  ```
- One-shot usage (inside scripts):
  ```python
  from pipeline.runner import run_once

  run_once(
      symbols=["AAPL"],
      start_date="2024-12-01",
      end_date="2024-12-20",
      strategy_profile="mean_reversion",
  )
  ```
- Requirements: `POLYGON_API_KEY` must be set. All data comes from real Polygon endpoints.

### News priority and open booster
- What it does:
  - Pre-open (default 5 minutes before US open): builds a news sentiment priority list for the selected universe and saves it.
  - At open: processes top-K (default 15) from the news-priority list. If `news_booster_enabled`, it can filter to names with |news score| ≥ `news_booster_threshold`.
  - After warm-up (default 5 minutes): runs a single booster pass blending news score with early-session relative volume and gap, then resumes normal loop.
- Parameters (in `run_loop`):
  - `prioritize_by_news: bool` — enable news-priority ordering for the general loop.
  - `preopen_build_minutes: int` — minutes before open to build priority and universe.
  - `news_booster_enabled: bool` — enable the open booster logic.
  - `news_booster_threshold: float` — minimum absolute news score at open (e.g., 0.2).
  - `priority_top_k_open: int` — number of names at the first open pass.
  - `booster_warmup_minutes: int` — minutes after open before the booster pass runs.
  - `priority_top_k_boost: int` — number of names processed in the booster pass.
- Example:
  ```python
  from pipeline.runner import run_loop

  run_loop(
      symbols=["AAPL","MSFT","NVDA"],
      lookback_days=20,
      interval_seconds=60,
      market_hours_only=True,
      prioritize_by_news=True,
      news_booster_enabled=True,
      news_booster_threshold=0.2,
      priority_top_k_open=15,
      booster_warmup_minutes=5,
      priority_top_k_boost=15,
  )
  ```

### S&P 500 source and daily refresh
- Where: `services/sp500_client.py` fetches the live S&P 500 constituents from Wikipedia.
- Validation: candidates are validated against Polygon snapshots to drop stale/invalid tickers before selection.
- Cache: `utils/sp500_cache.py` stores the list once per day at `pipeline/sp500_symbols.json`.
- Usage in loop: enable `sp500_auto=True` (default) to use the S&P 500 list as the candidate universe at pre-open; pass `candidate_universe` to override.
- Example:
  ```python
  from pipeline.runner import run_loop

  run_loop(
      symbols=[],  # optional if sp500_auto=True
      lookback_days=20,
      interval_seconds=60,
      market_hours_only=True,
      sp500_auto=True,
      universe_target_size=120,
  )
  ```

<!-- CI: trigger push run to sync required status checks -->

<!-- CI: refresh pull_request status after rules change -->

<!-- CI: retrigger PR merge status 2 -->

<!-- CI: unblock via fresh PR branch -->
> main
