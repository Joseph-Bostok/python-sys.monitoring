# How to Run and Test Everything

## Quick Start (Recommended)

### Interactive Test
```bash
cd /home/jbostok/cProfiler/modified_lib
./simple_run.sh
```

When prompted, enter a number for the fibonacci sequence (try 30-35 for visible timing results).

### Full Automated Test
```bash
cd /home/jbostok/cProfiler/modified_lib
./run_test.sh
```

This runs all tests automatically without user input.

## What's Happening Behind the Scenes

1. **Modified Library Location**:
   - `/home/jbostok/cProfiler/modified_lib/_lsprof.cpython-312-x86_64-linux-gnu.so`

2. **Patched Python Being Used**:
   - `/home/jbostok/cProfiler/cpython/python` (version 3.12.7)

3. **The library is loaded via PYTHONPATH**:
   - The patched Python automatically finds the modified `_lsprof.so` in the current directory

## Manual Commands

### Run profiling with any N value:
```bash
cd /home/jbostok/cProfiler/modified_lib

# Interactive mode
/home/jbostok/cProfiler/cpython/python -m cProfile -s cumulative test_modified_lsprof.py

# Save profile data to file
/home/jbostok/cProfiler/cpython/python -m cProfile -o my_profile.dat test_modified_lsprof.py
```

### Analyze saved profile data:
```bash
# Interactive pstats shell
/home/jbostok/cProfiler/cpython/python -m pstats test_stats.dat

# Common commands inside pstats:
# - sort cumulative    (sort by cumulative time)
# - stats 20           (show top 20 functions)
# - stats fibonacci    (show only fibonacci function)
# - quit               (exit)
```

### Quick analysis from command line:
```bash
/home/jbostok/cProfiler/cpython/python << 'EOF'
import pstats
p = pstats.Stats('test_stats.dat')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
p.print_stats('fibonacci')
EOF
```

## Profile Your Own Python Code

```bash
cd /home/jbostok/cProfiler/modified_lib

# Profile any script
/home/jbostok/cProfiler/cpython/python -m cProfile -o output.dat /path/to/your_script.py

# Analyze it
/home/jbostok/cProfiler/cpython/python -m pstats output.dat
```

## Understanding the Output

When you run cProfile, you'll see output like:

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    21891    0.005    0.000    0.005    0.000 test.py:21(fibonacci)
```

- **ncalls**: Number of times the function was called (21,891 times for fib(30))
- **tottime**: Total time spent in THIS function only (excluding subcalls)
- **percall**: tottime / ncalls (average time per call)
- **cumtime**: Cumulative time (including all subcalls)
- **percall**: cumtime / primitive calls

## Testing Different Fibonacci Values

For fibonacci(N), the number of function calls grows exponentially:
- fibonacci(20): 21,891 calls
- fibonacci(25): 242,785 calls
- fibonacci(30): 2,692,537 calls
- fibonacci(35): 29,860,703 calls (takes several seconds)

Try different values to see how cProfile tracks the timing!

## Next Step: Adding Debug Output to See Internals

To see HOW cProfile calculates time internally, you can add printf statements to the source code.

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions on modifying `_lsprof.c` to print debug information.

## Files in This Directory

- `_lsprof.cpython-312-x86_64-linux-gnu.so` - Modified profiler library
- `test_modified_lsprof.py` - Test script with fibonacci and primes
- `simple_run.sh` - Interactive test runner
- `run_test.sh` - Full automated test suite
- `HOW_TO_RUN.md` - This file
- `QUICKSTART.md` - Detailed guide for modifying source code
- `README.md` - Technical analysis of how cProfile works
- `test_stats.dat` - Generated profile data (after running tests)

## Troubleshooting

**Q: I get "command not found" for the patched Python**
A: Check that `/home/jbostok/cProfiler/cpython/python` exists. If not, you need to build CPython first.

**Q: The modified library isn't being loaded**
A: Make sure you're in the `/home/jbostok/cProfiler/modified_lib` directory when running, or set PYTHONPATH explicitly:
```bash
export PYTHONPATH=/home/jbostok/cProfiler/modified_lib:$PYTHONPATH
```

**Q: I want to see more detailed timing**
A: Use larger fibonacci numbers (30-35) or modify the source code to add printf debugging (see QUICKSTART.md).

## Reference

From your meeting notes (1/13):
- ✅ Located `_lsprof.cpython-312-x86_64-linux-gnu.so`
- ✅ Put it in a dedicated folder
- ✅ Set up to use with patched Python (via PYTHONPATH)
- ✅ Can now test and see function timing
- ✅ Figured out how cProfile calculates time (accumulates time differences)
