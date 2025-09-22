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

    print("🔍 VERIFYING TRAINING MODULE INTEGRATION")
    print("=" * 50)

    # Check if universe file exists
    universe_file = "data/training/universe_list.json"
    if not os.path.exists(universe_file):
        print(f"❌ Universe file not found: {universe_file}")
        print("   Run generate_training_universe.py first")
        return

    # Load universe data
    with open(universe_file, "r") as f:
        universe_data = json.load(f)

    print(f"✅ Universe file loaded: {universe_file}")
    print(f"📊 Symbol count: {universe_data['symbol_count']}")
    print(f"📅 Generated: {universe_data['generated_date']}")
    print(f"📈 Data source: {universe_data['data_source']}")

    # Check training module
    try:
        from training.historical_training_module import HistoricalTrainingModule
        from training.training_config import TrainingConfig

        print("\n✅ Training modules imported successfully")

        # Test with generated symbols
        symbols = universe_data["symbols"]
        print(f"📊 Testing with {len(symbols)} symbols...")

        # Create training config
        config = TrainingConfig.curated_120_training()
        config["symbols"] = symbols[:120]  # Use first 120 symbols

        print(f"✅ Training config created with {len(config['symbols'])} symbols")
        print(
            f"📅 Training period: {config['training_start_date']} to {config['training_end_date']}"
        )
        print(f"🔍 Lookback window: {config['lookback_window']} days")

        # Test training module initialization
        training_module = HistoricalTrainingModule(config)
        print("✅ Training module initialized successfully")

        print("\n🎯 INTEGRATION VERIFIED!")
        print("=" * 50)
        print("✅ Universe list works with training module")
        print("✅ All components integrated")
        print("✅ Ready for algorithm training")

    except Exception as e:
        print(f"❌ Training module error: {e}")
        print("   Check that training modules are properly installed")


if __name__ == "__main__":
    main()
