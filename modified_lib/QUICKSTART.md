# Quick Start Guide - Testing Modified _lsprof

## ✅ Everything is already set up and working!

The test confirms your modified `_lsprof` library is loaded correctly.

## Run the Test Now

```bash
cd /home/jbostok/cProfiler/modified_lib
./run_test.sh
```

This will:
1. Verify Python 3.12.7 is running
2. Confirm the modified `_lsprof` library is loaded
3. Run cProfile on test functions (fibonacci, primes)
4. Generate `test_stats.dat` with profiling data
5. Show detailed statistics for specific functions

## Manual Testing Commands

### Basic profiling:
```bash
cd /home/jbostok/cProfiler/modified_lib

# Run with profiling output to screen
/home/jbostok/cProfiler/cpython/python -m cProfile -s cumulative test_modified_lsprof.py

# Save to file for later analysis
/home/jbostok/cProfiler/cpython/python -m cProfile -o my_stats.dat test_modified_lsprof.py
```

### Analyze saved profile data:
```bash
# Interactive mode
/home/jbostok/cProfiler/cpython/python -m pstats test_stats.dat

# Then type these commands:
# sort cumulative
# stats 20
# stats fibonacci
# quit
```

### Programmatic analysis:
```bash
/home/jbostok/cProfiler/cpython/python << 'EOF'
import pstats
p = pstats.Stats('test_stats.dat')
p.strip_dirs().sort_stats('cumulative').print_stats(10)
p.print_stats('fibonacci')
EOF
```

## Profile Your Own Code

Create any Python script and run it with:
```bash
/home/jbostok/cProfiler/cpython/python -m cProfile -o output.dat your_script.py
```

## Next Steps - Adding Debug Output

To see timing details for specific functions, modify the `_lsprof.c` source:

### 1. Edit the source file:
```bash
# Open in your editor
code /home/jbostok/cProfiler/cpython/Modules/_lsprof.c
# or
vim /home/jbostok/cProfiler/cpython/Modules/_lsprof.c
```

### 2. Find line ~321 (the `Stop` function) and add debugging:
```c
static void
Stop(ProfilerObject *pObj, ProfilerContext *self, ProfilerEntry *entry)
{
    _PyTime_t tt = call_timer(pObj) - self->t0;
    _PyTime_t it = tt - self->subt;

    // ADD THIS DEBUG CODE:
    if (entry->userObj && PyCode_Check(entry->userObj)) {
        PyCodeObject *code = (PyCodeObject *)entry->userObj;
        const char *fname = PyUnicode_AsUTF8(code->co_name);

        // Print for specific function (change "fibonacci" to any function you want)
        if (strcmp(fname, "fibonacci") == 0) {
            printf("[DEBUG] Function: %s | TotalTime: %lld ns | InlineTime: %lld ns | CallCount: %ld\n",
                   fname, (long long)tt, (long long)it, entry->callcount + 1);
        }
    }

    if (self->previous)
        self->previous->subt += tt;
    // ... rest of function
```

### 3. Rebuild CPython:
```bash
cd /home/jbostok/cProfiler/cpython
make -j8

# Copy the new library (optional, already in PYTHONPATH)
cp Modules/_lsprof.cpython-312-x86_64-linux-gnu.so /home/jbostok/cProfiler/modified_lib/
```

### 4. Run test again to see debug output:
```bash
cd /home/jbostok/cProfiler/modified_lib
./run_test.sh
```

You'll now see real-time timing information printed for the `fibonacci` function!

## Understanding the Output

- **ncalls**: Number of times function was called
- **tottime**: Total time in function (excluding subcalls)
- **percall**: tottime/ncalls
- **cumtime**: Cumulative time (including subcalls)
- **percall**: cumtime/primitive calls

## Files Generated

- `test_stats.dat` - Profile data from test script
- Any `*.dat` files you create with `-o` flag

## Useful Paths

- **Patched Python**: `/home/jbostok/cProfiler/cpython/python`
- **Modified _lsprof**: `/home/jbostok/cProfiler/modified_lib/_lsprof.cpython-312-x86_64-linux-gnu.so`
- **Source code**: `/home/jbostok/cProfiler/cpython/Modules/_lsprof.c`
- **Test workload**: `/home/jbostok/cProfiler/python-sys.monitoring/workload.py`
