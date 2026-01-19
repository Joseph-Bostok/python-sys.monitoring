
## Analysis Summary (Added 1/19/2026)

### How cProfile Calculates Time

Based on analysis of `_lsprof.c`:

**Timer Source** (line 130):
- Uses `_PyTime_GetPerfCounter()` - high-resolution monotonic clock

**Time Accumulation** (lines 315-324):
```c
// On function entry:
self->t0 = call_timer(pObj);  // Record start time

// On function exit:
_PyTime_t tt = call_timer(pObj) - self->t0;  // Total = end - start
_PyTime_t it = tt - self->subt;              // Inline = total - subcalls
if (self->previous)
    self->previous->subt += tt;              // Add to parent's subcall time
```

**Answer**: cProfile **accumulates** time. Each invocation adds (end - start) to running totals.

### Key Data Structures

**ProfilerEntry** (lines 26-35):
- `tt`: Total time including subcalls
- `it`: Inline time excluding subcalls  
- `callcount`: Number of times called
- `recursivecallcount`: Recursive calls
- `userObj`: PyCodeObject or descriptive string (function identifier)

### Function Grouping/Comparison

To find where functions are compared for grouping, search for:
```bash
cd /home/jbostok/cProfiler/cpython/Modules
grep -n "rotating_tree\|_enter_call\|userObj" _lsprof.c
```

The `userObj` field is the key - it's a PyObject* that identifies the function.
Functions are grouped by this object (same function = same ProfilerEntry).

### Adding Debug Output

To print information for specific functions, modify `_lsprof.c` around line 321:

```c
_PyTime_t tt = call_timer(pObj) - self->t0;
_PyTime_t it = tt - self->subt;

// Add debugging for specific function
if (entry->userObj && PyCode_Check(entry->userObj)) {
    PyCodeObject *code = (PyCodeObject *)entry->userObj;
    // Print for specific function name
    if (strcmp(PyUnicode_AsUTF8(code->co_name), "fibonacci") == 0) {
        printf("Function: %s, TotalTime: %lld, InlineTime: %lld, Calls: %ld\n",
               PyUnicode_AsUTF8(code->co_name), tt, it, entry->callcount);
    }
}
```

Then rebuild:
```bash
cd /home/jbostok/cProfiler/cpython && make -j8
```

## Latest Modifications - 1/19/2026

### Per-Call Statistics Implementation

The library now tracks detailed per-call statistics for every profiled function:

**New Statistics Available:**
- **Mean time per call**: Average execution time
- **Standard deviation**: Measure of timing variance
- **Minimum time**: Fastest individual call
- **Maximum time**: Slowest individual call

**Output Example:**
```
[STATS] fibonacci (/path/to/test.py)
  Calls: 2692537 | Total: 1.363806 s
  Mean: 0.000000507 s | StdDev: 0.001211962 s
  Min: 0.000000025 s | Max: 1.363805794 s
```

**How It Works:**
- Tracks min/max time for every call (including recursive)
- Calculates variance using sum of squares: Var = E[X²] - (E[X])²
- Prints statistics automatically when profiler.disable() is called
- All data printed to stderr for easy filtering

**See STATISTICS_GUIDE.md for complete details.**
