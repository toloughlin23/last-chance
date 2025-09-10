# Post‑Launch Tuning Checklist

Use this after the first trading sessions (paper or live) to tighten behavior.

## 1) Universe selector thresholds
- min_price (default: 5.0)
- min_atr_pct (default: 1.0%)
- target_size (default: 120; range 80–150)
- Action: If too few names, relax ATR% (e.g., 1.0% → 0.7%); if too many, raise ATR% or reduce target_size.

## 2) NBBO spread gates (liquidity/quality)
- spread_filter_enabled (default: ON)
- spread_max_dollars (default: $0.02)
- spread_max_bps (default: 3 bps)
- spread_lookback_days (default: 5)
- core_hours_only (default: ON)
- Action: If fills/slippage are poor, tighten (e.g., $0.015 or 2 bps). If universe is too small, relax slightly ($0.03 or 5 bps).

## 3) News booster at market open
- news_booster_enabled (default: OFF unless strategy needs it)
- news_booster_threshold (default: 0.2)
- Overnight priority list used once at open; filtered by |score| ≥ threshold
- Action: Increase threshold (0.2 → 0.3) to reduce noise; decrease to capture more names.

## 4) Open activity gates (momentum profile)
- 5‑min relative volume ≥ 3× (vs 30‑day median 5‑min volume)
- Gap magnitude ≥ 2% (open vs prior close)
- Opening range ≥ 30–40% of 20‑day ATR
- Action: Raise thresholds if too many signals; lower if too few.

## 5) Batching and retries (rate‑limit hygiene)
- batch_size (default: 50)
- max_retries (default: 2)
- retry_backoff (default: 0.5s exponential)
- Action: Adjust to match API limits and latencies observed in logs.

## 6) Market hours & pre‑open window
- market_hours_only (default: ON)
- preopen_build_minutes (default: 5)
- Action: Extend window (e.g., 10–15min) if news backlog is heavy.

## 7) Execution promotion (paper → live)
- Verify pipeline_log.csv stability (coverage, errors=0, retries low)
- Confirm Alpaca paper orders behave as expected
- Enable live only after satisfactory dry‑runs and risk checks

## 8) Alerts & coverage metrics
- Per‑symbol success/fail and retry counts
- Repeated misses (top offenders)
- Optional notifications on excessive retries/failures

## 9) S&P 500 source integration
- Store/refresh candidate list daily from a reliable source
- Ensure symbol changes (additions/deletions) propagate to the selector

## 10) Backtest harness (1‑year)
- Run 1‑year Polygon backtest over the selected universe
- Metrics: P&L, Sharpe, max drawdown, win rate, slippage proxy
- Compare profiles (momentum vs mean‑reversion) and thresholds

---

Notes
- All selection/booster features are real‑data and toggleable per strategy.
- Use the defaults first; tune only after reviewing logs and fills.

