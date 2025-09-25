# Polygon.io Integration Documentation

## Overview

This repository uses Polygon.io as the primary source of truth for ALL market data. No mock data, no placeholders. This document explains exactly how we access data reliably, how to paginate, which endpoints to use for each metric, and which subscription features affect access. It also documents the precise, production-ready approach to retrieve S&P 500 constituents using ONLY Polygon.

## Current Subscription Level

You are on: **Stocks Advanced (Individual $199/mo) + Benzinga News ($99/mo)**

Notes:
- Indices Basic shows as a separate product. Enabling it may require plan changes in the dashboard UI; we therefore assume no Indices API access and use the Stocks APIs only.
- All guidance below works with Stocks Advanced without needing to downgrade.

## Available Endpoints & Features

### ✅ Working Endpoints (Stocks Advanced)

1. **Daily/Intraday Aggregates (Bars)**
   - Endpoint: `/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from}/{to}`
   - Access: Full historical and real-time data
   - Used for: ADV calculations, price history, volatility metrics
   - Status: **FULLY OPERATIONAL**

2. **Active Tickers List**
   - Endpoint: `/v3/reference/tickers`
   - Access: All active US stocks
   - Limitations: Does NOT return market cap in list view
   - Status: **FULLY OPERATIONAL**
   - Pagination: returns `next_url` when more pages exist. Call `next_url` directly (append `apiKey` if missing) until exhausted.
   - Useful params:
     - `market=stocks`
     - `active=true`
     - `type=CS` (common stock only)
     - `exchange=XNYS|XNAS`
     - `order=ticker` and `sort=asc|desc` if needed
     - `limit=1000` (max per page)

3. **Ticker Details (with Market Cap)**
   - Endpoint: `/v3/reference/tickers/{ticker}`
   - Access: Detailed information including market cap
   - Used for: Getting market capitalization for universe selection
   - Status: **FULLY OPERATIONAL**
   - Response fields used:
     - `results.market_cap` (float)
     - `results.name`, `results.ticker`, `results.type`, `results.primary_exchange`

4. **News API**
   - Endpoint: `/v2/reference/news`
   - Access: Real-time news with your News add-on
   - Used for: Sentiment analysis and news-based signals
   - Status: **FULLY OPERATIONAL**

5. **Quotes/NBBO Data**
   - Endpoint: `/v3/quotes/{ticker}`
   - Access: Real-time and historical NBBO quotes
   - Used for: Spread analysis and liquidity metrics
   - Status: **FULLY OPERATIONAL**
   - Usage pattern (for median spread over a window):
     - Pull quotes for a bounded time window (e.g., prior 5 trading days during core hours)
     - Compute per-quote spread: `ask_price - bid_price`
     - Compute median spread in dollars and in bps: `10000 * spread / mid_price`
     - Parameters:
       - `timestamp.gte`, `timestamp.lte` (nanoseconds or ISO depending on client)
       - `limit` with pagination via `next_url`

6. **Reference Financials (vX)** 
   - Endpoint: `/vX/reference/financials`
   - Access: Full financial statements with filing dates
   - Used for: Earnings date exclusion (via filing_date field)
   - Returns: Quarterly/Annual reports with income statement, balance sheet, cash flow
   - Status: **FULLY OPERATIONAL** ✅
   - Practical approach for earnings exclusion:
     - Use most recent filing windows to identify upcoming earnings windows; exclude ±N days.

### 🔸 Premium Endpoints (Additional Subscription May Be Required)

1. **Indices API - Direct S&P 500 Constituents**
   - Ticker: `I:SPX` (S&P 500)
   - Constituents API is part of the Indices product family; availability depends on account setup.
   - If enabled, prefer this route to retrieve exactly 500 constituents.
   - If unavailable, use the Stocks-only approach documented below.

### ❌ Unavailable Endpoints (Not needed)

1. **Earnings Calendar (Benzinga)**
   - Endpoint: `/v1/partners/benzinga/earnings`
   - Status: Returns 404 - requires separate Benzinga add-on subscription
   - Alternative: Using vX financials filing_date instead (better!)

2. **Events API**
   - Endpoint: `/vX/reference/tickers/events`
   - Status: Returns 404 - may be experimental or require different plan
   - Alternative: Using vX financials for earnings dates

## System Architecture

### Universe Selection Process (Stocks-Only, No Indices API)

1. **Candidate Discovery (Polygon-only, paginated)**
   - Enumerate active common stocks on XNYS and XNAS using `/v3/reference/tickers` with `limit=1000`
   - Follow `next_url` pagination until all pages fetched
   - For each symbol, fetch `/v3/reference/tickers/{ticker}` to obtain `market_cap`
   - Keep symbols meeting S&P-500 scale threshold (empirically ≥ $8B–$10B)
   - Continue until ~600 symbols are found, then dedupe and trim to 500 by market cap

