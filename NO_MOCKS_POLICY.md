# Zero-Contamination Build Policy

This repository enforces a strict "no mocks, no placeholders, no fake data" policy. All code must integrate with real systems or be intentionally left unimplemented with a clear contract. Do not include mock generators, fake files, or placeholder values.

## What is prohibited
- Mock or fake data generators
- Placeholder values like `REPLACE_ME`, `CHANGEME`, `YOUR_API_KEY`
- Lorem ipsum, dummy or sample data in source code
- Fake endpoints (e.g., `example.com/api` for production paths)
- Test scaffolds that simulate production data without clearly marked integration tests

## What is allowed
- Real integrations (e.g., Polygon.io) with keys provided via environment variables
- Skipping integration tests automatically when credentials are absent
- Explicit single-line allow with `nocontam: allow <reason>` when referencing prohibited tokens in a non-code context

## Enforcement
- Pre-commit hook runs a scanner that fails on prohibited patterns
- CI runs the scanner and integration tests
- Any violation blocks commits and pull requests

## How to add integrations safely
- Read credentials from environment variables (never commit secrets)
- Add minimal integration tests that call the real API and assert success
- Document setup in `README.md`
