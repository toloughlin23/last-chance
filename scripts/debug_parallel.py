#!/usr/bin/env python3
"""
Debug parallel execution issue
"""

import sys

sys.path.append(".")

from services.infrastructure_manager import InstitutionalInfrastructureManager


def test_func(a, b, c):
    training_logger.info(f"a={a}, b={b}, c={c}", operation="enhanced_logging")
    training_logger.info(f"a type: {type(a, operation="enhanced_logging")}")
    training_logger.info(f"b type: {type(b, operation="enhanced_logging")}")
    training_logger.info(f"c type: {type(c, operation="enhanced_logging")}")
    return "test"


def main():
    infra = InstitutionalInfrastructureManager(redis_enabled=False)

    tasks = [("task1", test_func, ("arg1", "arg2", "arg3"))]

    results = infra.execute_parallel_tasks(tasks, "algorithm_processing")
    training_logger.info(f"Results: {results}", operation="enhanced_logging")

    infra.shutdown()


if __name__ == "__main__":
    main()
