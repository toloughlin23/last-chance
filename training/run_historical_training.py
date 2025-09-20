#!/usr/bin/env python3
"""
🚀 HISTORICAL TRAINING RUNNER
=============================
Easy-to-use script for running historical training
"""

import os
import sys
import argparse
from datetime import datetime
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.historical_training_module import HistoricalTrainingModule, TrainingConfig
from training.training_config import TrainingPresets, TrainingValidation, TRAINING_BEST_PRACTICES


def main():
    parser = argparse.ArgumentParser(
        description='Run historical training for Super Bandits system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=TRAINING_BEST_PRACTICES
    )
    
    parser.add_argument(
        '--preset',
        choices=['3month', '6month', '1year', '2year', 'test'],
        default='1year',
        help='Training duration preset (default: 1year)'
    )
    
    parser.add_argument(
        '--export-path',
        default='training/exports/trained_models.json',
        help='Path to export trained models'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show configuration without running training'
    )
    
    args = parser.parse_args()
    
    # Get preset configuration
    preset_map = {
        '3month': TrainingPresets.three_month_training,
        '6month': TrainingPresets.six_month_training,
        '1year': TrainingPresets.one_year_training,
        '2year': TrainingPresets.two_year_training,
        'test': TrainingPresets.quick_test_training
    }
    
    config_dict = preset_map[args.preset]()
    
    # Create training config
    config = TrainingConfig(**config_dict)
    
    # Display configuration
    print("🎯 HISTORICAL TRAINING CONFIGURATION")
    print("=" * 50)
    print(f"Preset: {args.preset}")
    print(f"Training period: {config.training_start_date.date()} to {config.training_end_date.date()}")
    print(f"Duration: {(config.training_end_date - config.training_start_date).days} days")
    print(f"Symbols: {len(config.symbols)} stocks")
    print(f"Lookback window: {config.lookback_window} days")
    print(f"Zero forward-looking bias: {'ENABLED' if config.validate_no_future_data else 'DISABLED'}")
    print(f"Export path: {args.export_path}")
    print("=" * 50)
    
    # Validate configuration
    print("\n🔍 VALIDATING CONFIGURATION...")
    
    if not TrainingValidation.validate_no_overlap_with_live(config.training_end_date):
        print("⚠️ WARNING: Training end date is in the future!")
    
    if not TrainingValidation.validate_sufficient_data(
        config.training_start_date, 
        config.training_end_date
    ):
        print("⚠️ WARNING: Less than 60 trading days of data!")
    
    if not TrainingValidation.validate_symbol_coverage(config.symbols):
        print("⚠️ WARNING: Less than 5 symbols - may not achieve sufficient diversity!")
    
    if args.dry_run:
        print("\n✅ DRY RUN - Configuration validated, no training performed")
        return
    
    # Confirm before starting
    print("\n" + "=" * 50)
    response = input("📊 Start training? This may take several minutes. (y/N): ")
    if response.lower() != 'y':
        print("❌ Training cancelled")
        return
    
    # Create training module
    print("\n🚀 STARTING HISTORICAL TRAINING...")
    trainer = HistoricalTrainingModule(config)
    
    try:
        # Run training
        results = trainer.run_full_training()
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 TRAINING COMPLETE!")
        print("=" * 50)
        print(f"Total trades executed: {results['total_trades']:,}")
        print(f"Overall confidence variance: {results['overall_variance']:.6f}")
        print(f"Diversity target achieved: {'✅ YES' if results['diversity_achieved'] else '❌ NO'}")
        
        print("\n📈 ALGORITHM PERFORMANCE:")
        for algo_name, performance in results['algorithm_performance'].items():
            print(f"\n{algo_name.upper()}:")
            print(f"  Total trades: {performance['total_trades']:,}")
            print(f"  Average reward: {performance['avg_reward_bps']:.2f} basis points")
            print(f"  Win rate: {performance['win_rate']:.2%}")
            print(f"  Confidence variance: {performance['confidence_variance']:.6f}")
            print(f"  Unique confidence values: {performance['unique_confidence_count']}")
            print(f"  Confidence range: [{performance['confidence_range'][0]:.4f}, {performance['confidence_range'][1]:.4f}]")
        
        # Export models
        trainer.export_trained_models(args.export_path)
        print(f"\n✅ Trained models exported to: {args.export_path}")
        
        # Save training summary
        summary_path = args.export_path.replace('.json', '_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Training summary saved to: {summary_path}")
        
        # Next steps
        print("\n🎯 NEXT STEPS:")
        print("1. Review training summary for performance metrics")
        print("2. Verify diversity variance is > 0.15")
        print("3. Load trained models into live system when ready")
        print("4. Run backtesting on out-of-sample data")
        
        if results['diversity_achieved']:
            print("\n✅ DIVERSITY ACHIEVED! Algorithms are ready for live trading!")
        else:
            print("\n⚠️ DIVERSITY NOT ACHIEVED - Consider:")
            print("  - Training for a longer period")
            print("  - Adding more diverse symbols")
            print("  - Adjusting algorithm parameters")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
