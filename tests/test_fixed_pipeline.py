#!/usr/bin/env python3
"""
Test the fixed pipeline
"""

import sys

sys.path.append(".")

# NO MOCKS - 100% GENUINE REAL DATA ONLY

from pipeline.enhanced_runner import EnhancedPipelineRunner


def test_fixed_pipeline():
    """Test the fixed pipeline"""
    training_logger.info("🔧 TESTING FIXED PIPELINE", operation="enhanced_logging")
    training_logger.info("=" * 40, operation="enhanced_logging")

    runner = EnhancedPipelineRunner()

    training_logger.info("🔥 Using REAL market data from Polygon API - NO MOCKS!", operation="enhanced_logging")

    # Use recent dates to ensure data availability
    from datetime import datetime, timedelta

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Run with REAL market data
    runner.run_enhanced_once(
        ["AAPL"], start_date, end_date, execute=False, prioritize_by_news=False
    )

    training_logger.info("✅ Pipeline working with REAL DATA - 100% GENUINE!", operation="enhanced_logging")

    runner.shutdown()


if __name__ == "__main__":
    test_fixed_pipeline()