2. **ADV Prefiltering**
   - Use `/v2/aggs/ticker/{ticker}/range/{1}/{day}/{from}/{to}` for daily bars
   - ADV = average of `volume` over last N trading days (e.g., 20–60)
   - Prefer adjusted = true; handle partial sessions; drop illiquid names

3. **Final Selection**
   - Spreads via `/v3/quotes/{ticker}` over prior D days during core hours
   - Filters:
     - Provider prefilter: spread ≤ 50 bps, dollar spread ≤ $1.00 (sanity)
     - Selector strict: spread ≤ 5 bps; ADV ≥ $50M; ATR% within 1–5%
   - Sector balancing based on `results.sic_code` or sector if present; otherwise, maintain diversity by distribution guards
   - Earnings exclusion via vX financials filing calendar ±N days
   - Deterministic ordering: SHA-256 hash of date window + symbol to avoid alphabet bias

### Rate Limiting, Retries, and Performance

- Polygon returns HTTP 429 when rate limits hit. Implement exponential backoff: e.g., 0.5s, 1s, 2s, 4s and cap.
- Use connection reuse and bounded concurrency (5–10 workers) for details/quotes.
- Respect `next_url` pagination; do not guess page numbers.
- Cache intermediate artifacts (universe list with timestamp) for 24 hours to conserve calls.
- Avoid redundant calls by short-circuiting when the target S&P500-sized pool is satisfied.

Recommended retry pseudocode:
```
for attempt in range(max_attempts):
    try:
        return http.get_json(url, params)
    except TooManyRequests:
        time.sleep(base * 2**attempt)
```

## API Key Configuration

The Polygon API key is stored in the `.env` file:
```
POLYGON_API_KEY=your_api_key_here
```

Python scripts load it via `python-dotenv`. In PowerShell, ensure:
```
$env:PYTHONPATH=(Get-Location).Path
```

## Key Integration Points

1. **PolygonClient** (`services/polygon_client.py`)
   - Main interface to Polygon API
   - Handles authentication and HTTP requests
   - Implements reference tickers, ticker details, aggregates, quotes
   - Pagination helper via `next_url` (callers handle loop)

2. **ActiveUniverseProvider** (`utils/active_universe_provider.py`)
   - Orchestrates discovery using Stocks endpoints only (no Wikipedia, no hardcoded lists in production)
   - Uses paginated tickers + market-cap verification, stops at ~600, trims to 500
   - Batches detail calls conservatively to avoid 429s

3. **UniverseSelector** (`utils/universe_selector.py`)
   - Performs detailed symbol analysis
   - Calculates metrics (ADV, ATR%, spreads)
   - Applies selection criteria and ranking
   - Deterministic spread evaluation order to prevent alphabet bias

4. **QuotesClient** (`services/quotes_client.py`)
   - Specialized client for NBBO/quotes data
   - Calculates spread metrics
   - Handles quote data aggregation

## Data Quality Principles

1. **100% Real Data**: No mock data or simulations
2. **Point-in-Time Accuracy**: Historical data used as it was available
3. **Graceful Degradation**: If an endpoint fails, system continues with available data
4. **Validation**: All data validated before use

Additional enforcement:
- No fallbacks to external index lists; rely on Polygon-only flow unless Indices API is explicitly enabled.
- No hardcoded constituents in production universe generation.

## Troubleshooting

### Common Issues

1. **Empty Universe**
   - Check API key is set in `.env`
   - Verify internet connectivity
   - Check rate limits haven't been exceeded (HTTP 429)
   - Ensure `active=true`, `type=CS`, and exchange filters are correct

2. **Slow Performance**
   - Reduce batch size or concurrency
   - Confirm pagination is handled via `next_url` (no redundant first-page re-requests)
   - Cache candidates for 24 hours

3. **Missing Data**
   - Some endpoints (e.g., Indices constituents) may require add-ons
   - Check Polygon status page for outages
   - Verify symbol is active and on supported exchanges

4. **Alphabet Bias (A-bias)**
   - Cause: Taking first `limit` from `/v3/reference/tickers` without pagination
   - Fix: Use pagination and deterministic processing order; never truncate to first page

5. **Spreads too wide**
   - Cause: Including extended hours quotes or illiquid names
   - Fix: Restrict to core hours; apply prefilter at 50 bps in provider, 5 bps in selector

## Future Enhancements

1. **Real-time Updates**: Add WebSocket support for live data
2. **Options Data**: Extend to options market data if needed
3. **Enhanced Financials**: Use vX financials for fundamental analysis beyond earnings
4. **International Markets**: Extend to global exchanges if needed

5. **Indices API (if enabled in account)**: Replace market-cap filter with direct constituents retrieval for exact 500 names.

## Support

- Polygon Documentation: https://polygon.io/docs
- API Status: https://status.polygon.io/
- Support: support@polygon.io

## Version History

