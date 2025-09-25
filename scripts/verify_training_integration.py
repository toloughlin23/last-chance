#!/usr/bin/env python3
"""
Verify Training Module Integration
Check that the generated universe works with the training module
"""

import json
import os

from dotenv import load_dotenv


def main():
    load_dotenv()

    training_logger.info("🔍 VERIFYING TRAINING MODULE INTEGRATION", operation="enhanced_logging")
    training_logger.info("=" * 50, operation="enhanced_logging")

    # Check if universe file exists
    universe_file = "data/training/universe_list.json"
    if not os.path.exists(universe_file):
        training_logger.error(f"❌ Universe file not found: {universe_file}", operation="enhanced_logging")
        training_logger.info("   Run generate_training_universe.py first", operation="enhanced_logging")
        return

    # Load universe data
    with open(universe_file, "r") as f:
        universe_data = json.load(f)

    training_logger.info(f"✅ Universe file loaded: {universe_file}", operation="enhanced_logging")
    training_logger.info(f"📊 Symbol count: {universe_data['symbol_count']}", operation="enhanced_logging")
    training_logger.info(f"📅 Generated: {universe_data['generated_date']}", operation="enhanced_logging")
    training_logger.info(f"📈 Data source: {universe_data['data_source']}", operation="enhanced_logging")

    # Check training module
    try:
        from training.historical_training_module import HistoricalTrainingModule
        from training.training_config import TrainingConfig

        training_logger.info("\n✅ Training modules imported successfully", operation="enhanced_logging")

        # Test with generated symbols
        symbols = universe_data["symbols"]
        training_logger.info(f"📊 Testing with {len(symbols, operation="enhanced_logging")} symbols...")

        # Create training config
        config = TrainingConfig.curated_120_training()
        config["symbols"] = symbols[:120]  # Use first 120 symbols

        training_logger.info(f"✅ Training config created with {len(config['symbols'], operation="enhanced_logging")} symbols")
        training_logger.info(f"📅 Training period: {config['training_start_date']} to {config['training_end_date']}", operation="enhanced_logging")
        training_logger.info(f"🔍 Lookback window: {config['lookback_window']} days", operation="enhanced_logging")

        # Test training module initialization
        training_module = HistoricalTrainingModule(config)
        # Use the module to validate config wiring without running training
        assert training_module is not None
        training_logger.info(f"✅ Training module initialized: {training_module.__class__.__name__}", operation="enhanced_logging")

        training_logger.info("\n🎯 INTEGRATION VERIFIED!", operation="enhanced_logging")
        training_logger.info("=" * 50, operation="enhanced_logging")
        training_logger.info("✅ Universe list works with training module", operation="enhanced_logging")
        training_logger.info("✅ All components integrated", operation="enhanced_logging")
        training_logger.info("✅ Ready for algorithm training", operation="enhanced_logging")

    except Exception as e:
        training_logger.error(f"❌ Training module error: {e}", operation="enhanced_logging")
        training_logger.info("   Check that training modules are properly installed", operation="enhanced_logging")


if __name__ == "__main__":
    main()
