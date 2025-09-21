#!/usr/bin/env python3

from core.controller_hub import Hub, Phase1Controller


def main() -> None:
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
    hub = Hub()

    # Example subscriptions
    def on_decision(msg):
        try:
            print(f"DECISION {msg.symbol} {msg.algorithm} {msg.decision} conf={msg.confidence:.3f}")
        except Exception:
            pass

    def on_metrics(msg):
        try:
            print(
                f"METRICS var={msg.diversity_overall:.4f} cross={msg.diversity_cross_algorithm:.4f} cv={msg.coefficient_of_variation:.4f} lr={msg.learning_rate:.4f} pnl={msg.total_pnl:.2f}"
            )
        except Exception:
            pass

    hub.subscribe("decisions", on_decision)
    hub.subscribe("metrics", on_metrics)

    controller = Phase1Controller(symbols=symbols, hub=hub)
    controller.run_cycle_and_publish(lookback_days=3)


if __name__ == "__main__":
    main()

