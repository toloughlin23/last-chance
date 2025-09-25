#!/usr/bin/env python3
"""
🚀 HISTORICAL TRAINING RUNNER
=============================
Easy-to-use script for running historical training
"""

import argparse
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.historical_training_module import HistoricalTrainingModule, TrainingConfig
from training.training_config import (
    TRAINING_BEST_PRACTICES,
    TrainingPresets,
    TrainingValidation,
)


def main():
    parser = argparse.ArgumentParser(
        description="Run historical training for Super Bandits system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=TRAINING_BEST_PRACTICES,
    )

    parser.add_argument(
        "--preset",
        choices=["3month", "6month", "1year", "2year", "test"],
        default="1year",
        help="Training duration preset (default: 1year)",
    )

    parser.add_argument(
        "--export-path",
        default="training/exports/trained_models.json",
        help="Path to export trained models",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show configuration without running training",
    )

    args = parser.parse_args()

    # Get preset configuration
    preset_map = {
        "3month": TrainingPresets.three_month_training,
        "6month": TrainingPresets.six_month_training,
        "1year": TrainingPresets.one_year_training,
        "2year": TrainingPresets.two_year_training,
        "test": TrainingPresets.quick_test_training,
    }

    config_dict = preset_map[args.preset]()

    # Create training config
    config = TrainingConfig(**config_dict)

    # Display configuration
    training_logger.info("🎯 HISTORICAL TRAINING CONFIGURATION", operation="run_historical_training")
    training_logger.info("=" * 50, operation="run_historical_training")
    training_logger.info(f"Preset: {args.preset}", operation="run_historical_training")
    training_logger.info(
        f"Training period: {config.training_start_date.date(, operation="run_historical_training")} to {config.training_end_date.date()}"
    )
    training_logger.info(
        f"Duration: {(config.training_end_date - config.training_start_date, operation="run_historical_training").days} days"
    )
    training_logger.info(f"Symbols: {len(config.symbols)} stocks", operation="run_historical_training")
    training_logger.info(f"Lookback window: {config.lookback_window} days", operation="run_historical_training")
    training_logger.info(
        f"Zero forward-looking bias: {'ENABLED' if config.validate_no_future_data else 'DISABLED'}"
    , operation="run_historical_training")
    training_logger.info(f"Export path: {args.export_path}", operation="run_historical_training")
    training_logger.info("=" * 50, operation="run_historical_training")

    # Validate configuration
    training_logger.info("\n🔍 VALIDATING CONFIGURATION...", operation="run_historical_training")

    if not TrainingValidation.validate_no_overlap_with_live(config.training_end_date):
        training_logger.info("⚠️ WARNING: Training end date is in the future!", operation="run_historical_training")

    if not TrainingValidation.validate_sufficient_data(
        config.training_start_date, config.training_end_date
    ):
        training_logger.info("⚠️ WARNING: Less than 60 trading days of data!", operation="run_historical_training")

    if not TrainingValidation.validate_symbol_coverage(config.symbols):
        training_logger.info("⚠️ WARNING: Less than 5 symbols - may not achieve sufficient diversity!", operation="run_historical_training")

    if args.dry_run:
        training_logger.info("\n✅ DRY RUN - Configuration validated, no training performed", operation="run_historical_training")
        return

    # Confirm before starting
    training_logger.info("\n" + "=" * 50, operation="run_historical_training")
    response = input("📊 Start training? This may take several minutes. (y/N): ")
    if response.lower() != "y":
        training_logger.info("❌ Training cancelled", operation="run_historical_training")
        return

    # Create training module
    training_logger.info("\n🚀 STARTING HISTORICAL TRAINING...", operation="run_historical_training")
    trainer = HistoricalTrainingModule(config)

    try:
        # Run training
        results = trainer.run_full_training()

        # Display results
        training_logger.info("\n" + "=" * 50, operation="run_historical_training")
        training_logger.info("📊 TRAINING COMPLETE!", operation="run_historical_training")
        training_logger.info("=" * 50, operation="run_historical_training")
        training_logger.info(f"Total trades executed: {results['total_trades']:,}", operation="run_historical_training")
        training_logger.info(f"Overall confidence variance: {results['overall_variance']:.6f}", operation="run_historical_training")
        training_logger.info(
            f"Diversity target achieved: {'✅ YES' if results['diversity_achieved'] else '❌ NO'}"
        , operation="run_historical_training")

        training_logger.info("\n📈 ALGORITHM PERFORMANCE:", operation="run_historical_training")
        for algo_name, performance in results["algorithm_performance"].items():
            training_logger.info(f"\n{algo_name.upper()}:", operation="run_historical_training")
            training_logger.info(f"  Total trades: {performance['total_trades']:,}", operation="run_historical_training")
            training_logger.info(f"  Average reward: {performance['avg_reward_bps']:.2f} basis points", operation="run_historical_training")
            training_logger.info(f"  Win rate: {performance['win_rate']:.2%}", operation="run_historical_training")
            training_logger.info(f"  Confidence variance: {performance['confidence_variance']:.6f}", operation="run_historical_training")
            training_logger.info(
                f"  Unique confidence values: {performance['unique_confidence_count']}"
            , operation="run_historical_training")
            training_logger.info(
                f"  Confidence range: [{performance['confidence_range'][0]:.4f}, {performance['confidence_range'][1]:.4f}]"
            , operation="run_historical_training")

        # Export models
        trainer.export_trained_models(args.export_path)
        training_logger.info(f"\n✅ Trained models exported to: {args.export_path}", operation="run_historical_training")

        # Save training summary (JSON-safe version)
        summary_path = args.export_path.replace(".json", "_summary.json")
        
        # Create JSON-safe version of results
        json_safe_results = {
            "total_trades": int(results["total_trades"]),
            "overall_variance": float(results["overall_variance"]),
            "diversity_achieved": bool(results["diversity_achieved"]),
            "algorithm_performance": {}
        }
        
        # Convert algorithm performance to JSON-safe format
        for algo_name, performance in results["algorithm_performance"].items():
            json_safe_results["algorithm_performance"][algo_name] = {
                "total_trades": int(performance["total_trades"]),
                "avg_reward_bps": float(performance["avg_reward_bps"]),
                "win_rate": float(performance["win_rate"]),
                "confidence_variance": float(performance["confidence_variance"]),
                "unique_confidence_count": int(performance["unique_confidence_count"]),
                "confidence_range": [
                    float(performance["confidence_range"][0]),
                    float(performance["confidence_range"][1])
                ]
            }
        
        with open(summary_path, "w") as f:
            json.dump(json_safe_results, f, indent=2)
        training_logger.info(f"📄 Training summary saved to: {summary_path}", operation="run_historical_training")

        # Next steps
        training_logger.info("\n🎯 NEXT STEPS:", operation="run_historical_training")
        training_logger.info("1. Review training summary for performance metrics", operation="run_historical_training")
        training_logger.info("2. Verify diversity variance is > 0.15", operation="run_historical_training")
        training_logger.info("3. Load trained models into live system when ready", operation="run_historical_training")
        training_logger.info("4. Run backtesting on out-of-authentic data sources", operation="run_historical_training")

        if results["diversity_achieved"]:
            training_logger.info("\n✅ DIVERSITY ACHIEVED! Algorithms are ready for live trading!", operation="run_historical_training")
        else:
            training_logger.info("\n⚠️ DIVERSITY NOT ACHIEVED - Consider:", operation="run_historical_training")
            training_logger.info("  - Training for a longer period", operation="run_historical_training")
            training_logger.info("  - Adding more diverse symbols", operation="run_historical_training")
            training_logger.info("  - Adjusting algorithm parameters", operation="run_historical_training")

    except Exception as e:
        training_logger.info(f"\n❌ Training failed: {e}", operation="run_historical_training")
        import traceback
from utils.enhanced_logging_system import training_logger

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
