from datetime import datetime
from training.historical_training_module import TrainingConfig

# Define the optimized 13 symbols
symbols = [
    "AAPL",  # Apple Inc. (Technology)
    "RKT",   # Rocket Companies (Financial Technology)
    "GOOGL", # Google (Technology) - Replaced CDE for better liquidity
    "AAL",   # American Airlines (Consumer Discretionary)
    "NCLH",  # Norwegian Cruise Line (Consumer Discretionary)
    "HAL",   # Halliburton (Energy)
    "STM",   # STMicroelectronics (Technology)
    "NU",    # Nu Holdings (Financial Technology)
    "CCL",   # Carnival Corporation (Consumer Discretionary)
    "SLB",   # Schlumberger (Energy)
    "HPE",   # Hewlett Packard Enterprise (Technology)
    "BAC",   # Bank of America (Financials)
    "DAY"    # Dayforce (Technology)
]

# Define the training configuration
optimized_training_config = TrainingConfig(
    training_start_date=datetime(2025, 3, 1),
    training_end_date=datetime(2025, 9, 25),
    symbols=symbols,
    lookback_window=20,
    news_lookback_hours=24,
    min_data_points=100,
    validate_no_future_data=True,
    save_checkpoints=True,
    checkpoint_frequency=30,
    enable_walk_forward=True,
    cross_validation_folds=5,
    bias_detection_enabled=True,
    performance_monitoring=True,
    adaptive_learning_rate=True,
    feature_engineering="kitchen_sink",
    data_quality_checks=True,
    model_ensemble=True,
    risk_management="institutional",
    backtesting_mode="kitchen_sink",
    use_minute_data=True,
    data_granularity="minute",
    zero_lookforward_bias=True,
    temporal_validation=True,
    point_in_time_validation=True,
    technical_indicators=True,
    minute_level_indicators=True,
    advanced_oscillators=True,
    volume_analysis=True,
    volatility_indicators=True,
    momentum_indicators=True,
    support_resistance=True,
    intraday_patterns=True,
    market_microstructure=True,
    news_sentiment=True,
    sector_analysis=True,
    earnings_impact=True,
    analyst_sentiment=True,
    institutional_flow=True,
    retail_sentiment=True,
    enable_advanced_nlp=True,
    sentiment_momentum=True,
    news_urgency_scoring=True,
    sector_sentiment_analysis=True,
    earnings_impact_analysis=True,
    analyst_sentiment_tracking=True,
    volatility_impact_analysis=True,
    liquidity_impact_analysis=True,
    institutional_flow_analysis=True,
    retail_sentiment_analysis=True,
    news_quality_scoring=True,
    temporal_decay_weighting=True,
    multi_source_aggregation=True,
    linucb_alpha=0.8,
    neural_learning_rate=0.01,
    neural_hidden_sizes=[64, 32, 16],
    ucbv_confidence_boost=1.6,
    ucbv_min_confidence=0.4,
    ucbv_max_confidence=0.85,
    confidence_variance_threshold=0.05,
    action_distribution_threshold=0.8,
    temporal_bias_threshold=0.1,
    overconfidence_threshold=0.6,
    underconfidence_threshold=0.4,
    model_drift_detection=True,
    retraining_threshold=0.1,
    performance_degradation_threshold=0.15,
    diversity_target=0.15,
    description="Optimized training for 13 symbols from March 1st to September 25th, 2025 with minute data and news sentiment. Hybrid approach with proven liquidity and unique sector diversification."
)

print("🚀 OPTIMIZED TRAINING CONFIGURATION READY!")
print(f"📊 Symbols: {len(symbols)} symbols")
print(f"📅 Time Frame: {optimized_training_config.training_start_date.strftime('%Y-%m-%d')} to {optimized_training_config.training_end_date.strftime('%Y-%m-%d')}")
print(f"⏱️ Duration: ~6.8 months of minute-level data")
print(f"🎯 Features: Kitchen sink approach with zero lookforward bias")
print(f"🔧 Algorithms: LinUCB, Neural Bandit, UCB-V (independent)")
print(f"📈 Expected: High-quality training with diverse sector exposure")
