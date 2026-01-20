# Modified cProfile Library - Per-Call Statistics

Modified CPython `_lsprof` profiler with per-call statistics tracking.

## What This Does

Tracks detailed per-call statistics for every profiled function:
- **Mean time per call**: Average execution time
- **Standard deviation**: Measure of timing variance
- **Minimum time**: Fastest individual call
- **Maximum time**: Slowest individual call

## Quick Start

```bash
cd /home/jbostok/cProfiler/modified_lib
./run_test.sh
```

## Example Output

```
========================================
PER-CALL PROFILING STATISTICS
========================================
[STATS] fibonacci (test_modified_lsprof.py)
  Calls: 2692537 | Total: 1.343882 s
  Mean: 0.000000499 s | StdDev: 0.001192687 s
  Min: 0.000000025 s | Max: 1.343882405 s
========================================
```

**Interpretation**:
- **2.7M calls**: fibonacci called recursively 2.7 million times
- **Mean 499ns**: Average call takes 499 nanoseconds
- **StdDev 1.2ms**: High variance - some calls fast (base case), some slow (deep recursion)
- **Min 25ns**: Fastest call (base case `n <= 1`)
- **Max 1.34s**: Slowest call (outermost call including all recursion)

## How It Works

### Time Calculation

cProfile **accumulates** time (from `_lsprof.c:321-324`):

```c
// On function entry:
self->t0 = call_timer(pObj);  // Record start time

// On function exit:
_PyTime_t tt = call_timer(pObj) - self->t0;  // Duration = end - start
entry->tt += tt;  // ACCUMULATE to running total
```

- Uses `_PyTime_GetPerfCounter()` for nanosecond precision
- Each call: record start → calculate duration → add to cumulative total
- Not a simple timer - it's accumulation across all calls

### Statistics Calculation

**New fields in ProfilerEntry struct**:
- `min_time`: Minimum call duration
- `max_time`: Maximum call duration
- `sum_squares`: Sum of squared times for variance

**Statistics computed**:
1. **Mean**: `total_time / call_count`
2. **Variance**: `E[X²] - (E[X])²` (using sum of squares)
3. **Standard Deviation**: `√variance`
4. **Min/Max**: Tracked on every function call

### Function Grouping

Functions are grouped by their `userObj` field:
- For Python functions: `userObj` points to `PyCodeObject*`
- Function name: `code->co_name`
- Same function → same ProfilerEntry → statistics grouped together
- Uses rotating tree data structure for efficient lookup

## Files

- `_lsprof.cpython-312-x86_64-linux-gnu.so` - Modified profiler library (186 KB)
- `test_modified_lsprof.py` - Test script (fibonacci + primes)
- `run_test.sh` - Automated test runner
- `test_stats.dat` - Generated profile data (after running tests)

## Usage

### With Test Script
```bash
./run_test.sh
```

### With Your Own Code
```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()

your_function()  # Your code here

profiler.disable()  # Statistics print automatically!
```

### From Command Line
```bash
/home/jbostok/cProfiler/cpython/python -m cProfile your_script.py
```

Statistics are automatically printed to **stderr** when profiling ends.

## Modifications Made

**Source file**: `/home/jbostok/cProfiler/cpython/Modules/_lsprof.c`

**Changes**:
1. Added 3 fields to `ProfilerEntry` struct (lines 38-40)
2. Modified `Stop()` function to track min/max/sum_squares (lines 335-347)
3. Added `printStatsForEntry()` function to calculate and print stats (lines 512-556)
4. Modified `profiler_disable()` to print statistics (lines 917-922)
5. Added includes: `<stdio.h>`, `<math.h>`

**Total**: ~100 lines of C code added

## Rebuild Instructions

If you modify the source:

```bash
cd /home/jbostok/cProfiler/cpython
make -j8
cp Modules/_lsprof.cpython-312-x86_64-linux-gnu.so ../modified_lib/
```

## Technical Details

**Memory overhead**: 24 bytes per function (3 fields × 8 bytes each)
**CPU overhead**: < 1% (min/max comparisons + arithmetic)
**Precision**: Nanosecond (9 decimal places)
**Platform**: Linux x86_64, Python 3.12.7

## Understanding the Output

### Low Standard Deviation
```
Calls: 1 | Total: 0.000124 s
Mean: 0.000124 s | StdDev: 0.000000 s
```
- Single call or all calls take same time
- Consistent, predictable performance

### High Standard Deviation
```
Calls: 2692537 | Total: 1.343882 s
Mean: 0.000000499 s | StdDev: 0.001192687 s
```
- Wide variation in call times
- Common in recursive functions (fast base cases + slow deep calls)
- High variance = investigate what causes the spread

## Documentation

- **QUICK_REFERENCE.md** - Quick start guide
- **STATISTICS_GUIDE.md** - Detailed usage and interpretation
- **SUMMARY.md** - Complete implementation details
- **HOW_TO_RUN.md** - Usage instructions
- **QUICKSTART.md** - Development guide

## Git Branch

Branch: `per-call-statistics`
Commit: `9d745d8` - "Remove unnecessary status scripts"

All changes committed and ready to push to GitHub.
