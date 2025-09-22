# 🚫 ZERO TOLERANCE: Random Data Policy

## THIS IS NON-NEGOTIABLE

**ABSOLUTELY NO RANDOM DATA, MOCK DATA, OR PLACEHOLDERS ARE ALLOWED IN THIS CODEBASE.**

## Why This Matters

1. **100% GENUINE**: Every line of code must use REAL data from REAL sources
2. **REPRODUCIBILITY**: All tests must produce EXACTLY the same results every time
3. **BULLETPROOF**: No flaky tests, no random failures, no intermittent issues
4. **PROFESSIONAL**: This is production-grade code, not a toy project

## What Is BANNED

### ❌ Random Data Generation
```python
# NEVER DO THIS:
np.random.random()
np.random.normal()
random.randint()
random.choice()
torch.rand()
uuid4()  # Use deterministic IDs
```

### ❌ Mock Data
```python
# NEVER DO THIS:
mock_response = {"fake": "data"}
@patch('module.function')
unittest.mock.Mock()
```

### ❌ Placeholders
```python
# NEVER DO THIS:
API_KEY = "YOUR_API_KEY_HERE"
url = "example.com/api"
data = "lorem ipsum"
```

## What To Do Instead

### ✅ Use Real Data Sources
- Polygon API for market data
- Real news APIs for sentiment
- Actual historical data for backtesting

### ✅ Deterministic Test Data
```python
# DO THIS:
test_features = np.array([0.1, -0.2, 0.3, ...])  # Fixed values
feature_hash = hash(identifier) % 1.0  # Deterministic from input
```

### ✅ Feature-Based Calculations
```python
# DO THIS:
variation = feature_std * deterministic_multiplier
confidence = base_value + feature_derived_adjustment
```

## Enforcement

1. **Pre-commit Hook**: Runs `enhanced_contamination_scanner.py` on EVERY commit
2. **CI/CD Pipeline**: Blocks ALL merges with violations
3. **Code Reviews**: ZERO TOLERANCE for violations

## How To Test Compliance

```bash
# Run the contamination scanner
python enhanced_contamination_scanner.py

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

## Consequences

- **Commit Blocked**: Pre-commit will prevent contaminated code
- **PR Rejected**: CI will fail any PR with violations
- **Immediate Fix Required**: No exceptions, no delays

## Remember

**"ALWAYS MAKE BETTER, NEVER REMOVE TO FIX"**
**"100% GENUINE - NO SHORTCUTS"**

This policy exists because we build BULLETPROOF systems that work with REAL data in REAL markets.

NO EXCEPTIONS. NO EXCUSES. ZERO TOLERANCE.





