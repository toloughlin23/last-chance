from __future__ import annotations

from typing import Dict, List

from core.controller_hub.hub import Hub
from core.controller_hub.messages import DecisionMessage, MetricsMessage
from learning.phase1_learning_loop import Phase1LearningLoop


class Phase1Controller:
    """Controller orchestrating the learning loop and publishing messages to the Hub."""

    def __init__(self, symbols: List[str], hub: Hub | None = None) -> None:
        self.symbols = symbols
        self.hub = hub or Hub()
        self.learning = Phase1LearningLoop(symbols=symbols, learning_rate=0.01)

        # Channels
        self.channel_decisions = "decisions"
        self.channel_metrics = "metrics"

        # Ensure channels exist
        self.hub.ensure_channel(self.channel_decisions)
        self.hub.ensure_channel(self.channel_metrics)

    def run_cycle_and_publish(self, lookback_days: int = 5) -> Dict[str, float]:
        """Run a single learning cycle and publish decisions + metrics."""
        metrics = self.learning.run_learning_cycle(lookback_days=lookback_days, execute_trades=False)

        # Publish per-symbol decisions with confidences
        # We reuse the last computed decisions by recomputing in a lightweight way per symbol
        # to generate DecisionMessage entries. This avoids modifying the learning loop's internals.
        market_data = self.learning._fetch_market_data(lookback_days)
        for symbol, data in market_data.items():
            enriched = self.learning._safe_build_enriched(data) if hasattr(self.learning, "_safe_build_enriched") else None
            if enriched is None:
                from services.feature_builder import build_enriched_from_aggs
                enriched = build_enriched_from_aggs(data)

            decisions = self.learning._get_algorithm_decisions(symbol, enriched)
            for alg_name, (decision, avg_conf, all_conf) in decisions.items():
                msg = DecisionMessage(
                    symbol=symbol,
                    algorithm=alg_name,
                    decision=decision,
                    confidence=float(avg_conf),
                    all_confidences=[float(x) for x in all_conf],
                    metadata={}
                )
                self.hub.publish(self.channel_decisions, msg, block=True)

        # Publish metrics
        m = MetricsMessage(
            diversity_overall=float(metrics.get("overall_variance", 0.0)),
            diversity_cross_algorithm=float(metrics.get("cross_algorithm_variance", 0.0)),
            coefficient_of_variation=float(metrics.get("coefficient_of_variation", 0.0)),
            total_pnl=float(self.learning.metrics.total_pnl),
            learning_rate=float(self.learning.learning_rate),
            extra={}
        )
        self.hub.publish(self.channel_metrics, m, block=True)

        return metrics




