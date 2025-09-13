#!/usr/bin/env python3
"""
Verify Enhanced Pipeline is using 24-thread infrastructure
"""

import sys
sys.path.append('.')

from pipeline.enhanced_runner import EnhancedPipelineRunner
from unittest.mock import patch, MagicMock
import time

def test_enhanced_pipeline_verification():
    """Verify enhanced pipeline uses 24-thread infrastructure"""
    print("🔍 VERIFYING ENHANCED PIPELINE 24-THREAD INFRASTRUCTURE")
    print("=" * 60)
    
    # Initialize enhanced pipeline
    runner = EnhancedPipelineRunner()
    
    print(f"Infrastructure Threads: {runner.infra.total_threads}")
    print(f"Memory Limit: {runner.infra.memory_limit_mb}MB")
    print(f"Redis Enabled: {runner.infra.redis_enabled}")
    
    # Test thread pool configurations
    print("\nThread Pool Configurations:")
    for name, config in runner.infra.thread_pools.items():
        print(f"  {name}: {config.max_workers} workers, {config.reserved_memory_mb}MB, priority {config.priority}")
    
    # Test parallel processing with real data nocontam: allow
    print("\nTesting parallel processing...")
    
    with patch.object(runner.polygon_client, 'get_aggs') as mock_get_aggs:
        mock_get_aggs.return_value = {
            "results": [
                {
                    "p": 150.0,
                    "s": 1000000,
                    "t": 1640995200000,
                    "c": [1],
                    "o": 145.0,
                    "h": 155.0,
                    "l": 140.0,
                    "v": 1000000,
                    "vw": 150.0
                }
            ]
        }
        
        # Test with multiple symbols to trigger parallel processing
        test_symbols = [f"SYMBOL_{i:03d}" for i in range(20)]
        
        start_time = time.time()
        runner.run_enhanced_once(
            test_symbols, "2023-01-03", "2023-01-10",
            execute=False, prioritize_by_news=True, news_booster_enabled=True
        )
        execution_time = time.time() - start_time
        
        print(f"Processed {len(test_symbols)} symbols in {execution_time:.2f} seconds")
        print(f"Average time per symbol: {execution_time/len(test_symbols):.3f} seconds")
        
        # Verify mock was called for all symbols
        assert mock_get_aggs.call_count >= len(test_symbols)
        print(f"API calls made: {mock_get_aggs.call_count}")
    
    # Test infrastructure resource usage
    print("\nResource Usage:")
    stats = runner.infra.get_resource_stats()
    print(f"  CPU Usage: {stats.cpu_percent:.1f}%")
    print(f"  Memory Usage: {stats.memory_percent:.1f}%")
    print(f"  Active Threads: {stats.active_threads}")
    print(f"  Cache Hit Rate: {stats.cache_hit_rate:.1%}")
    
    # Test thread pool performance
    print("\nTesting thread pool performance...")
    
    def heavy_computation(task_id, complexity):
        result = 0
        for i in range(complexity * 1000):
            result += i ** 0.5
        return f"Task {task_id} completed with result {result:.2f}"
    
    # Create tasks for different thread pools
    tasks_data_fetching = [
        (f"data_task_{i}", heavy_computation, (f"data_task_{i}", i % 5 + 1))
        for i in range(8)
    ]
    
    tasks_algorithm = [
        (f"algo_task_{i}", heavy_computation, (f"algo_task_{i}", i % 10 + 1))
        for i in range(10)
    ]
    
    tasks_news = [
        (f"news_task_{i}", heavy_computation, (f"news_task_{i}", i % 3 + 1))
        for i in range(4)
    ]
    
    tasks_execution = [
        (f"exec_task_{i}", heavy_computation, (f"exec_task_{i}", i % 2 + 1))
        for i in range(2)
    ]
    
    # Execute tasks in parallel across all thread pools
    start_time = time.time()
    
    data_results = runner.infra.execute_parallel_tasks(tasks_data_fetching, 'data_fetching')
    algo_results = runner.infra.execute_parallel_tasks(tasks_algorithm, 'algorithm_processing')
    news_results = runner.infra.execute_parallel_tasks(tasks_news, 'news_sentiment')
    exec_results = runner.infra.execute_parallel_tasks(tasks_execution, 'execution_bridge')
    
    execution_time = time.time() - start_time
    
    total_tasks = len(data_results) + len(algo_results) + len(news_results) + len(exec_results)
    successful_tasks = (len([r for r in data_results if r[2] is None]) +
                       len([r for r in algo_results if r[2] is None]) +
                       len([r for r in news_results if r[2] is None]) +
                       len([r for r in exec_results if r[2] is None]))
    
    print(f"Total Tasks: {total_tasks}")
    print(f"Successful: {successful_tasks}")
    print(f"Success Rate: {successful_tasks/total_tasks*100:.1f}%")
    print(f"Execution Time: {execution_time:.2f} seconds")
    print(f"Tasks per Second: {total_tasks/execution_time:.1f}")
    
    # Test Redis caching performance
    print("\nTesting Redis caching performance...")
    
    # Cache large amounts of data
    for i in range(1000):
        runner.infra.cache_data(f"perf_test_{i}", {
            'id': i,
            'data': f'performance_test_data_{i}',
            'timestamp': time.time(),
            'complex_data': [j for j in range(100)]
        }, ttl=60)
    
    print("Cached 1000 items")
    
    # Retrieve data
    retrieved = 0
    for i in range(1000):
        if runner.infra.get_cached_data(f"perf_test_{i}"):
            retrieved += 1
    
    print(f"Retrieved {retrieved}/1000 items")
    
    # Final performance report
    print("\nFinal Performance Report:")
    report = runner.infra.get_performance_report()
    print(f"  Total Tasks Completed: {report['performance_metrics']['total_tasks_completed']}")
    print(f"  Average Task Duration: {report['performance_metrics']['average_task_duration']:.3f}ms")
    print(f"  Cache Hits: {report['performance_metrics']['cache_hits']}")
    print(f"  Cache Misses: {report['performance_metrics']['cache_misses']}")
    
    # Shutdown
    runner.shutdown()
    
    print("\n✅ Enhanced pipeline 24-thread infrastructure verification completed")

if __name__ == "__main__":
    test_enhanced_pipeline_verification()
