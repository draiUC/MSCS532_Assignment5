"""
main.py
============
Assignment 5 — Quicksort: Implementation, Analysis, and Randomization

Provides:
    quicksort(arr)             – Deterministic Quicksort (last-element pivot)
    randomized_quicksort(arr)  – Randomized Quicksort (random pivot)
    run_empirical_analysis()   – Prints timing results for both variants

Usage:
    python main.py
"""

import random
import sys
import time

sys.setrecursionlimit(100_000)


# ─── 1. Deterministic Quicksort ───────────────────────────────────────────
def quicksort(arr: list) -> list:
    """
    Deterministic Quicksort using the last element as the pivot.

    Algorithm:
        1. Base case: return arrays of length 0 or 1 unchanged.
        2. Select pivot as the last element of the subarray.
        3. Partition remaining elements into 'less' (≤ pivot) and
           'greater' (> pivot) using list comprehensions.
        4. Recursively sort each partition and concatenate.

    Complexity:
        Best-case  time  : O(n log n)  – perfectly balanced splits
        Average    time  : O(n log n)  – expected over random permutations
        Worst-case time  : O(n²)       – sorted / reverse-sorted input
        Space            : O(log n) average stack depth (O(n) worst case)

    Args:
        arr: list of comparable elements (not modified in place)

    Returns:
        A new sorted list.
    """
    if len(arr) <= 1:
        return arr

    pivot   = arr[-1]
    less    = [x for x in arr[:-1] if x <= pivot]
    greater = [x for x in arr[:-1] if x  > pivot]

    return quicksort(less) + [pivot] + quicksort(greater)


# ─── 2. Randomized Quicksort ──────────────────────────────────────────────
def randomized_quicksort(arr: list) -> list:
    """
    Randomized Quicksort: pivot chosen uniformly at random.

    Algorithm:
        1. Base case: return arrays of length 0 or 1 unchanged.
        2. Select a pivot index uniformly at random in [0, len(arr)-1].
        3. Remove the pivot from the array.
        4. Partition remaining elements into 'less' (≤ pivot) and
           'greater' (> pivot).
        5. Recursively sort each partition and concatenate.

    Complexity:
        Expected time  : O(n log n)  – for ALL input orderings
        Worst-case     : O(n²)       – probability decreases exponentially
        Space          : O(log n) expected stack depth

    The randomization ensures no fixed input can deterministically trigger
    the worst case; the expected number of comparisons is ≈ 2n ln n.

    Args:
        arr: list of comparable elements (not modified in place)

    Returns:
        A new sorted list.
    """
    if len(arr) <= 1:
        return arr

    pivot_idx    = random.randint(0, len(arr) - 1)
    pivot        = arr[pivot_idx]
    arr_no_pivot = arr[:pivot_idx] + arr[pivot_idx + 1:]

    less    = [x for x in arr_no_pivot if x <= pivot]
    greater = [x for x in arr_no_pivot if x  > pivot]

    return randomized_quicksort(less) + [pivot] + randomized_quicksort(greater)


# ─── 3. Empirical timing helper ───────────────────────────────────────────
def _time_sort(func, data: list, reps: int = 5) -> float:
    """Return the mean elapsed time (seconds) over `reps` repetitions."""
    total = 0.0
    for _ in range(reps):
        arr = data[:]                       # fresh copy each run
        t0  = time.perf_counter()
        func(arr)
        total += time.perf_counter() - t0
    return total / reps


def run_empirical_analysis() -> None:
    """
    Compare deterministic vs. randomized Quicksort across:
        - Input sizes : [100, 500, 1000, 2500, 5000]
        - Distributions: random, sorted, reverse-sorted
    Results are printed to stdout in milliseconds.
    """
    sizes         = [100, 500, 1_000, 2_500, 5_000]
    distributions = {
        "random":         lambda n: [random.randint(0, n * 10) for _ in range(n)],
        "sorted":         lambda n: list(range(n)),
        "reverse-sorted": lambda n: list(range(n, 0, -1)),
    }

    print("=" * 70)
    print("Empirical Analysis: Deterministic vs. Randomized Quicksort")
    print("=" * 70)
    print(f"{'Distribution':<16} {'n':>6}  {'Det (ms)':>10}  {'Rand (ms)':>10}  {'Speedup':>8}")
    print("-" * 70)

    for dist_name, gen in distributions.items():
        for n in sizes:
            data  = gen(n)
            det_t  = _time_sort(quicksort,            data) * 1_000
            rand_t = _time_sort(randomized_quicksort, data) * 1_000
            speedup = det_t / rand_t if rand_t > 0 else float("inf")
            print(f"{dist_name:<16} {n:>6}  {det_t:>10.3f}  {rand_t:>10.3f}  {speedup:>7.1f}x")
        print()


# ─── 4. Correctness smoke test ────────────────────────────────────────────
def _smoke_test() -> None:
    test_cases = [
        [],
        [42],
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],
        list(range(20, 0, -1)),
        [7] * 10,
    ]
    for tc in test_cases:
        expected = sorted(tc)
        assert quicksort(tc)            == expected, f"Det failed on {tc}"
        assert randomized_quicksort(tc) == expected, f"Rand failed on {tc}"
    print("All smoke tests passed.\n")


# ─── Entry point ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    _smoke_test()
    run_empirical_analysis()
