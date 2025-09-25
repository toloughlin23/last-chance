#!/usr/bin/env python3
"""
🚀 KITCHEN SINK MINUTE DATA TRAINING RUNNER
===========================================
ULTRA-ENHANCED training system for active day trading with minute data
ZERO LOOKFORWARD BIAS - BULLETPROOF TEMPORAL INTEGRITY
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 🚀 ENHANCED: Load environment variables from .env file
from utils.env_loader import load_env_from_known_locations
load_env_from_known_locations()

from training.historical_training_module import HistoricalTrainingModule, TrainingConfig
from training.kitchen_sink_minute_training_config import get_kitchen_sink_minute_config
from utils.enhanced_logging_system import training_logger


def create_kitchen_sink_training_config(config_name: str) -> TrainingConfig:
    """🚀 KITCHEN SINK: Create ultra-enhanced training configuration"""
    config_dict = get_kitchen_sink_minute_config(config_name)
    
    # Convert to TrainingConfig object
    config = TrainingConfig(
        training_start_date=config_dict["training_start_date"],
        training_end_date=config_dict["training_end_date"],
        symbols=config_dict["symbols"],
        lookback_window=config_dict["lookback_window"],
        news_lookback_hours=config_dict["news_lookback_hours"],
        validate_no_future_data=config_dict["validate_no_future_data"],
        save_checkpoints=config_dict["save_checkpoints"],
        checkpoint_frequency=config_dict["checkpoint_frequency"]
    )
    
    # Add minute data specific attributes
    config.use_minute_data = config_dict.get("use_minute_data", True)
    config.data_granularity = config_dict.get("data_granularity", "minute")
    config.zero_lookforward_bias = config_dict.get("zero_lookforward_bias", True)
    config.temporal_validation = config_dict.get("temporal_validation", True)
    config.point_in_time_validation = config_dict.get("point_in_time_validation", True)
    
    return config


def run_kitchen_sink_minute_training(config_name: str, export_path: str = None) -> Dict[str, Any]:
    """🚀 KITCHEN SINK: Run ultra-enhanced minute data training"""
    
    training_logger.info("🚀 KITCHEN SINK MINUTE DATA TRAINING INITIATED")
    training_logger.info("=" * 60)
    
    # Create ultra-enhanced configuration
    config = create_kitchen_sink_training_config(config_name)
    
    training_logger.info(f"📊 Configuration: {config_name}")
    training_logger.info(f"📅 Training period: {config.training_start_date} to {config.training_end_date}")
    training_logger.info(f"📈 Data granularity: {getattr(config, 'data_granularity', 'minute')}")
    training_logger.info(f"🎯 Symbols: {len(config.symbols)} symbols")
    training_logger.info(f"🛡️ Zero lookforward bias: {getattr(config, 'zero_lookforward_bias', True)}")
    
    # Initialize training module
    training_module = HistoricalTrainingModule(config)
    
    # Load minute data with ultra-enhanced processing
    training_logger.info("📊 Loading ULTRA-ENHANCED minute data...")
    start_time = time.time()
    
    historical_data = training_module.load_historical_data()
    
    load_time = time.time() - start_time
    training_logger.info(f"✅ Minute data loaded in {load_time:.2f} seconds")
    
    # Validate data quality
    total_minutes = sum(len(df) for df in historical_data.values())
    training_logger.info(f"📊 Total minute bars loaded: {total_minutes:,}")
    
    # Run training with enhanced monitoring
    training_logger.info("🚀 Starting KITCHEN SINK training...")
    training_start = time.time()
    
    results = training_module.run_full_training()
    
    training_time = time.time() - training_start
    training_logger.info(f"✅ Training completed in {training_time:.2f} seconds")
    
    # Enhanced results analysis
    training_logger.info("📊 KITCHEN SINK TRAINING RESULTS:")
    training_logger.info("=" * 50)
    training_logger.info(f"Total trades: {results['total_trades']:,}")
    training_logger.info(f"Overall variance: {results['overall_variance']:.6f}")
    training_logger.info(f"Diversity achieved: {results['diversity_achieved']}")
    
    # Algorithm performance analysis
    for algo_name, performance in results['algorithm_performance'].items():
        training_logger.info(f"\n{algo_name.upper()}:")
        training_logger.info(f"  Trades: {performance['total_trades']:,}")
        training_logger.info(f"  Avg reward: {performance['avg_reward_bps']:.2f} bps")
        training_logger.info(f"  Win rate: {performance['win_rate']:.2%}")
        training_logger.info(f"  Confidence range: [{performance['confidence_range'][0]:.4f}, {performance['confidence_range'][1]:.4f}]")
    
    # Export results
    if export_path:
        training_logger.info(f"💾 Exporting results to: {export_path}")
        
        # Create JSON-safe results
        json_safe_results = {
            "training_config": {
                "config_name": config_name,
                "training_start_date": config.training_start_date.isoformat(),
                "training_end_date": config.training_end_date.isoformat(),
                "symbols": config.symbols,
                "data_granularity": getattr(config, 'data_granularity', 'minute'),
                "zero_lookforward_bias": getattr(config, 'zero_lookforward_bias', True)
            },
            "training_metrics": {
                "total_trades": int(results["total_trades"]),
                "overall_variance": float(results["overall_variance"]),
                "diversity_achieved": bool(results["diversity_achieved"]),
                "training_duration_seconds": float(training_time),
                "data_load_duration_seconds": float(load_time),
                "total_minute_bars": int(total_minutes)
            },
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
                "confidence_range": [float(x) for x in performance["confidence_range"]]
            }
        
        # Save results
        with open(export_path, "w") as f:
            json.dump(json_safe_results, f, indent=2)
        
        # Save summary
        summary_path = export_path.replace(".json", "_summary.json")
        with open(summary_path, "w") as f:
            json.dump({
                "training_summary": {
                    "config_name": config_name,
                    "total_trades": int(results["total_trades"]),
                    "overall_variance": float(results["overall_variance"]),
                    "diversity_achieved": bool(results["diversity_achieved"]),
                    "training_duration": f"{training_time:.2f} seconds",
                    "data_granularity": "minute",
                    "zero_lookforward_bias": True,
                    "export_timestamp": datetime.now().isoformat()
                }
            }, f, indent=2)
        
        training_logger.info(f"📄 Training summary saved to: {summary_path}")
    
    training_logger.info("🚀 KITCHEN SINK MINUTE DATA TRAINING COMPLETE!")
    training_logger.info("=" * 60)
    
    return results


def main():
    """🚀 KITCHEN SINK: Main training runner"""
    parser = argparse.ArgumentParser(description="🚀 KITCHEN SINK: Ultra-enhanced minute data training")
    parser.add_argument(
        "--config", 
        choices=["ultra_enhanced", "rapid_test", "production"],
        default="ultra_enhanced",
        help="Training configuration to use"
    )
    parser.add_argument(
        "--export-path",
        default="training/exports/kitchen_sink_minute_training.json",
        help="Path to export training results"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show configuration without running training"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        # Show configuration
        config_dict = get_kitchen_sink_minute_config(args.config)
        training_logger.info("🚀 KITCHEN SINK MINUTE DATA CONFIGURATION:", operation="run_kitchen_sink_minute_training")
        training_logger.info("=" * 50, operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Config: {args.config}", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Training period: {config_dict['training_start_date']} to {config_dict['training_end_date']}", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Symbols: {len(config_dict['symbols'])} symbols", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Data granularity: {config_dict['data_granularity']}", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Zero lookforward bias: {config_dict['zero_lookforward_bias']}", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"Lookback window: {config_dict['lookback_window']} minutes", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"News lookback: {config_dict['news_lookback_hours']} hours", operation="run_kitchen_sink_minute_training")
        training_logger.info("✅ Configuration ready for ROCKET-LEVEL training!", operation="run_kitchen_sink_minute_training")
        return
    
    # Ensure export directory exists
    os.makedirs(os.path.dirname(args.export_path), exist_ok=True)
    
    # Run training
    try:
        results = run_kitchen_sink_minute_training(args.config, args.export_path)
        training_logger.info("🚀 KITCHEN SINK TRAINING COMPLETED SUCCESSFULLY!", operation="run_kitchen_sink_minute_training")
        training_logger.info(f"📊 Results exported to: {args.export_path}", operation="run_kitchen_sink_minute_training")
    except Exception as e:
        training_logger.error(f"❌ Training failed: {e}")
        raise


if __name__ == "__main__":
    main()
