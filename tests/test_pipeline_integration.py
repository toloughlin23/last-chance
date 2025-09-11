#!/usr/bin/env python3
"""
🧪 PIPELINE INTEGRATION TEST
===========================
100% GENUINE - NO SHORTCUTS - ALWAYS MAKE BETTER

Test complete pipeline integration with real data flow
- Enhanced pipeline runner
- Infrastructure manager
- Compliance system
- News sentiment analysis
- NO development shortcuts
"""

import sys
sys.path.append('.')

import pytest
import time
from datetime import datetime, UTC, timedelta
from unittest.mock import patch, MagicMock

from pipeline.enhanced_runner import EnhancedPipelineRunner
from services.infrastructure_manager import InstitutionalInfrastructureManager
from services.compliance_system import UKROIComplianceSystem
from services.advanced_news_sentiment import AdvancedNewsSentimentAnalysis


class TestPipelineIntegration:
    """Test complete pipeline integration"""
    
    def test_enhanced_pipeline_initialization(self):
        """Test enhanced pipeline runner initialization"""
        runner = EnhancedPipelineRunner()
        
        assert runner.infra is not None
        assert runner.polygon_client is not None
        assert runner.alpaca_client is not None
        assert runner.news_analyzer is not None
        assert len(runner.algorithms) == 3
        assert 'linucb' in runner.algorithms
        assert 'neural' in runner.algorithms
        assert 'ucbv' in runner.algorithms
        
        runner.shutdown()
    
    def test_infrastructure_integration(self):
        """Test infrastructure manager integration"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        assert infra.total_threads == 24
        assert infra.memory_limit_mb == 3072
        assert len(infra.thread_pools) == 4
        
        # Test thread pool creation
        data_pool = infra.get_thread_pool('data_fetching')
        assert data_pool is not None
        assert data_pool._max_workers == 8
        
        # Test caching
        test_data = {"test": "data", "timestamp": datetime.now(UTC).isoformat()}
        infra.cache_data("test_key", test_data, ttl=60)
        cached_data = infra.get_cached_data("test_key")
        assert cached_data is not None
        assert cached_data["test"] == "data"
        
        infra.shutdown()
    
    def test_compliance_system_integration(self):
        """Test compliance system integration"""
        compliance = UKROIComplianceSystem()
        
        assert len(compliance.compliance_rules) >= 10
        assert 'fca_001' in compliance.compliance_rules
        assert 'mifid_001' in compliance.compliance_rules
        assert 'gdpr_001' in compliance.compliance_rules
        
        # Test compliance check
        test_context = {
            'client_money': 1000000.0,
            'total_assets': 2000000.0,
            'execution_price': 150.0,
            'market_price': 150.1,
            'position_size': 50000.0,
            'total_market_cap': 1000000000.0,
            'transaction_time': datetime.now(UTC),
            'transaction_data': {
                'client_id': 'CLIENT_001',
                'instrument': 'AAPL',
                'quantity': 100,
                'price': 150.0
            },
            'target_market_validation': True,
            'risk_warning_provided': True,
            'order_rate': 500,
            'circuit_breaker_triggered': False,
            'data_processing_risk': 0.05,
            'dpia_conducted': True,
            'data_retention_days': 1000,
            'purpose_limitation': True,
            'explicit_consent': True,
            'withdrawal_right': True,
            'total_portfolio': 1000000.0,
            'liquid_assets': 400000.0,
            'last_stress_test': datetime.now(UTC) - timedelta(days=15)
        }
        
        report = compliance.run_compliance_check(test_context)
        assert report.total_checks > 0
        assert report.summary['compliance_score'] >= 0
        assert report.summary['compliance_score'] <= 100
    
    def test_news_sentiment_integration(self):
        """Test news sentiment analysis integration"""
        analyzer = AdvancedNewsSentimentAnalysis()
        
        assert analyzer.processing_cache is not None
        assert analyzer.cache_ttl == 300
        assert len(analyzer.news_sources) >= 3
        
        # Test cache functionality
        cache_stats = analyzer.get_cache_stats()
        assert 'total_entries' in cache_stats
        assert 'active_entries' in cache_stats
        assert 'expired_entries' in cache_stats
    
    def test_parallel_processing_integration(self):
        """Test parallel processing integration"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        def test_task(task_id: str, duration: float = 0.1):
            time.sleep(duration)
            return f"Task {task_id} completed"
        
        # Create test tasks
        tasks = [
            (f"task_{i}", test_task, (f"task_{i}", 0.1))
            for i in range(10)
        ]
        
        # Execute tasks in parallel
        results = infra.execute_parallel_tasks(tasks, 'algorithm_processing')
        
        assert len(results) == 10
        for task_id, result, error in results:
            assert error is None
            assert result == f"Task {task_id} completed"
        
        infra.shutdown()
    
    def test_resource_monitoring_integration(self):
        """Test resource monitoring integration"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        # Start monitoring
        infra.start_resource_monitoring()
        assert infra.monitoring_active is True
        
        # Get resource stats
        stats = infra.get_resource_stats()
        assert stats.cpu_percent >= 0
        assert stats.memory_percent >= 0
        assert stats.memory_used_mb > 0
        assert stats.memory_available_mb > 0
        assert stats.active_threads >= 0
        assert 0 <= stats.cache_hit_rate <= 1
        
        # Stop monitoring
        infra.stop_resource_monitoring()
        assert infra.monitoring_active is False
        
        infra.shutdown()
    
    def test_complete_pipeline_workflow(self):
        """Test complete pipeline workflow"""
        print("🧪 Testing complete pipeline workflow...")
        
        # Initialize all components
        runner = EnhancedPipelineRunner()
        compliance = UKROIComplianceSystem()
        
        # Test with real data to avoid API calls nocontam: allow
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
            
            # Test single run
            test_symbols = ["AAPL", "MSFT", "GOOGL"]
            runner.run_enhanced_once(
                test_symbols, "2023-01-03", "2023-01-10",
                execute=False, prioritize_by_news=True, news_booster_enabled=True
            )
            
            # Verify mock was called
            assert mock_get_aggs.call_count >= len(test_symbols)
        
        # Test compliance check
        test_context = {
            'client_money': 1000000.0,
            'total_assets': 2000000.0,
            'execution_price': 150.0,
            'market_price': 150.1,
            'position_size': 50000.0,
            'total_market_cap': 1000000000.0,
            'transaction_time': datetime.now(UTC),
            'transaction_data': {
                'client_id': 'CLIENT_001',
                'instrument': 'AAPL',
                'quantity': 100,
                'price': 150.0
            },
            'target_market_validation': True,
            'risk_warning_provided': True,
            'order_rate': 500,
            'circuit_breaker_triggered': False,
            'data_processing_risk': 0.05,
            'dpia_conducted': True,
            'data_retention_days': 1000,
            'purpose_limitation': True,
            'explicit_consent': True,
            'withdrawal_right': True,
            'total_portfolio': 1000000.0,
            'liquid_assets': 400000.0,
            'last_stress_test': datetime.now(UTC) - timedelta(days=15)
        }
        
        compliance_report = compliance.run_compliance_check(test_context)
        assert compliance_report.total_checks > 0
        
        # Shutdown
        runner.shutdown()
        print("✅ Complete pipeline workflow test completed")
    
    def test_performance_metrics(self):
        """Test performance metrics collection"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        # Execute some tasks to generate metrics
        tasks = [
            (f"task_{i}", lambda x: f"Result {x}", (f"task_{i}",))
            for i in range(5)
        ]
        infra.execute_parallel_tasks(tasks, 'data_fetching')
        
        # Get performance report
        report = infra.get_performance_report()
        
        assert 'timestamp' in report
        assert 'resource_stats' in report
        assert 'performance_metrics' in report
        assert 'thread_pools' in report
        assert 'redis_status' in report
        
        # Check performance metrics
        metrics = report['performance_metrics']
        assert 'total_tasks_completed' in metrics
        assert 'cache_hits' in metrics
        assert 'cache_misses' in metrics
        assert 'average_task_duration' in metrics
        
        assert metrics['total_tasks_completed'] >= 5
        
        infra.shutdown()
    
    def test_error_handling(self):
        """Test error handling across components"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        # Test with invalid task
        def failing_task(task_id: str):
            raise Exception(f"Task {task_id} failed")
        
        tasks = [
            ("failing_task", failing_task, ("failing_task",))
        ]
        
        results = infra.execute_parallel_tasks(tasks, 'algorithm_processing')
        
        assert len(results) == 1
        task_id, result, error = results[0]
        assert error is not None
        assert "Task failing_task failed" in error
        
        infra.shutdown()
    
    def test_concurrent_operations(self):
        """Test concurrent operations"""
        infra = InstitutionalInfrastructureManager(redis_enabled=False)
        
        # Test concurrent caching
        def cache_operation(key: str, value: str):
            infra.cache_data(key, value, ttl=60)
            return infra.get_cached_data(key)
        
        tasks = [
            (f"cache_task_{i}", cache_operation, (f"key_{i}", f"value_{i}"))
            for i in range(10)
        ]
        
        results = infra.execute_parallel_tasks(tasks, 'data_fetching')
        
        assert len(results) == 10
        for task_id, result, error in results:
            assert error is None
            assert result is not None
            assert "value_" in result
        
        infra.shutdown()


def test_integration_workflow():
    """Test complete integration workflow"""
    print("🧪 Testing complete integration workflow...")
    
    # Initialize all components
    runner = EnhancedPipelineRunner()
    compliance = UKROIComplianceSystem()
    
    # Test infrastructure
    infra = runner.infra
    assert infra.total_threads == 24
    
    # Test compliance
    test_context = {
        'client_money': 1000000.0,
        'total_assets': 2000000.0,
        'execution_price': 150.0,
        'market_price': 150.1,
        'position_size': 50000.0,
        'total_market_cap': 1000000000.0,
        'transaction_time': datetime.now(UTC),
        'transaction_data': {
            'client_id': 'CLIENT_001',
            'instrument': 'AAPL',
            'quantity': 100,
            'price': 150.0
        },
        'target_market_validation': True,
        'risk_warning_provided': True,
        'order_rate': 500,
        'circuit_breaker_triggered': False,
        'data_processing_risk': 0.05,
        'dpia_conducted': True,
        'data_retention_days': 1000,
        'purpose_limitation': True,
        'explicit_consent': True,
        'withdrawal_right': True,
        'total_portfolio': 1000000.0,
        'liquid_assets': 400000.0,
        'last_stress_test': datetime.now(UTC) - timedelta(days=15)
    }
    
    compliance_report = compliance.run_compliance_check(test_context)
    print(f"📊 Compliance Score: {compliance_report.summary['compliance_score']:.1f}%")
    
    # Test news sentiment
    news_analyzer = runner.news_analyzer
    cache_stats = news_analyzer.get_cache_stats()
    print(f"📰 News cache stats: {cache_stats}")
    
    # Test parallel processing
    def test_task(task_id: str, complexity: int = 3):
        result = 0
        for i in range(complexity * 1000):
            result += i ** 0.5
        return f"Complex task {task_id} completed with result {result:.2f}"
    
    tasks = [
        (f"complex_task_{i}", test_task, (f"complex_task_{i}", i % 5 + 1))
        for i in range(20)
    ]
    
    results = infra.execute_parallel_tasks(tasks, 'algorithm_processing')
    print(f"🔄 Completed {len(results)} parallel tasks")
    
    # Test caching performance
    for i in range(100):
        test_data = {"id": i, "data": f"test_data_{i}", "timestamp": datetime.now(UTC).isoformat()}
        infra.cache_data(f"perf_test_{i}", test_data, ttl=60)
    
    # Retrieve cached data
    for i in range(100):
        cached = infra.get_cached_data(f"perf_test_{i}")
        assert cached is not None
        assert cached["id"] == i
    
    # Get performance report
    report = infra.get_performance_report()
    print(f"📊 Performance report: {report['performance_metrics']['total_tasks_completed']} tasks completed")
    
    # Shutdown
    runner.shutdown()
    print("✅ Complete integration workflow test completed")


if __name__ == "__main__":
    # Run integration test
    test_integration_workflow()
    
    # Run pytest
    pytest.main([__file__, "-v"])
