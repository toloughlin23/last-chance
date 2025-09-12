import numpy as np
from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB


class _Sentiment:
    def __init__(self, s, conf, vol):
        self.overall_sentiment = s
        self.confidence_level = conf
        self.market_impact_estimate = 0.4
        self.news_volume = vol


class _Market:
    def __init__(self, pm, vol, vr):
        self.price_momentum = pm
        self.volatility = vol
        self.volume_ratio = vr
        self.price = 100.0
        self.high = 105.0
        self.low = 95.0


class _Enriched:
    def __init__(self, s, conf, vol, pm, vlt, vr):
        self.sentiment_analysis = _Sentiment(s, conf, vol)
        self.data_quality_score = 0.8
        self.market_data = _Market(pm, vlt, vr)


def test_linucb_day1_foundation_confidence_bounds_and_features():
    bandit = OptimizedInstitutionalLinUCB()

    data = _Enriched(0.2, 0.7, 10, 0.01, 0.02, 1.0)
    ctx = bandit.extract_enhanced_market_features(data)
    assert len(ctx) == 15

    arm = bandit.select_arm(data)
    conf = bandit.get_confidence_for_context(arm, data)
    assert 0.45 <= conf <= 0.90


def test_linucb_day1_variation_over_inputs():
    bandit = OptimizedInstitutionalLinUCB()

    d1 = _Enriched(0.1, 0.6, 8, 0.00, 0.02, 0.8)
    d2 = _Enriched(0.6, 0.9, 20, 0.03, 0.05, 1.5)

    a1 = bandit.select_arm(d1)
    c1 = bandit.get_confidence_for_context(a1, d1)

    a2 = bandit.select_arm(d2)
    c2 = bandit.get_confidence_for_context(a2, d2)

    assert abs(c2 - c1) >= 0.05

