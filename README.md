# Assignment 5 — Quicksort: Implementation, Analysis, and Randomization

## Repository Contents

| File | Description |
|------|-------------|
| `main.py` | Deterministic and Randomized Quicksort implementations |
| `Assignment5.docx` | APA-format paper: implementation, complexity analysis, empirical results |

---

## Requirements

- Python 3.8 or later  
- No third-party packages required (uses only `random`, `time`, `sys` from the standard library)

---

## How to Run

### 1. Correctness check + empirical analysis (combined)

```bash
python main.py
```

Expected output (measured on Windows 11):

```
All smoke tests passed.

======================================================================
Empirical Analysis: Deterministic vs. Randomized Quicksort
======================================================================
Distribution          n     Det (ms)   Rand (ms)   Speedup
----------------------------------------------------------------------
random              100        0.135       0.121      1.1x
random              500        0.578       0.739      0.8x
random             1000        2.226       1.942      1.1x
random             2500        4.203      13.915      0.3x
random             5000        7.250       9.407      0.8x

sorted              100        0.542       0.112      4.8x
sorted              500       11.430       0.797     14.3x
sorted             1000       40.688       1.650     24.7x
sorted             2500      264.234       4.152     63.6x
sorted             5000     1763.552      18.108     97.4x

reverse-sorted      100        0.818       0.249      3.3x
reverse-sorted      500       23.782       1.374     17.3x
reverse-sorted     1000       79.827       2.795     28.6x
reverse-sorted     2500      464.436       8.057     57.6x
reverse-sorted     5000     1920.496      17.583    109.2x
```

### 2. Function where test data is passed in

```python
from quicksort import quicksort, randomized_quicksort

data = [5, 3, 8, 1, 9, 2]
print(quicksort(data))             # [1, 2, 3, 5, 8, 9]
print(randomized_quicksort(data))  # [1, 2, 3, 5, 8, 9]
```

---

## Summary of Findings

Results measured on Windows 11 (Intel CPU), Python 3.x, 5 repetitions averaged.

| Input Distribution | Deterministic (n=5,000) | Randomized (n=5,000) | Speedup |
|--------------------|------------------------|----------------------|---------|
| Random             | 7.3 ms                 | 9.4 ms               | ~0.8×   |
| Sorted             | **1,763.6 ms**         | 18.1 ms              | **97×** |
| Reverse-sorted     | **1,920.5 ms**         | 17.6 ms              | **109×**|

### Key takeaways

1. **On random inputs** both implementations run in O(n log n); performance is comparable with minor variation due to OS scheduling.
2. **On sorted/reverse-sorted inputs** the deterministic variant degrades to O(n²), while the randomized variant maintains O(n log n) expected performance.
3. **Randomization is robust** — on adversarial (ordered) inputs the speedup exceeds 97–109×.
4. **Practical approach**: always use randomized pivot selection (or median-of-three) when input ordering is unknown or adversarially controlled.

---

## Complexity Reference

| Variant        | Best Case    | Average Case | Worst Case                        | Space (stack) |
|----------------|--------------|--------------|-----------------------------------|---------------|
| Deterministic  | O(n log n)   | O(n log n)   | O(n²) — triggered by ordered input| O(log n) avg  |
| Randomized     | O(n log n)   | O(n log n)   | O(n²) — exponentially unlikely    | O(log n) expected |

---

## References

- Cormen, T. H., et al. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.  
- Hoare, C. A. R. (1962). Quicksort. *The Computer Journal, 5*(1), 10–16.  
- Motwani, R., & Raghavan, P. (1995). *Randomized Algorithms*. Cambridge University Press.
