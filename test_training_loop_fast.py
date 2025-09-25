from datetime import datetime, timedelta
from training.historical_training_module import TrainingConfig

# Create a FAST test configuration with just 1 week of data and 3 symbols
fast_test_config = TrainingConfig(
    training_start_date=datetime(2025, 9, 18),  # Just 1 week ago
    training_end_date=datetime(2025, 9, 25),    # Today
    symbols=["AAPL", "MSFT", "GOOGL"],          # Just 3 symbols
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
    description="FAST TEST: 1 week of data for 3 symbols to test training loop"
)

print("🚀 FAST TEST CONFIGURATION READY!")
print(f"📊 Symbols: {len(fast_test_config.symbols)} symbols")
print(f"📅 Time Frame: {fast_test_config.training_start_date.strftime('%Y-%m-%d')} to {fast_test_config.training_end_date.strftime('%Y-%m-%d')}")
print(f"⏱️ Duration: ~1 week of minute-level data")
print(f"🎯 Purpose: Test training loop with minimal data")
