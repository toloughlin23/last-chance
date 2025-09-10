import math
import numpy as np
from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit


class _Sentiment:
    def __init__(self, s, conf, vol, impact=0.4):
        self.overall_sentiment = s
        self.confidence_level = conf
        self.market_impact_estimate = impact
        self.news_volume = vol


class _Market:
    def __init__(self, pm, vol, vr):
        self.price_momentum = pm
        self.volatility = vol
        self.volume_ratio = vr


class _Enriched:
    def __init__(self, s, conf, vol, pm, vlt, vr, dq=0.8):
        self.sentiment_analysis = _Sentiment(s, conf, vol)
        self.data_quality_score = dq
        self.market_data = _Market(pm, vlt, vr)


def test_neural_day2_features_and_bounds():
    bandit = OptimizedInstitutionalNeuralBandit()
    data = _Enriched(0.2, 0.7, 12, 0.01, 0.02, 1.0)

    feats = bandit.extract_neural_features(data)
    assert len(feats) == 15

    bandit.add_arm('buy_signal')
    conf = bandit.get_confidence('buy_signal', data)
    assert 0.40 <= conf <= 0.95


def test_neural_day2_variation():
    bandit = OptimizedInstitutionalNeuralBandit()
    bandit.add_arm('buy_signal')

    d1 = _Enriched(0.1, 0.5, 8, 0.00, 0.01, 0.7)
    d2 = _Enriched(0.7, 0.95, 20, 0.03, 0.05, 1.6)

    c1 = bandit.get_confidence('buy_signal', d1)
    c2 = bandit.get_confidence('buy_signal', d2)

    assert abs(c2 - c1) >= 0.08


def test_neural_day2_learning_reduces_loss():
    bandit = OptimizedInstitutionalNeuralBandit()
    bandit.add_arm('buy_signal')

    data = _Enriched(0.3, 0.8, 15, 0.02, 0.03, 1.2)
    feats = bandit.extract_neural_features(data)

    # prediction before update
    pred_before = bandit._forward_pass('buy_signal', feats)
    loss_before = (pred_before - 1.0) ** 2

    # perform update toward reward 1.0
    bandit.update_arm('buy_signal', data, reward=1.0)

    pred_after = bandit._forward_pass('buy_signal', feats)
    loss_after = (pred_after - 1.0) ** 2

    assert loss_after <= loss_before

