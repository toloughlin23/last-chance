"""
🎯 TRAINING CONFIGURATION
========================
Centralized configuration for historical training module
"""

from datetime import datetime
from typing import Any, Dict, List

from utils.proven_symbol_expander import get_proven_expanded_symbols


class TrainingPresets:
    """Pre-configured training scenarios"""

    @staticmethod
    def three_month_training() -> Dict[str, Any]:
        """3-month training configuration"""
        return {
            "training_start_date": datetime(2024, 10, 1),
            "training_end_date": datetime(2024, 12, 31),
            "symbols": [
                "AAPL",
                "GOOGL",
                "MSFT",
                "AMZN",
                "TSLA",
                "NVDA",
                "META",
                "JPM",
                "V",
                "JNJ",
            ],
            "lookback_window": 20,
            "news_lookback_hours": 24,
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 15,  # Every 15 days
        }

    @staticmethod
    def six_month_training() -> Dict[str, Any]:
        """6-month training configuration"""
        return {
            "training_start_date": datetime(2024, 7, 1),
            "training_end_date": datetime(2024, 12, 31),
            "symbols": [
                "AAPL",
                "GOOGL",
                "MSFT",
                "AMZN",
                "TSLA",
                "NVDA",
                "META",
                "JPM",
                "V",
                "JNJ",
                "WMT",
                "PG",
                "MA",
                "HD",
                "DIS",
                "ADBE",
                "NFLX",
                "CRM",
                "PFE",
                "TMO",
            ],
            "lookback_window": 20,
            "news_lookback_hours": 24,
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 30,  # Monthly
        }

    @staticmethod
    def one_year_training() -> Dict[str, Any]:
        """Full year training configuration (RECOMMENDED)"""
        return {
            "training_start_date": datetime(2024, 1, 1),
            "training_end_date": datetime(2024, 12, 31),
            "symbols": [
                # Tech Giants
                "AAPL",
                "GOOGL",
                "MSFT",
                "AMZN",
                "TSLA",
                "NVDA",
                "META",
                # Financial
                "JPM",
                "V",
                "MA",
                "BAC",
                "WFC",
                "GS",
                "MS",
                "AXP",
                # Healthcare
                "JNJ",
                "UNH",
                "PFE",
                "TMO",
                "ABT",
                "CVS",
                "DHR",
                # Consumer
                "WMT",
                "PG",
                "HD",
                "DIS",
                "NKE",
                "MCD",
                "SBUX",
                # Industrial
                "BA",
                "CAT",
                "MMM",
                "GE",
                "HON",
                "UPS",
                "RTX",
            ],
            "lookback_window": 20,
            "news_lookback_hours": 24,
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 30,  # Monthly
        }

    @staticmethod
    def two_year_training() -> Dict[str, Any]:
        """Two-year comprehensive training (MAXIMUM DIVERSITY)"""
        return {
            "training_start_date": datetime(2023, 1, 1),
            "training_end_date": datetime(2024, 12, 31),
            "symbols": [
                # S&P 500 Top 50 for maximum market coverage
                "AAPL",
                "MSFT",
                "GOOGL",
                "AMZN",
                "NVDA",
                "TSLA",
                "META",
                "BRK.B",
                "V",
                "JNJ",
                "WMT",
                "JPM",
                "MA",
                "PG",
                "UNH",
                "DIS",
                "HD",
                "VZ",
                "ADBE",
                "NFLX",
                "CRM",
                "PFE",
                "TMO",
                "ABT",
                "CSCO",
                "ACN",
                "NKE",
                "CVX",
                "LLY",
                "WFC",
                "DHR",
                "TXN",
                "PM",
                "NEE",
                "RTX",
                "SPGI",
                "INTU",
                "LOW",
                "UNP",
                "GS",
                "MS",
                "BMY",
                "AMT",
                "SYK",
                "ISRG",
                "CVS",
                "SCHW",
                "PLD",
                "AXP",
                "TJX",
            ],
            "lookback_window": 30,  # Longer lookback for more patterns
            "news_lookback_hours": 48,  # 2 days of news
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 60,  # Bi-monthly
        }

    @staticmethod
    def curated_120_training() -> Dict[str, Any]:
        """CURATED 120 SYMBOLS - OPTIMIZED FOR DAY TRADING (RECOMMENDED)"""
        return {
            "training_start_date": datetime(2024, 1, 1),
            "training_end_date": datetime(2024, 12, 31),
            "symbols": get_proven_expanded_symbols(),  # 120 symbols from proven candidates + REAL Polygon data
            "lookback_window": 20,
            "news_lookback_hours": 24,
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 30,  # Monthly
            "description": "120 symbols curated for optimal day trading performance",
        }

    @staticmethod
    def quick_test_training() -> Dict[str, Any]:
        """Quick test configuration (1 month for testing)"""
        return {
            "training_start_date": datetime(2024, 11, 1),
            "training_end_date": datetime(2024, 11, 30),
            "symbols": ["AAPL", "GOOGL", "MSFT"],
            "lookback_window": 10,
            "news_lookback_hours": 12,
            "validate_no_future_data": True,
            "save_checkpoints": True,
            "checkpoint_frequency": 10,
        }


class TrainingValidation:
    """Validation rules for training"""

    @staticmethod
    def validate_no_overlap_with_live(training_end_date: datetime) -> bool:
        """Ensure training data doesn't overlap with live trading"""
        # Live trading should start at least 1 day after training ends
        current_date = datetime.now()
        return training_end_date < current_date

    @staticmethod
    def validate_sufficient_data(
        start_date: datetime, end_date: datetime, min_days: int = 60
    ) -> bool:
        """Ensure sufficient training data"""
        trading_days = (end_date - start_date).days * 5 / 7  # Approximate trading days
        return trading_days >= min_days

    @staticmethod
    def validate_symbol_coverage(symbols: List[str], min_symbols: int = 5) -> bool:
        """Ensure adequate symbol diversity"""
        return len(symbols) >= min_symbols


# Best practices for training
TRAINING_BEST_PRACTICES = """
🎯 TRAINING BEST PRACTICES:

1. **Training Duration**:
   - Minimum: 3 months (catch recent patterns)
   - Recommended: 1 year (full market cycle)
   - Maximum benefit: 2 years (multiple market regimes)

2. **Symbol Selection**:
   - Minimum: 5-10 symbols (basic diversity)
   - Recommended: 20-30 symbols (good coverage)
   - Maximum: 50 symbols (comprehensive market view)

3. **Data Quality**:
   - Always use validate_no_future_data=True
   - Check for missing data gaps
   - Ensure consistent market hours

4. **Checkpointing**:
   - Save monthly for long training
   - Save bi-weekly for short training
   - Keep last 3 checkpoints

5. **Post-Training Validation**:
   - Verify diversity > 0.15
   - Check each algorithm has unique patterns
   - Validate no data leakage
"""
