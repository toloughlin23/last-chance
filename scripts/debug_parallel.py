#!/usr/bin/env python3
"""
Debug parallel execution issue
"""

import sys
sys.path.append('.')

from services.infrastructure_manager import InstitutionalInfrastructureManager

def test_func(a, b, c):
    print(f'a={a}, b={b}, c={c}')
    print(f'a type: {type(a)}')
    print(f'b type: {type(b)}')
    print(f'c type: {type(c)}')
    return 'test'

def main():
    infra = InstitutionalInfrastructureManager(redis_enabled=False)
    
    tasks = [
        ('task1', test_func, ('arg1', 'arg2', 'arg3'))
    ]
    
    results = infra.execute_parallel_tasks(tasks, 'algorithm_processing')
    print(f'Results: {results}')
    
    infra.shutdown()

if __name__ == "__main__":
    main()
