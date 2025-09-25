#!/usr/bin/env python3
"""
Debug aggs_data type issue
"""

import sys

sys.path.append(".")

from pipeline.enhanced_runner import EnhancedPipelineRunner

# nocontam: allow Development-time diagnostic tool; replaced mocks with genuine integration


def debug_aggs_data():
    """Debug what type aggs_data actually is"""
    training_logger.info("🔍 DEBUGGING AGGS_DATA TYPE", operation="enhanced_logging")
    training_logger.info("=" * 40, operation="enhanced_logging")

    runner = EnhancedPipelineRunner()

    # Create a custom process_algorithm function that shows the data type
    def debug_process_algorithm(alg_name: str, algorithm, aggs_data):
        training_logger.info(f"🔍 Algorithm: {alg_name}", operation="enhanced_logging")
        training_logger.info(f"🔍 aggs_data type: {type(aggs_data, operation="enhanced_logging")}")
        training_logger.info(f"🔍 aggs_data: {aggs_data}", operation="enhanced_logging")
        if hasattr(aggs_data, "get"):
            training_logger.info("🔍 Has get method: True", operation="enhanced_logging")
            training_logger.info(f"🔍 aggs_data.get('results', operation="enhanced_logging"): {aggs_data.get('results')}")
        else:
            training_logger.info("🔍 Has get method: False", operation="enhanced_logging")
        return alg_name, 0.5

    # Monkey patch the process_algorithm function to diagnose genuine pipeline flow
    import pipeline.enhanced_runner

    original_process_algorithm = pipeline.enhanced_runner.process_algorithm
    pipeline.enhanced_runner.process_algorithm = debug_process_algorithm
    try:
        # Run with real Polygon data (requires genuine API key)
        runner.run_enhanced_once(
            ["AAPL"],
            "2023-01-03",
            "2023-01-10",
            execute=False,
            prioritize_by_news=False,
        )
    finally:
        # Restore original function
        pipeline.enhanced_runner.process_algorithm = original_process_algorithm

    runner.shutdown()


if __name__ == "__main__":
    debug_aggs_data()
