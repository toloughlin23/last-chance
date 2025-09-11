#!/usr/bin/env python3
"""
Test the fixed pipeline
"""

import sys
sys.path.append('.')

from pipeline.enhanced_runner import EnhancedPipelineRunner
from unittest.mock import patch

def test_fixed_pipeline():
    """Test the fixed pipeline"""
    print("🔧 TESTING FIXED PIPELINE")
    print("=" * 40)
    
    runner = EnhancedPipelineRunner()
    
    print("Testing fixed pipeline...")
    
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
        
        runner.run_enhanced_once(
            ['AAPL'], 
            '2023-01-03', 
            '2023-01-10', 
            execute=False, 
            prioritize_by_news=False
        )
        
        print("✅ Pipeline working!")
    
    runner.shutdown()

if __name__ == "__main__":
    test_fixed_pipeline()
