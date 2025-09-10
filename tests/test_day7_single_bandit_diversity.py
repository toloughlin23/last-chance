import os
import pytest

from services.polygon_client import PolygonClient
from services.feature_builder import build_enriched_from_aggs
from CORE_SUPER_BANDITS.optimized_linucb_institutional import OptimizedInstitutionalLinUCB
from CORE_SUPER_BANDITS.optimized_neural_bandit_institutional import OptimizedInstitutionalNeuralBandit
from CORE_SUPER_BANDITS.optimized_ucbv_institutional import OptimizedInstitutionalUCBV


@pytest.mark.integration
def test_day7_single_bandit_diversity_with_real_polygon_aggs():
    if not os.getenv("POLYGON_API_KEY"):
        pytest.skip("POLYGON_API_KEY not set; skipping Day 7 diversity test.")

    client = PolygonClient()
    aggs = client.get_aggs("AAPL", 1, "day", "2023-01-03", "2023-01-20", limit=10, adjusted=True, sort="asc")
    enriched = build_enriched_from_aggs(aggs)

    lin = OptimizedInstitutionalLinUCB()
    neu = OptimizedInstitutionalNeuralBandit()
    ucv = OptimizedInstitutionalUCBV()

    arm_lin = lin.select_arm(enriched)
    conf_lin = lin.get_confidence_for_context(arm_lin, enriched)

    neu.add_arm('buy_signal')
    conf_neu = neu.get_confidence('buy_signal', enriched)

    polygon_like = {
        'status': 'OK',
        'results': {'p': getattr(enriched.market_data, 'price', 100.0), 's': int(getattr(enriched.market_data, 'volume', 1000000)), 't': 0, 'c': [1], 'o': 0, 'h': 0, 'l': 0, 'v': int(getattr(enriched.market_data, 'volume', 1000000)), 'vw': getattr(enriched.market_data, 'price', 100.0)}
    }
    action_ucv, conf_ucv = ucv.select_action(polygon_like)

    # Diversity: at least two confidences should differ by >= 5%
    values = [conf_lin, conf_neu, conf_ucv]
    assert max(values) - min(values) >= 0.05

