[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/kdfTwECC)
# Midterm p1: Report on Analysis of Fibonacci Series
* **Author**: Catherine Zhang
* **GitHub Repo**: [GitHub Classroom Repo]
* **Semester**: Fall 2025
* **Languages Used**: C, Python

> You are free to rename/ modify these sections as you need (and don't forget to remove this line..)

## Overview

This report analyzes the runtime and operation counts of three Fibonacci algorithms: iterative, naive recursive, and dynamic programming (memoized and tabulation), implemented in C and Python. I provide Big O analysis with reasoning and pseudocode, then compare empirical results across algorithms and languages.

### Pseudocode and Big O

- Iterative (tabulation, series 1..n)

```
F[1] = 1; F[2] = 1
for i = 3..n:
    F[i] = F[i-1] + F[i-2]
return F[1..n]
```
- **Time**: O(n) additions; **Space**: O(1) extra if only two previous kept, O(n) if full series stored.

- Naive Recursive (Nth)

```
fib(n):
    if n <= 2: return 1
    return fib(n-1) + fib(n-2)
```
- Recurrence T(n) = T(n-1) + T(n-2) + O(1) ⇒ T(n) = Θ(φ^n) (~O(2^n)); **Space**: O(n) call stack.

- Dynamic Programming (memoized)

```
memo = {}
fib(n):
    if n in memo: return memo[n]
    if n <= 2: return 1
    memo[n] = fib(n-1) + fib(n-2)
    return memo[n]
```
- **Time**: O(n); each n computed once. **Space**: O(n) for memo.

## Empirical Data & Discussion 

I generated timing and operation CSVs using `fib_runner.py` (C and Python variants). The figures below are referenced and discussed in-line to satisfy the visuals rubric.

![C Iterative vs DP Runtime](iter_vs_dp_c.png)
Figure 1: C runtime for Iterative vs DP shows near-identical O(n) growth; minor differences from memory access patterns and function-call overhead.

![Python Iterative vs DP Runtime](iter_vs_dp_py.png)
Figure 2: Python runtime for Iterative vs DP also aligns with O(n); absolute times are higher than C due to interpreter overhead.

![C Recursive Runtime (Log Scale)](recursive_c_log.png)
Figure 3: C recursive runtime on a log scale illustrates exponential growth consistent with Θ(φ^n). DP/Iterative dominate quickly.

![Python Recursive Runtime (Log Scale)](recursive_py_log.png)
Figure 4: Python recursive runtime on a log scale exhibits even steeper observed growth due to recursion overhead and interpreter cost.

![C Operations vs N](ops_c.png)
Figure 5: C operations: Iterative and DP scale linearly; Recursive explodes exponentially until timeout thresholds.

![Python Operations vs N](ops_py.png)
Figure 6: Python operations mirror C trends; DP and Iterative differ slightly due to implementation details and cache behavior.

![Speedup Iterative (Python/C)](speedup_iter.png)
![Speedup DP (Python/C)](speedup_dp.png)
![Speedup Recursive (Python/C)](speedup_rec.png)
Figures 7–9: Cross-language speedup (Python/C). Ratios > 1 indicate Python slower than C. The gap grows with N, especially for Recursive.

Observations: function-call overhead, interpreter vs compiled execution, recursion depth limits, integer size/overflow (C `uint64_t` vs Python big ints), timer resolution, and cache warmup effects all influence absolute timings but not asymptotic trends.

## Language Analysis

### Language 1: C
Focus areas: manual memory management, fixed-width integers (`uint64_t`) and overflow considerations, `clock_gettime` timing, iterative array vs minimal-state variants, and stack vs heap for safety.

### Language 2: Python
Focus areas: `functools.lru_cache` for memoization, list-based tabulation, recursion depth and performance, dynamic big integers simplifying correctness at large N.

### Comparison and Discussion Between Experiences
Contrast ergonomics and performance; align empirical curves with Big O; discuss how language features (caching, big ints, allocation) influenced results and how I kept comparisons fair.

## Conclusions / Reflection
Key takeaways: iterative and DP are O(n) and dominate recursive at modest N; Python’s ease vs C’s speed; pitfalls (overflow, recursion limits) and how they change interpretation. Future work: fast doubling, matrix exponentiation.

## Reproduction & Usage

### Build & Run (C)

```
# compile (macOS/clang)
cc -O2 -std=c11 fib.c -o fib.exe

# CSV line: all three (iterative, dp, recursive)
./fib.exe 30 3

# CSV line: iterative and dp only (for larger N)
./fib.exe 50000 4

# Human-readable iterative with series print
./fib.exe 10 0 print
```

### Run (Python)

```
python3 fib.py 30 3          # CSV all three
python3 fib.py 50000 4       # CSV iterative + dp
python3 fib.py 10 0 --print  # iterative with series printed
```

### Batch Collection

```
# C
python3 fib_runner.py 200 --step 5 --out fib_c.csv --exec "./fib.exe"

# Python
python3 fib_runner.py 200 --step 5 --out fib_py.csv --exec "python3 fib.py"
```

Create plots from `timings_*.csv` and `ops_*.csv` and include them in this README.

## References
- ACM format references will be added in final draft (algorithm texts, language docs).

