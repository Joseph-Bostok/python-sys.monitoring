# Per-Call Statistics Guide

## Overview

The modified `_lsprof` library now tracks detailed per-call statistics for every function:
- **Mean** - Average time per call
- **Standard Deviation** - Variance in call times
- **Minimum** - Fastest single call
- **Maximum** - Slowest single call

## What Changed

### Added Fields to ProfilerEntry
```c
typedef struct _ProfilerEntry {
    // ... existing fields ...

    /* Per-call statistics */
    _PyTime_t min_time;   /* minimum time for a single call */
    _PyTime_t max_time;   /* maximum time for a single call */
    double sum_squares;   /* sum of squared times for variance */
} ProfilerEntry;
```

### Statistics Calculated

For each function, we track:

1. **Total Time**: Sum of all call durations
2. **Call Count**: Number of times called
3. **Mean Time**: `total_time / call_count`
4. **Sum of Squares**: `Σ(time²)` for variance calculation
5. **Variance**: `E[X²] - (E[X])²`
6. **Standard Deviation**: `√variance`
7. **Min Time**: Smallest individual call duration
8. **Max Time**: Largest individual call duration

### When Statistics Are Printed

Statistics are automatically printed to **stderr** when you call `profiler.disable()` or when profiling ends.

## Example Output

```
========================================
PER-CALL PROFILING STATISTICS
========================================
[STATS] fibonacci (/home/jbostok/cProfiler/modified_lib/test_modified_lsprof.py)
  Calls: 242785 | Total: 0.125631 s
  Mean: 0.000000517 s | StdDev: 0.000371716 s
  Min: 0.000000026 s | Max: 0.125631257 s
[STATS] calculate_primes (/home/jbostok/cProfiler/modified_lib/test_modified_lsprof.py)
  Calls: 1 | Total: 0.000128 s
  Mean: 0.000127969 s | StdDev: 0.000000000 s
  Min: 0.000127969 s | Max: 0.000127969 s
========================================
```

## Interpreting the Results

### Fibonacci Example (N=25)
```
Calls: 242785 | Total: 0.125631 s
Mean: 0.000000517 s | StdDev: 0.000371716 s
Min: 0.000000026 s | Max: 0.125631257 s
```

**What this tells you:**
- **242,785 calls**: Fibonacci was called this many times (recursive calls)
- **Mean 517 ns**: Average call takes ~517 nanoseconds
- **StdDev 0.37 ms**: High variance - some calls are very fast, some very slow
- **Min 26 ns**: Fastest call (base case: `n <= 1`)
- **Max 125 ms**: Slowest call (the initial `fibonacci(25)` that includes all recursion)

### Understanding Standard Deviation

- **Low StdDev** (~0): All calls take similar time (consistent performance)
- **High StdDev**: Wide variation in call times (like recursive functions)

For fibonacci:
- Base cases (`n <= 1`) are extremely fast (~26 ns)
- Deep recursive calls accumulate time from subcalls (up to 125 ms)
- This creates high variance → high standard deviation

## Running Tests

### Basic Test
```bash
cd /home/jbostok/cProfiler/modified_lib
./simple_run.sh
```

### See Statistics for Different Workloads

Try different fibonacci numbers to see how statistics change:

```bash
# Quick (N=20)
echo "20" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py 2>&1 | grep -A 20 "PER-CALL"

# Medium (N=30)
echo "30" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py 2>&1 | grep -A 20 "PER-CALL"

# Large (N=35) - takes a few seconds
echo "35" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py 2>&1 | grep -A 20 "PER-CALL"
```

### Redirect Statistics to File

To save just the statistics (without all the debug output):

```bash
cd /home/jbostok/cProfiler/modified_lib
echo "30" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py 2> stats_output.txt 1>/dev/null
cat stats_output.txt | grep -A 50 "PER-CALL"
```

## Use with Your Own Code

```python
import cProfile

# Your code here
def my_function():
    # ... do work ...
    pass

# Profile it
profiler = cProfile.Profile()
profiler.enable()

my_function()

profiler.disable()  # Statistics printed here automatically!
```

## Technical Details

### Time Units
- Internal: Nanoseconds (`_PyTime_t`)
- Displayed: Seconds (converted with `/1e9`)
- Precision: 9 decimal places for sub-microsecond resolution

### Variance Calculation
We use Welford's online algorithm concept:
```
variance = E[X²] - (E[X])²
         = (sum_of_squares / count) - mean²
```

This avoids numerical instability and overflow for large datasets.

### Memory Overhead
Per function:
- 3 additional fields in `ProfilerEntry`
- ~24 bytes overhead (2 × 8-byte integers + 1 × 8-byte double)
- Negligible for most use cases

## Next Steps

### Disable Debug Output

To remove the `CPROFILE PY_START:` messages, edit [_lsprof.c:628-646](/home/jbostok/cProfiler/cpython/Modules/_lsprof.c#L628-L646) and comment out the fprintf in `pystart_callback()`.

### Filter Specific Functions

To only show statistics for specific functions, modify `printStatsForEntry()` around line 540:

```c
// Only print fibonacci function
if (funcname && strcmp(funcname, "fibonacci") == 0) {
    fprintf(stderr, "[STATS] %s (%s)\n...", funcname, filename);
}
```

### Export to CSV

Modify `printStatsForEntry()` to use CSV format:

```c
fprintf(stderr, "%s,%s,%ld,%.9f,%.9f,%.9f,%.9f,%.9f\n",
        funcname, filename, entry->callcount,
        total_time_sec, mean, stddev, min_time_sec, max_time_sec);
```

Then run:
```bash
echo "30" | python test.py 2> stats.csv
```

## Troubleshooting

**Q: I don't see any statistics**
- Make sure you're calling `profiler.disable()` or the script ends normally
- Check stderr, not stdout (use `2>&1` to combine)

**Q: StdDev is 0 for some functions**
- Functions called only once have no variance
- This is mathematically correct

**Q: Min and Max are the same**
- Function was only called once
- Or all calls took exactly the same time (rare)

**Q: Stats look wrong for recursive functions**
- Min time: fastest individual call (usually base case)
- Max time: longest individual call (usually outermost call with all recursion)
- This is correct - we track every call independently
