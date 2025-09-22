#!/usr/bin/env python3
"""
Performance Benchmark for Universe Provider & Selector
Measures speed, memory usage, and API efficiency
"""

import time
from datetime import date, timedelta

import psutil
from dotenv import load_dotenv

from utils.active_universe_provider import ActiveUniverseProvider


def benchmark_candidate_discovery():
    """Benchmark: Candidate discovery performance"""
    print("⚡ Benchmark 1: Candidate Discovery")
    print("-" * 50)

    provider = ActiveUniverseProvider()

    # Test different limits
    limits = [50, 100, 200, 500]
    results = []

    for limit in limits:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

        candidates = provider._discover_candidates(limit=limit)

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

        elapsed = end_time - start_time
        memory_used = end_memory - start_memory

        results.append(
            {
                "limit": limit,
                "candidates": len(candidates),
                "time": elapsed,
                "memory_mb": memory_used,
                "rate": len(candidates) / elapsed if elapsed > 0 else 0,
            }
        )

        print(
            f"  Limit {limit:3d}: {len(candidates):3d} candidates in {elapsed:.2f}s ({memory_used:.1f}MB)"
        )

    return results


def benchmark_adv_prefiltering():
    """Benchmark: ADV prefiltering performance"""
    print("\n⚡ Benchmark 2: ADV Prefiltering")
    print("-" * 50)

    provider = ActiveUniverseProvider()

    # Get candidates first
    candidates = provider._discover_candidates(limit=100)
    if not candidates:
        print("  ❌ No candidates for benchmarking")
        return []

    end_date = date.today()
    start_date = end_date - timedelta(days=60)

    # Test different batch sizes
    batch_sizes = [5, 10, 20, 50]
    results = []

    for batch_size in batch_sizes:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        _prefiltered_results = provider._prefilter_by_adv_and_price(
            candidates,
            start_date.isoformat(),
            end_date.isoformat(),
            adv_min_dollar=50_000_000,
            price_min=10.0,
            max_symbols=50,
            batch_size=batch_size,
        )

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024

        elapsed = end_time - start_time
        memory_used = end_memory - start_memory

        results.append(
            {
                "batch_size": batch_size,
                "input_candidates": len(candidates),
                "output_candidates": len(_prefiltered_results),
                "time": elapsed,
                "memory_mb": memory_used,
                "throughput": len(candidates) / elapsed if elapsed > 0 else 0,
            }
        )

        print(
            f"  Batch {batch_size:2d}: {len(candidates):3d}→{len(prefiltered):2d} in {elapsed:.2f}s ({memory_used:.1f}MB)"
        )

    return results


def benchmark_spread_calculation():
    """Benchmark: Spread calculation performance"""
    print("\n⚡ Benchmark 3: Spread Calculation")
    print("-" * 50)

    from services.quotes_client import QuotesClient

    client = QuotesClient()

    # Test with different numbers of symbols
    test_symbols = [
        "AAPL",
        "MSFT",
        "NVDA",
        "GOOGL",
        "AMZN",
        "TSLA",
        "META",
        "NFLX",
        "AMD",
        "INTC",
    ]

    results = []

    for num_symbols in [1, 3, 5, 10]:
        symbols = test_symbols[:num_symbols]

        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        spreads = []
        for symbol in symbols:
            try:
                med_dollar, med_bps = client.median_spread_over_days(symbol, days=5)
                spreads.append((symbol, med_dollar, med_bps))
            except Exception as e:
                print(f"    Error with {symbol}: {e}")

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024

        elapsed = end_time - start_time
        memory_used = end_memory - start_memory

        results.append(
            {
                "symbols": num_symbols,
                "successful": len(spreads),
                "time": elapsed,
                "memory_mb": memory_used,
                "rate": num_symbols / elapsed if elapsed > 0 else 0,
            }
        )

        print(
            f"  {num_symbols:2d} symbols: {len(spreads):2d} successful in {elapsed:.2f}s ({memory_used:.1f}MB)"
        )

    return results


def benchmark_full_pipeline():
    """Benchmark: Complete pipeline performance"""
    print("\n⚡ Benchmark 4: Full Pipeline")
    print("-" * 50)

    provider = ActiveUniverseProvider()

    # Test different target sizes
    target_sizes = [20, 50, 100, 150]
    results = []

    for target_size in target_sizes:
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024

        universe = provider.get_active_universe(
            target_size=target_size,
            analysis_days=60,
            force_refresh=True,
            batch_size=20,
        )

        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024

        elapsed = end_time - start_time
        memory_used = end_memory - start_memory

        results.append(
            {
                "target_size": target_size,
                "actual_size": len(universe),
                "time": elapsed,
                "memory_mb": memory_used,
                "efficiency": len(universe) / elapsed if elapsed > 0 else 0,
            }
        )

        print(
            f"  Target {target_size:3d}: {len(universe):3d} symbols in {elapsed:.1f}s ({memory_used:.1f}MB)"
        )

    return results