- v1.0: Initial integration with basic aggregates and tickers
- v2.0: Added market cap discovery via ticker details
- v2.1: Enhanced batching and rate limiting
- v2.2: Added smart universe builder with ADV prefiltering
- v2.3: Integrated vX financials for earnings date exclusion
- v2.4: Documented strict Polygon-only S&P 500 discovery with pagination; removed reliance on external lists; added Indices API guidance

## Appendix: Quick Endpoint Cheatsheet

- List stocks (paginated): `/v3/reference/tickers?market=stocks&active=true&type=CS&exchange=XNYS&limit=1000`
- Next page: use `next_url` from previous response (append `apiKey` if absent)
- Ticker details (market cap): `/v3/reference/tickers/{ticker}`
- Daily aggregates: `/v2/aggs/ticker/{ticker}/range/1/day/{from}/{to}?adjusted=true&sort=asc&limit=50000`
- Quotes (NBBO): `/v3/quotes/{ticker}?timestamp.gte=...&timestamp.lte=...&limit=50000`

## HOWTO: Fetch S&P 500 With Stocks Advanced (No Indices API)

Prerequisites
- Set your API key as an environment variable: `POLYGON_API_KEY`

### Curl examples

- First page of NYSE common stocks (1000 max):
```
curl -s "https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&type=CS&exchange=XNYS&limit=1000&apiKey=${POLYGON_API_KEY}"
```

- Follow pagination using `next_url` from the response (append `apiKey` if missing):
```
# Pseudocode steps
# 1) Save next_url from previous response
# 2) If next_url does not contain apiKey, append `?apiKey=${POLYGON_API_KEY}` or `&apiKey=${POLYGON_API_KEY}`
curl -s "https://api.polygon.io/v3/reference/tickers?....&apiKey=${POLYGON_API_KEY}"
curl -s "${NEXT_URL}&apiKey=${POLYGON_API_KEY}"
```

- Ticker details (includes market_cap):
```
curl -s "https://api.polygon.io/v3/reference/tickers/AAPL?apiKey=${POLYGON_API_KEY}"
```

### Python: End‑to‑end Stocks‑Only S&P 500 Discovery
Fetch all NYSE/NASDAQ common stocks with pagination, verify market caps, then trim to 500 largest.

```
import os, time, requests
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = os.environ.get("POLYGON_API_KEY", "")
BASE = "https://api.polygon.io"

def get_json(url, params=None):
    for attempt in range(5):
        r = requests.get(url, params=(params or {}))
        if r.status_code == 429:
            time.sleep(0.5 * (2 ** attempt))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("rate limited")

def list_exchange_symbols(exchange):
    url = f"{BASE}/v3/reference/tickers"
    params = {
        "market": "stocks",
        "active": "true",
        "type": "CS",
        "exchange": exchange,
        "limit": 1000,
        "apiKey": API_KEY,
    }
    syms = []
    next_url = None
    while True:
        data = get_json(next_url or url, None if next_url else params)
        results = data.get("results", [])
        for t in results:
            s = t.get("ticker")
            if s and isinstance(s, str) and "/" not in s and "-" not in s:
                syms.append(s)
        next_url = data.get("next_url")
        if not next_url:
            break
        if "apiKey=" not in next_url:
            next_url += ("&" if "?" in next_url else "?") + f"apiKey={API_KEY}"
    return syms

def get_market_cap(symbol):
    url = f"{BASE}/v3/reference/tickers/{symbol}"
    data = get_json(url, {"apiKey": API_KEY})
    res = data.get("results") or {}
    return float(res.get("market_cap") or 0.0)

def discover_sp500_like(limit=500, cap_threshold=8_000_000_000):
    all_syms = []
    for ex in ("XNYS", "XNAS"):
        all_syms.extend(list_exchange_symbols(ex))
    # Deduplicate preserving order
    seen, unique_syms = set(), []
    for s in all_syms:
        if s not in seen:
            seen.add(s)
            unique_syms.append(s)

    caps = {}
    with ThreadPoolExecutor(max_workers=10) as pool:
        fut = {pool.submit(get_market_cap, s): s for s in unique_syms}
        for f in as_completed(fut):
            s = fut[f]
            try:
                mc = f.result()
                if mc >= cap_threshold:
                    caps[s] = mc
            except Exception:
                pass

    # Top 500 by market cap
    ordered = sorted(caps.items(), key=lambda kv: kv[1], reverse=True)[:limit]
    symbols = [s for s, _ in ordered]
    dist = Counter(s[0] for s in symbols)
    print(f"Selected {len(symbols)} symbols. Letter distribution: {dict(dist)}")
    return symbols

if __name__ == "__main__":
    syms = discover_sp500_like()
    print(syms[:20])
```

Notes
- This flow matches Stocks Advanced capabilities. If your account later enables the Indices product, prefer the dedicated constituents endpoint for `I:SPX`.
- Keep spread prefiltering at 50 bps in the provider, strict 5 bps in the selector.
