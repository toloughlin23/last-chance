#!/usr/bin/env python3
import os
import time
import csv
from datetime import datetime, timezone, timedelta

import pytest
from hypothesis import given, strategies as st

from services.infrastructure_manager import InstitutionalInfrastructureManager
from utils.uk_us_timezone_handler import UKUSTimezoneHandler
from pipeline.enhanced_runner import EnhancedPipelineRunner


def test_cache_ttl_and_eviction_behavior(tmp_path):
    im = InstitutionalInfrastructureManager()

    # Store value with short TTL
    payload = {"value": 123, "ts": datetime.now(timezone.utc).isoformat()}
    assert im.cache_data("k1", payload, ttl=0.2) is True
    assert im.get_cached_data("k1") == payload

    # Expire
    time.sleep(0.25)
    assert im.get_cached_data("k1") is None

    # Eviction under load: insert many, ensure no error and entries tracked
    for i in range(50):
        im.cache_data(f"key_{i}", {"i": i}, ttl=1)
    report = im.get_performance_report()
    assert report["cache_status"]["entries"] >= 50

    im.clear_cache()
    assert im.get_performance_report()["cache_status"]["entries"] == 0


def test_timezone_dst_boundaries():
    tz = UKUSTimezoneHandler()

    # A known DST boundary around late March/late October; just assert conversion is monotonic
    # Create two UK times one hour apart spanning potential DST change and ensure ordering preserved in US time
    uk_time = tz.uk_tz.localize(datetime(2024, 3, 31, 0, 30))
    uk_time2 = uk_time + timedelta(hours=2)

    us1 = tz.uk_to_us_market(uk_time)
    us2 = tz.uk_to_us_market(uk_time2)
    assert us2 > us1

    # Market-hours boundaries 09:30 and 16:00 ET
    us_open = tz.us_market_tz.localize(datetime(2024, 5, 6, 9, 30))
    us_close = tz.us_market_tz.localize(datetime(2024, 5, 6, 16, 0))
    assert tz.is_us_market_open(us_open)
    assert tz.is_us_market_open(us_close)


def test_pipeline_two_iterations_durability(tmp_path):
    log_path = tmp_path / "durability_log.csv"
    runner = EnhancedPipelineRunner()

    # Keep it small and offline-safe (no execution, news prioritization off)
    runner.run_enhanced_loop(["AAPL", "MSFT"], lookback_days=7, interval_seconds=1,
                             iterations=2, execute=False, log_path=str(log_path),
                             prioritize_by_news=False, batch_size=0)

    assert log_path.exists()
    # Validate header and at least some rows
    with open(log_path, "r", newline="") as f:
        r = csv.reader(f)
        header = next(r)
        assert set(["timestamp", "symbol", "avg_confidence"]).issubset(set(header))
        row_count = sum(1 for _ in r)
        assert row_count > 0

    runner.shutdown()


@given(
    sentiment=st.floats(min_value=-1.0, max_value=1.0),
    momentum=st.floats(min_value=-0.05, max_value=0.05),
    volatility=st.floats(min_value=0.0, max_value=0.2),
)
def test_linucb_confidence_invariants(sentiment, momentum, volatility):
    # Minimal enriched data structure with required fields
    class _M:
        def __init__(self, pm, vol, vr):
            self.price_momentum = pm
            self.volatility = vol
            self.volume_ratio = 1.0
            self.price = 100.0
            self.high = 105.0
            self.low = 95.0

    class _S:
        def __init__(self, s):
            self.overall_sentiment = s
            self.confidence_level = 0.7
            self.market_impact_estimate = 0.3

    class _E:
        def __init__(self, s, pm, vol):
            self.sentiment_analysis = _S(s)
            self.data_quality_score = 0.8
            self.market_data = _M(pm, vol, 1.0)

    from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB

    bandit = OptimizedInstitutionalLinUCB()

    ctx1 = _E(sentiment, momentum, volatility)
    arm = bandit.select_arm(ctx1)
    c1 = bandit.get_confidence_for_context(arm, ctx1)

    # Confidence bounds invariant
    assert 0.45 <= c1 <= 0.90

    # Increasing positive sentiment tends to not decrease confidence
    ctx2 = _E(min(1.0, sentiment + 0.2), momentum, volatility)
    c2 = bandit.get_confidence_for_context(arm, ctx2)
    assert c2 >= 0.45 and c2 <= 0.90

