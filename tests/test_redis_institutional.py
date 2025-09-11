#!/usr/bin/env python3
"""
Test Redis Institutional Integration
"""

import sys
sys.path.append('.')

from services.infrastructure_manager import InstitutionalInfrastructureManager

def test_redis_institutional():
    """Test Redis institutional integration"""
    print("🔍 VERIFYING REDIS INSTITUTIONAL INTEGRATION")
    print("=" * 50)
    
    # Initialize infrastructure
    infra = InstitutionalInfrastructureManager(redis_enabled=True)
    
    print(f"Redis Enabled: {infra.redis_enabled}")
    print(f"Redis Client: {infra.redis_client is not None}")
    
    # Test Redis caching
    print("\nTesting Redis caching...")
    test_data = {
        'institutional_test': True,
        'timestamp': '2025-09-11T00:37:00Z',
        'data_size': 'large'
    }
    
    infra.cache_data('institutional_test', test_data, ttl=3600)
    cached = infra.get_cached_data('institutional_test')
    
    print(f"Cache Test: {cached is not None}")
    print(f"Data Integrity: {cached == test_data}")
    
    # Test Redis performance
    print("\nTesting Redis performance...")
    for i in range(100):
        infra.cache_data(f'perf_test_{i}', {
            'id': i,
            'data': f'performance_test_{i}'
        }, ttl=60)
    
    print("Cached 100 items")
    
    # Retrieve items
    retrieved = 0
    for i in range(100):
        if infra.get_cached_data(f'perf_test_{i}'):
            retrieved += 1
    
    print(f"Retrieved {retrieved}/100 items")
    
    # Get cache statistics
    stats = infra.get_resource_stats()
    print(f"Cache Hit Rate: {stats.cache_hit_rate:.1%}")
    
    # Test large data caching
    print("\nTesting large data caching...")
    large_data = {
        'institutional_portfolio': {
            'positions': [{'symbol': f'STOCK_{i}', 'quantity': i*100, 'price': 150.0 + i} for i in range(50)],
            'metrics': {'total_value': 1000000, 'pnl': 50000},
            'timestamp': '2025-09-11T00:37:00Z'
        }
    }
    
    infra.cache_data('large_portfolio', large_data, ttl=3600)
    cached_large = infra.get_cached_data('large_portfolio')
    
    print(f"Large Data Cache: {cached_large is not None}")
    print(f"Large Data Integrity: {cached_large == large_data}")
    
    # Test concurrent caching
    print("\nTesting concurrent caching...")
    import threading
    import time
    
    def cache_worker(worker_id, start_idx, count):
        for i in range(start_idx, start_idx + count):
            infra.cache_data(f'concurrent_{worker_id}_{i}', {
                'worker': worker_id,
                'index': i,
                'timestamp': time.time()
            }, ttl=60)
    
    # Start 4 concurrent workers
    threads = []
    for i in range(4):
        t = threading.Thread(target=cache_worker, args=(i, i*25, 25))
        threads.append(t)
        t.start()
    
    # Wait for completion
    for t in threads:
        t.join()
    
    print("Concurrent caching completed")
    
    # Verify concurrent data
    concurrent_retrieved = 0
    for worker_id in range(4):
        for i in range(worker_id*25, worker_id*25 + 25):
            if infra.get_cached_data(f'concurrent_{worker_id}_{i}'):
                concurrent_retrieved += 1
    
    print(f"Concurrent Data Retrieved: {concurrent_retrieved}/100")
    
    # Final statistics
    final_stats = infra.get_resource_stats()
    print(f"\nFinal Cache Hit Rate: {final_stats.cache_hit_rate:.1%}")
    print(f"Memory Usage: {final_stats.memory_percent:.1f}%")
    print(f"Active Threads: {final_stats.active_threads}")
    
    infra.shutdown()
    print("\n✅ Redis institutional integration test completed")

if __name__ == "__main__":
    test_redis_institutional()
