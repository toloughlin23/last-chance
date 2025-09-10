import math
import numpy as np
from datetime import datetime
from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV


def make_polygon(price: float, prev_close: float, high: float, low: float, volume: int, vwap: float):
    return {
        'status': 'OK',
        'results': {
            'p': price,
            's': volume,
            't': int(datetime.now().timestamp() * 1000),
            'c': [1],
            'o': prev_close,
            'h': high,
            'l': low,
            'v': volume,
            'vw': vwap,
        },
        'prev_close': prev_close,
        'high': high,
        'low': low,
        'vwap': vwap,
    }


def test_ucbv_features_and_bounds():
    ucbv = OptimizedInstitutionalUCBV()
    data = make_polygon(price=100.0, prev_close=99.5, high=101.0, low=99.0, volume=20000, vwap=100.0)

    feats = ucbv.extract_features_from_polygon(data)
    assert len(feats) == 15

    action, conf = ucbv.select_action(data)
    assert 0.40 <= conf <= 0.85


def test_ucbv_variation_high_vs_low_variance():
    ucbv = OptimizedInstitutionalUCBV()
    low_var = make_polygon(price=100.0, prev_close=100.0, high=100.4, low=99.6, volume=15000, vwap=100.0)
    high_var = make_polygon(price=100.0, prev_close=100.0, high=105.0, low=95.0, volume=30000, vwap=100.0)

    a1, c1 = ucbv.select_action(low_var)
    a2, c2 = ucbv.select_action(high_var)

    assert abs(c2 - c1) >= 0.05


def test_ucbv_update_changes_state():
    ucbv = OptimizedInstitutionalUCBV()
    data = make_polygon(price=100.0, prev_close=100.0, high=101.0, low=99.0, volume=25000, vwap=100.0)

    action, conf = ucbv.select_action(data)
    before_pulls = ucbv.arms[action]['pulls']

    feats = ucbv.extract_features_from_polygon(data)
    alpaca_data = {'order_id': 'test123', 'holding_time': 300}
    ucbv.update_with_real_pnl(action, feats, real_pnl=50.0, alpaca_data=alpaca_data)

    after_pulls = ucbv.arms[action]['pulls']
    assert after_pulls == before_pulls + 1
    assert ucbv.arms[action]['variance'] >= 0.001


