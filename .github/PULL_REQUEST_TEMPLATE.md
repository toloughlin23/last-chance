### Summary

Describe the change and why it improves functionality. Link issues/tickets.

### Zero-Contamination Checklist
- [ ] No mocks, placeholders, lorem ipsum, dummy/fake data, or stubs introduced
- [ ] Uses only real integrations (Polygon/Alpaca/etc.). If not available, code left unimplemented
- [ ] No example/fake endpoints or config files
- [ ] Tests updated and pass locally (`pytest -q`)
- [ ] Scanner passes locally (`python scripts/check_no_mocks.py`)

### Integration
- [ ] Polygon historical data used where applicable
- [ ] Secrets sourced from env only (no keys committed)

### Notes
Add any migration or operational notes.
