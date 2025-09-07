## Branch Protection Guide (GitHub)

1) Settings → Branches → Branch protection rules → Add rule
- Branch name pattern: `main`
- Require a pull request before merging: ON
- Require approvals: 1+ (or your policy)
- Dismiss stale approvals: optional
- Require status checks to pass before merging: ON
  - Select your CI workflow (CI)
- Require branches to be up to date before merging: ON
- Include administrators: recommended

2) Required status checks
- `Run contamination scanner` (part of CI job)
- `Run tests` (CI job that runs pytest)

3) Enforce linear history: optional

4) Restrict who can push to matching branches: recommended for `main`

5) CODEOWNERS
- Ensure `.github/CODEOWNERS` lists real owners. GitHub will request their review automatically.
