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


<!-- CI trigger: ensuring workflow runs to select required checks -->