def benchmark_memory_usage():
    """Benchmark: Memory usage patterns"""
    print("\n⚡ Benchmark 5: Memory Usage")
    print("-" * 50)

    provider = ActiveUniverseProvider()

    # Monitor memory during full process
    process = psutil.Process()

    print("  Memory usage during pipeline execution:")

    # Initial memory
    initial_memory = process.memory_info().rss / 1024 / 1024
    print(f"    Initial: {initial_memory:.1f} MB")

    # After candidate discovery
    candidates = provider._discover_candidates(limit=200)
    after_discovery = process.memory_info().rss / 1024 / 1024
    print(
        f"    After discovery: {after_discovery:.1f} MB (+{after_discovery - initial_memory:.1f})"
    )

    # After prefiltering
    end_date = date.today()
    start_date = end_date - timedelta(days=60)
        _prefiltered_results = provider._prefilter_by_adv_and_price(
        candidates,
        start_date.isoformat(),
        end_date.isoformat(),
        adv_min_dollar=50_000_000,
        price_min=10.0,
        max_symbols=100,
        batch_size=20,
    )
    after_prefilter = process.memory_info().rss / 1024 / 1024
        print(
            f"    After prefilter: {after_prefilter:.1f} MB (+{after_prefilter - after_discovery:.1f})"
        )

    # After full selection
    universe = provider.get_active_universe(
        target_size=100,
        analysis_days=60,
        force_refresh=True,
    )
    after_selection = process.memory_info().rss / 1024 / 1024
    print(
        f"    After selection: {after_selection:.1f} MB (+{after_selection - after_prefilter:.1f})"
    )

    total_memory_used = after_selection - initial_memory
    print(f"    Total memory used: {total_memory_used:.1f} MB")

    return {
        "initial_mb": initial_memory,
        "final_mb": after_selection,
        "total_used_mb": total_memory_used,
        "universe_size": len(universe),
    }


def benchmark_api_efficiency():
    """Benchmark: API call efficiency"""
    print("\n⚡ Benchmark 6: API Efficiency")
    print("-" * 50)

    from services.polygon_client import PolygonClient

    client = PolygonClient()

    # Test different batch sizes for API calls
    test_symbols = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]

    results = []

    for batch_size in [1, 2, 5]:
        start_time = time.time()
        api_calls = 0

        # Simulate batch processing
        for i in range(0, len(test_symbols), batch_size):
            batch = test_symbols[i : i + batch_size]

            for symbol in batch:
                try:
                    # Make a real API call
                    data = client.get_aggs(
                        symbol,
                        1,
                        "day",
                        (date.today() - timedelta(days=5)).isoformat(),
                        date.today().isoformat(),
                        limit=1,
                    )
                    api_calls += 1
                except Exception as e:
                    print(f"    API error for {symbol}: {e}")

        end_time = time.time()
        elapsed = end_time - start_time

        results.append(
            {
                "batch_size": batch_size,
                "api_calls": api_calls,
                "time": elapsed,
                "calls_per_second": api_calls / elapsed if elapsed > 0 else 0,
            }
        )

        print(
            f"  Batch {batch_size}: {api_calls} calls in {elapsed:.2f}s ({api_calls/elapsed:.1f} calls/s)"
        )

    return results


def main():
    load_dotenv()

    print("🚀 PERFORMANCE BENCHMARK SUITE")
    print("=" * 70)
    print("Measuring speed, memory, and API efficiency")
    print("=" * 70)

    benchmarks = [
        ("Candidate Discovery", benchmark_candidate_discovery),
        ("ADV Prefiltering", benchmark_adv_prefiltering),
        ("Spread Calculation", benchmark_spread_calculation),
        ("Full Pipeline", benchmark_full_pipeline),
        ("Memory Usage", benchmark_memory_usage),
        ("API Efficiency", benchmark_api_efficiency),
    ]

    all_results = {}

    for benchmark_name, benchmark_func in benchmarks:
        try:
            print(f"\n{'='*20} {benchmark_name} {'='*20}")
            results = benchmark_func()
            all_results[benchmark_name] = results
            print(f"✅ {benchmark_name} completed")
        except Exception as e:
            print(f"❌ {benchmark_name} failed: {e}")
            all_results[benchmark_name] = None

    # Summary
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)

    for benchmark_name, results in all_results.items():
        if results:
            print(f"\n📊 {benchmark_name}:")
            if isinstance(results, list) and results:
                # Show key metrics
                if "time" in results[0]:
                    times = [r["time"] for r in results]
                    print(f"  Time range: {min(times):.2f}s - {max(times):.2f}s")
                if "memory_mb" in results[0]:
                    memories = [r["memory_mb"] for r in results]
                    print(
                        f"  Memory range: {min(memories):.1f}MB - {max(memories):.1f}MB"
                    )
            elif isinstance(results, dict):
                print(f"  Results: {results}")
        else:
            print(f"\n❌ {benchmark_name}: FAILED")

    print("\n🎯 Performance testing complete!")


if __name__ == "__main__":
    main()
