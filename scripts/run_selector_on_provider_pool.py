#!/usr/bin/env python3
"""
Run selector on provider's full candidate pool (no caching shortcut).

Steps:
1) Discover & rank S&P 500 candidates (provider) with min_market_cap=100M
2) Run UniverseSelector on those candidates with strict spread=5 bps
3) Print counts and sample symbols

Data source: 100% real Polygon via existing clients (.env POLYGON_API_KEY required)
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import List

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    from utils.active_universe_provider import ActiveUniverseProvider
    from utils.universe_selector import UniverseSelector

    analysis_days = 60
    ed = date.today()
    sd = ed - timedelta(days=analysis_days)

    provider = ActiveUniverseProvider()

    print("🚀 Discovering and ranking provider candidates...")
    candidates: List[str] = provider._discover_and_rank_candidates(
        min_market_cap=100_000_000,  # $100M generous provider cutoff
        analysis_days=analysis_days,
        start_date=sd,
        end_date=ed,
        max_candidates=300,          # allow up to 300 from provider
        batch_size=10,
    )
    print(f"📊 Provider ranked candidates: {len(candidates)}")
    if not candidates:
        print("⚠️ No candidates found from provider.")
        return

    sector_classifier, sector_index_weights = provider._build_sector_classifier_and_weights(candidates)

    selector = UniverseSelector()
    print("🎯 Running selector on provider pool...")
    picks = selector.select_universe(
        candidates=candidates,
        start_date=sd.isoformat(),
        end_date=ed.isoformat(),
        target_size=120,
        target_max_size=150,
        allow_expand_above_target=True,
        expand_margin=0.95,
        min_price=10.0,
        min_atr_pct=0.01,
        max_atr_pct=0.05,
        adv_min_dollar=50_000_000.0,
        spread_filter_enabled=True,
        spread_max_dollars=0.02,
        spread_max_bps=5.0,
        spread_lookback_days=5,
        spread_core_hours_only=True,
        sector_classifier=sector_classifier,
        sector_index_weights=sector_index_weights,
    )

    print(f"✅ Selector picks: {len(picks)}")
    print("Top 20:", picks[:20])


if __name__ == "__main__":
    main()



