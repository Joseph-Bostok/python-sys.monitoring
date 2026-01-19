# Quick Reference - Modified cProfiler

## What You Have Now

A modified CPython `_lsprof` profiler that tracks:
- Mean, StdDev, Min, Max time **per function call**
- Automatically printed when profiling ends

## Run It

```bash
cd /home/jbostok/cProfiler/modified_lib

# Interactive test
./simple_run.sh

# Automated test suite
./run_test.sh

# Manual command
echo "30" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py
```

## Output Format

```
[STATS] function_name (filepath)
  Calls: N | Total: X.XXXXXX s
  Mean: X.XXXXXXXXX s | StdDev: X.XXXXXXXXX s
  Min: X.XXXXXXXXX s | Max: X.XXXXXXXXX s
```

## What the Numbers Mean

- **Calls**: Total function invocations
- **Total**: Cumulative time across all calls
- **Mean**: Average time per call (Total / Calls)
- **StdDev**: Standard deviation (shows variance)
  - Low = consistent performance
  - High = variable performance
- **Min**: Fastest single call
- **Max**: Slowest single call

## Example: fibonacci(30)

```
[STATS] fibonacci (/path/test.py)
  Calls: 2692537 | Total: 1.363806 s
  Mean: 0.000000507 s | StdDev: 0.001211962 s
  Min: 0.000000025 s | Max: 1.363805794 s
```

**Interpretation:**
- Called 2.7M times (recursive calls)
- Average call: 507 nanoseconds
- Fastest: 25ns (base case `n <= 1`)
- Slowest: 1.36s (outermost call including all recursion)
- High StdDev due to mix of fast base cases and slow recursive calls

## Use with Your Code

```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()

your_function()  # Your code here

profiler.disable()  # Stats print automatically!
```

## Files

- `_lsprof.cpython-312-x86_64-linux-gnu.so` - Modified library
- `test_modified_lsprof.py` - Test with fibonacci & primes
- `SUMMARY.md` - Complete implementation details
- `STATISTICS_GUIDE.md` - Detailed usage guide
- `HOW_TO_RUN.md` - Getting started

## Modified Source

`/home/jbostok/cProfiler/cpython/Modules/_lsprof.c`

To rebuild after changes:
```bash
cd /home/jbostok/cProfiler/cpython
make -j8
cp Modules/_lsprof.cpython-312-x86_64-linux-gnu.so /home/jbostok/cProfiler/modified_lib/
```

## Key Modifications

1. Added fields: `min_time`, `max_time`, `sum_squares`
2. Track stats on every function exit
3. Calculate variance: `E[X²] - (E[X])²`
4. Print stats when profiler disables

## Common Tasks

### See only statistics (filter debug output):
```bash
python test.py 2>&1 | grep -A 50 "PER-CALL"
```

### Save statistics to file:
```bash
python test.py 2> stats.txt
```

### Test different workload sizes:
```bash
echo "20" | python test_modified_lsprof.py  # Small
echo "30" | python test_modified_lsprof.py  # Medium
echo "35" | python test_modified_lsprof.py  # Large
```

---

**TL;DR**: Run `./simple_run.sh` to see it in action!
