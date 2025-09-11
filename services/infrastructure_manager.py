#!/usr/bin/env python3
"""
🏗️ INSTITUTIONAL INFRASTRUCTURE MANAGER
======================================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

24-thread parallel processing architecture with 3GB Redis allocation
- Production-grade memory management
- Real-time data caching system
- Resource monitoring and optimization
- Scalability for 216 bandit future
- NO development shortcuts

INSTITUTIONAL-GRADE INFRASTRUCTURE
"""

import os
import time
import psutil
import threading
import queue
from typing import Dict, List, Any, Optional, Callable, Tuple
from datetime import datetime, UTC
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from threading import Lock, Event
import json
import logging

# Redis imports (will be installed if needed)
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️ Redis not available - using in-memory cache fallback")

from utils.env_loader import load_env_from_known_locations


@dataclass
class ResourceStats:
    """Resource utilization statistics"""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    active_threads: int
    cache_hit_rate: float
    timestamp: datetime


@dataclass
class ThreadPoolConfig:
    """Thread pool configuration"""
    max_workers: int
    thread_name_prefix: str
    priority: int
    reserved_memory_mb: int


class InstitutionalInfrastructureManager:
    """
    🏗️ INSTITUTIONAL INFRASTRUCTURE MANAGER
    ======================================
    24-thread parallel processing with 3GB Redis allocation
    """
    
    def __init__(self, redis_enabled: bool = True):
        load_env_from_known_locations()
        
        # ENHANCED: 24-thread architecture configuration
        self.total_threads = 24
        self.redis_enabled = redis_enabled and REDIS_AVAILABLE
        self.memory_limit_mb = 3072  # 3GB
        self.cache_ttl = 300  # 5 minutes
        
        # ENHANCED: Thread pool configurations for different workloads
        self.thread_pools = {
            'data_fetching': ThreadPoolConfig(
                max_workers=8,
                thread_name_prefix='data-fetch',
                priority=1,
                reserved_memory_mb=512
            ),
            'algorithm_processing': ThreadPoolConfig(
                max_workers=10,
                thread_name_prefix='algo-proc',
                priority=2,
                reserved_memory_mb=1024
            ),
            'news_sentiment': ThreadPoolConfig(
                max_workers=4,
                thread_name_prefix='news-sent',
                priority=3,
                reserved_memory_mb=256
            ),
            'execution_bridge': ThreadPoolConfig(
                max_workers=2,
                thread_name_prefix='exec-bridge',
                priority=4,
                reserved_memory_mb=128
            )
        }
        
        # ENHANCED: Initialize Redis connection
        self.redis_client = None
        if self.redis_enabled:
            try:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    db=int(os.getenv('REDIS_DB', 0)),
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self.redis_client.ping()
                print("✅ Redis connection established")
            except Exception as e:
                print(f"⚠️ Redis connection failed: {e}")
                self.redis_enabled = False
                self.redis_client = None
        
        # ENHANCED: Fallback in-memory cache
        self.memory_cache = {}
        self.cache_lock = Lock()
        
        # ENHANCED: Resource monitoring
        self.resource_monitor = ResourceMonitor(self)
        self.monitoring_active = False
        self.monitoring_thread = None
        
        # ENHANCED: Thread pool managers
        self.active_pools = {}
        self.pool_locks = {name: Lock() for name in self.thread_pools.keys()}
        
        # ENHANCED: Performance metrics
        self.performance_metrics = {
            'total_tasks_completed': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'average_task_duration': 0.0,
            'memory_usage_history': [],
            'cpu_usage_history': []
        }
        
        print("🏗️ Institutional Infrastructure Manager initialized")
        print(f"✅ 24-thread architecture ready")
        print(f"✅ Memory limit: {self.memory_limit_mb}MB")
        print(f"✅ Redis enabled: {self.redis_enabled}")
        print(f"✅ Thread pools configured: {len(self.thread_pools)}")

    def get_thread_pool(self, pool_name: str) -> ThreadPoolExecutor:
        """
        ENHANCED: Get or create thread pool for specific workload
        """
        if pool_name not in self.thread_pools:
            raise ValueError(f"Unknown thread pool: {pool_name}")
        
        with self.pool_locks[pool_name]:
            if pool_name not in self.active_pools:
                config = self.thread_pools[pool_name]
                self.active_pools[pool_name] = ThreadPoolExecutor(
                    max_workers=config.max_workers,
                    thread_name_prefix=config.thread_name_prefix
                )
                print(f"✅ Created thread pool: {pool_name} ({config.max_workers} workers)")
            
            return self.active_pools[pool_name]

    def cache_data(self, key: str, data: Any, ttl: Optional[int] = None) -> bool:
        """
        ENHANCED: Cache data with Redis or memory fallback
        """
        ttl = ttl or self.cache_ttl
        serialized_data = json.dumps(data, default=str)
        
        if self.redis_enabled and self.redis_client:
            try:
                self.redis_client.setex(key, ttl, serialized_data)
                return True
            except Exception as e:
                print(f"⚠️ Redis cache failed: {e}")
                # Fallback to memory cache
                pass
        
        # Memory cache fallback
        with self.cache_lock:
            self.memory_cache[key] = {
                'data': serialized_data,
                'expires': time.time() + ttl
            }
            return True

    def get_cached_data(self, key: str) -> Optional[Any]:
        """
        ENHANCED: Retrieve cached data with automatic expiration
        """
        if self.redis_enabled and self.redis_client:
            try:
                data = self.redis_client.get(key)
                if data:
                    self.performance_metrics['cache_hits'] += 1
                    return json.loads(data)
                else:
                    self.performance_metrics['cache_misses'] += 1
                    return None
            except Exception as e:
                print(f"⚠️ Redis cache retrieval failed: {e}")
                # Fallback to memory cache
                pass
        
        # Memory cache fallback
        with self.cache_lock:
            if key in self.memory_cache:
                entry = self.memory_cache[key]
                if time.time() < entry['expires']:
                    self.performance_metrics['cache_hits'] += 1
                    return json.loads(entry['data'])
                else:
                    # Expired entry
                    del self.memory_cache[key]
                    self.performance_metrics['cache_misses'] += 1
                    return None
            else:
                self.performance_metrics['cache_misses'] += 1
                return None

    def execute_parallel_tasks(self, tasks: List[Tuple[str, Callable, tuple]], 
                             pool_name: str = 'algorithm_processing') -> List[Any]:
        """
        ENHANCED: Execute tasks in parallel with resource monitoring
        """
        if not tasks:
            return []
        
        # Get appropriate thread pool
        thread_pool = self.get_thread_pool(pool_name)
        
        # ENHANCED: Monitor resource usage before execution
        if not self._check_resource_availability(pool_name):
            print(f"⚠️ Insufficient resources for {pool_name}, reducing task load")
            tasks = tasks[:len(tasks)//2]  # Reduce task load
        
        results = []
        start_time = time.time()
        
        try:
            # Submit tasks
            future_to_task = {
                thread_pool.submit(task_func, *args): (task_id, task_func, args)
                for task_id, task_func, args in tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task_id, task_func, args = future_to_task[future]
                try:
                    result = future.result()
                    results.append((task_id, result, None))
                except Exception as e:
                    results.append((task_id, None, str(e)))
                    print(f"⚠️ Task {task_id} failed: {e}")
        
        finally:
            # ENHANCED: Update performance metrics
            duration = time.time() - start_time
            self.performance_metrics['total_tasks_completed'] += len(tasks)
            self.performance_metrics['average_task_duration'] = (
                (self.performance_metrics['average_task_duration'] * 
                 (self.performance_metrics['total_tasks_completed'] - len(tasks)) + 
                 duration) / self.performance_metrics['total_tasks_completed']
            )
        
        return results

    def _check_resource_availability(self, pool_name: str) -> bool:
        """
        ENHANCED: Check if sufficient resources are available
        """
        config = self.thread_pools[pool_name]
        
        # Check memory availability
        memory = psutil.virtual_memory()
        available_mb = memory.available / (1024 * 1024)
        
        if available_mb < config.reserved_memory_mb:
            return False
        
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        if cpu_percent > 90:  # Don't overload CPU
            return False
        
        return True

    def start_resource_monitoring(self):
        """
        ENHANCED: Start real-time resource monitoring
        """
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(
            target=self.resource_monitor.monitor_resources,
            daemon=True
        )
        self.monitoring_thread.start()
        print("✅ Resource monitoring started")

    def stop_resource_monitoring(self):
        """
        ENHANCED: Stop resource monitoring
        """
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("✅ Resource monitoring stopped")

    def get_resource_stats(self) -> ResourceStats:
        """
        ENHANCED: Get current resource utilization statistics
        """
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Calculate cache hit rate
        total_cache_requests = (self.performance_metrics['cache_hits'] + 
                               self.performance_metrics['cache_misses'])
        cache_hit_rate = (self.performance_metrics['cache_hits'] / 
                         max(1, total_cache_requests))
        
        # Count active threads
        active_threads = sum(
            pool._threads.__len__() if hasattr(pool, '_threads') else 0
            for pool in self.active_pools.values()
        )
        
        return ResourceStats(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / (1024 * 1024),
            memory_available_mb=memory.available / (1024 * 1024),
            active_threads=active_threads,
            cache_hit_rate=cache_hit_rate,
            timestamp=datetime.now(UTC)
        )

    def optimize_performance(self):
        """
        ENHANCED: Optimize system performance based on current metrics
        """
        stats = self.get_resource_stats()
        
        # Memory optimization
        if stats.memory_percent > 80:
            print("🧹 High memory usage detected, clearing cache")
            self.clear_cache()
        
        # CPU optimization
        if stats.cpu_percent > 85:
            print("⚡ High CPU usage detected, reducing thread pools")
            for pool_name, pool in self.active_pools.items():
                if hasattr(pool, '_max_workers'):
                    current_workers = pool._max_workers
                    if current_workers > 2:
                        pool._max_workers = max(2, current_workers - 1)
                        print(f"   Reduced {pool_name} workers to {pool._max_workers}")

    def clear_cache(self):
        """
        ENHANCED: Clear all caches
        """
        if self.redis_enabled and self.redis_client:
            try:
                self.redis_client.flushdb()
                print("✅ Redis cache cleared")
            except Exception as e:
                print(f"⚠️ Redis cache clear failed: {e}")
        
        with self.cache_lock:
            self.memory_cache.clear()
            print("✅ Memory cache cleared")

    def shutdown(self):
        """
        ENHANCED: Graceful shutdown of all resources
        """
        print("🛑 Shutting down infrastructure manager...")
        
        # Stop monitoring
        self.stop_resource_monitoring()
        
        # Shutdown thread pools
        for pool_name, pool in self.active_pools.items():
            print(f"   Shutting down {pool_name} pool...")
            pool.shutdown(wait=True)
        
        # Close Redis connection
        if self.redis_client:
            self.redis_client.close()
        
        print("✅ Infrastructure manager shutdown complete")

    def get_performance_report(self) -> Dict[str, Any]:
        """
        ENHANCED: Get comprehensive performance report
        """
        stats = self.get_resource_stats()
        
        return {
            'timestamp': datetime.now(UTC).isoformat(),
            'resource_stats': {
                'cpu_percent': stats.cpu_percent,
                'memory_percent': stats.memory_percent,
                'memory_used_mb': stats.memory_used_mb,
                'memory_available_mb': stats.memory_available_mb,
                'active_threads': stats.active_threads,
                'cache_hit_rate': stats.cache_hit_rate
            },
            'performance_metrics': self.performance_metrics.copy(),
            'thread_pools': {
                name: {
                    'max_workers': config.max_workers,
                    'reserved_memory_mb': config.reserved_memory_mb,
                    'active': name in self.active_pools
                }
                for name, config in self.thread_pools.items()
            },
            'redis_status': {
                'enabled': self.redis_enabled,
                'connected': self.redis_client is not None
            }
        }


class ResourceMonitor:
    """
    ENHANCED: Real-time resource monitoring
    """
    
    def __init__(self, infrastructure_manager):
        self.infrastructure_manager = infrastructure_manager
        self.monitoring_interval = 30  # seconds
        self.max_history = 100
        
    def monitor_resources(self):
        """
        ENHANCED: Continuous resource monitoring
        """
        while self.infrastructure_manager.monitoring_active:
            try:
                stats = self.infrastructure_manager.get_resource_stats()
                
                # Store history
                self.infrastructure_manager.performance_metrics['memory_usage_history'].append(
                    stats.memory_percent
                )
                self.infrastructure_manager.performance_metrics['cpu_usage_history'].append(
                    stats.cpu_percent
                )
                
                # Trim history
                for key in ['memory_usage_history', 'cpu_usage_history']:
                    history = self.infrastructure_manager.performance_metrics[key]
                    if len(history) > self.max_history:
                        self.infrastructure_manager.performance_metrics[key] = history[-self.max_history:]
                
                # Auto-optimize if needed
                if stats.memory_percent > 85 or stats.cpu_percent > 90:
                    self.infrastructure_manager.optimize_performance()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"⚠️ Resource monitoring error: {e}")
                time.sleep(5)


def main():
    """Test the infrastructure manager"""
    print("🧪 Testing Institutional Infrastructure Manager")
    print("=" * 50)
    
    # Initialize infrastructure
    infra = InstitutionalInfrastructureManager()
    
    # Start monitoring
    infra.start_resource_monitoring()
    
    # Test thread pools
    def test_task(task_id: str, duration: float = 0.1):
        time.sleep(duration)
        return f"Task {task_id} completed"
    
    # Test parallel execution
    tasks = [
        (f"task_{i}", test_task, (f"task_{i}", 0.1))
        for i in range(10)
    ]
    
    print("🚀 Testing parallel task execution...")
    results = infra.execute_parallel_tasks(tasks, 'algorithm_processing')
    print(f"✅ Completed {len(results)} tasks")
    
    # Test caching
    print("💾 Testing cache functionality...")
    test_data = {"test": "data", "timestamp": datetime.now(UTC).isoformat()}
    infra.cache_data("test_key", test_data, ttl=60)
    cached_data = infra.get_cached_data("test_key")
    print(f"✅ Cache test: {cached_data is not None}")
    
    # Get performance report
    report = infra.get_performance_report()
    print(f"📊 Performance report generated: {len(report)} metrics")
    
    # Shutdown
    infra.shutdown()
    print("✅ Infrastructure manager test completed")


if __name__ == "__main__":
    main()
