import numpy as np
from systems.personality import AuthenticPersonalitySystem, PersonalityProfile
from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit
from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV


class _Sent:
    def __init__(self, s, c, v):
        self.overall_sentiment = s
        self.confidence_level = c
        self.market_impact_estimate = 0.4
        self.news_volume = v


class _Mkt:
    def __init__(self, pm, vol, vr):
        self.price_momentum = pm
        self.volatility = vol
        self.volume_ratio = vr
        self.price = 100.0
        self.high = 105.0
        self.low = 95.0


class _Data:
    def __init__(self, s, c, v, pm, vol, vr, dq=0.8):
        self.sentiment_analysis = _Sent(s, c, v)
        self.data_quality_score = dq
        self.market_data = _Mkt(pm, vol, vr)


def test_personality_affects_linucb_confidence():
    base = AuthenticPersonalitySystem(PersonalityProfile(0.2, 0.2, 0.2))
    high = AuthenticPersonalitySystem(PersonalityProfile(0.9, 0.9, 0.9))

    d = _Data(0.3, 0.8, 12, 0.02, 0.03, 1.1)

    b1 = OptimizedInstitutionalLinUCB(personality=base)
    arm = b1.select_arm(d)
    c_low = b1.get_confidence_for_context(arm, d)

    b2 = OptimizedInstitutionalLinUCB(personality=high)
    arm2 = b2.select_arm(d)
    c_high = b2.get_confidence_for_context(arm2, d)

    assert c_high != c_low
    assert 0.45 <= c_low <= 0.90 and 0.45 <= c_high <= 0.90


def test_personality_affects_neural_confidence():
    base = AuthenticPersonalitySystem(PersonalityProfile(0.2, 0.2, 0.2))
    high = AuthenticPersonalitySystem(PersonalityProfile(0.9, 0.9, 0.9))

    d = _Data(0.3, 0.8, 12, 0.02, 0.03, 1.1)

    n1 = OptimizedInstitutionalNeuralBandit(personality=base)
    n1.add_arm('buy_signal')
    c1 = n1.get_confidence('buy_signal', d)

    n2 = OptimizedInstitutionalNeuralBandit(personality=high)
    n2.add_arm('buy_signal')
    c2 = n2.get_confidence('buy_signal', d)

    assert c1 != c2
    assert 0.40 <= c1 <= 0.95 and 0.40 <= c2 <= 0.95


def test_personality_affects_ucbv_confidence():
    base = AuthenticPersonalitySystem(PersonalityProfile(0.2, 0.2, 0.2))
    high = AuthenticPersonalitySystem(PersonalityProfile(0.9, 0.9, 0.9))

    def mk(price, pc, hi, lo, vol, vwap):
        return {
            'status': 'OK',
            'results': {'p': price, 's': vol, 't': 0, 'c': [1], 'o': pc, 'h': hi, 'l': lo, 'v': vol, 'vw': vwap},
            'prev_close': pc, 'high': hi, 'low': lo, 'vwap': vwap,
        }

    data = mk(100.0, 100.0, 101.0, 99.0, 20000, 100.0)

    u1 = OptimizedInstitutionalUCBV(personality=base)
    a1, c1 = u1.select_action(data)

    u2 = OptimizedInstitutionalUCBV(personality=high)
    a2, c2 = u2.select_action(data)

    assert c1 != c2
    assert 0.40 <= c1 <= 0.85 and 0.40 <= c2 <= 0.85

