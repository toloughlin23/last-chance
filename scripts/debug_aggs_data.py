#!/usr/bin/env python3
"""
Debug aggs_data type issue
"""

import sys
sys.path.append('.')

from pipeline.enhanced_runner import EnhancedPipelineRunner
from unittest.mock import patch

def debug_aggs_data():
    """Debug what type aggs_data actually is"""
    print("🔍 DEBUGGING AGGS_DATA TYPE")
    print("=" * 40)
    
    runner = EnhancedPipelineRunner()
    
    # Create a custom process_algorithm function that shows the data type
    def debug_process_algorithm(alg_name: str, algorithm, aggs_data):
        print(f"🔍 Algorithm: {alg_name}")
        print(f"🔍 aggs_data type: {type(aggs_data)}")
        print(f"🔍 aggs_data: {aggs_data}")
        if hasattr(aggs_data, 'get'):
            print(f"🔍 Has get method: True")
            print(f"🔍 aggs_data.get('results'): {aggs_data.get('results')}")
        else:
            print(f"🔍 Has get method: False")
        return alg_name, 0.5
    
    # Replace the process_algorithm function temporarily
    original_process_algorithm = None
    
    with patch.object(runner.polygon_client, 'get_aggs') as mock_get_aggs:
        mock_get_aggs.return_value = {
            'results': [
                {
                    'p': 150.0,
                    's': 1000000,
                    't': 1640995200000,
                    'c': [1],
                    'o': 145.0,
                    'h': 155.0,
                    'l': 140.0,
                    'v': 1000000,
                    'vw': 150.0
                }
            ]
        }
        
        # Monkey patch the process_algorithm function
        import pipeline.enhanced_runner
        original_process_algorithm = pipeline.enhanced_runner.process_algorithm
        pipeline.enhanced_runner.process_algorithm = debug_process_algorithm
        
        try:
            runner.run_enhanced_once(
                ['AAPL'], 
                '2023-01-03', 
                '2023-01-10', 
                execute=False, 
                prioritize_by_news=False
            )
        finally:
            # Restore original function
            pipeline.enhanced_runner.process_algorithm = original_process_algorithm
    
    runner.shutdown()

if __name__ == "__main__":
    debug_aggs_data()
