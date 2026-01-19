# cProfiler - Per-Call Statistics Implementation

Modified CPython cProfile implementation with per-call statistics tracking.

## What's Here

This repository contains modifications to CPython's `_lsprof` profiler to track detailed per-call statistics including mean, standard deviation, minimum, and maximum execution times.

## Directory Structure

```
cProfiler/
├── cpython/                    # Modified CPython 3.12.7 source
│   └── Modules/_lsprof.c      # Modified profiler implementation
├── python-sys.monitoring/      # Test workloads and documentation
│   └── meeting_notes.txt      # Implementation notes and analysis
└── modified_lib/               # Built library and test scripts
    ├── _lsprof.cpython-312-x86_64-linux-gnu.so  # Modified profiler library
    ├── test_modified_lsprof.py                   # Test script
    ├── simple_run.sh                             # Quick test runner
    ├── QUICK_REFERENCE.md                        # Quick start guide
    ├── STATISTICS_GUIDE.md                       # Detailed usage guide
    └── SUMMARY.md                                # Implementation summary
```

## Features

### Per-Call Statistics Tracked

- **Mean time**: Average execution time per call
- **Standard deviation**: Variance in call times
- **Minimum time**: Fastest individual call
- **Maximum time**: Slowest individual call
- **Total time**: Cumulative time across all calls
- **Call count**: Number of function invocations

### Example Output

```
[STATS] fibonacci (/path/to/test.py)
  Calls: 2692537 | Total: 1.363806 s
  Mean: 0.000000507 s | StdDev: 0.001211962 s
  Min: 0.000000025 s | Max: 1.363805794 s
```

## Quick Start

```bash
cd modified_lib
./simple_run.sh
```

## Implementation Details

### Modified Files

- **cpython/Modules/_lsprof.c**: Core profiler implementation
  - Added `min_time`, `max_time`, `sum_squares` fields to `ProfilerEntry`
  - Track statistics on every function call
  - Calculate variance using: `Var = E[X²] - (E[X])²`
  - Auto-print stats when `profiler.disable()` is called

### Key Changes

1. Extended `ProfilerEntry` struct with statistical fields
2. Modified `Stop()` function to track per-call timing
3. Added `printStatsForEntry()` to format and display statistics
4. Integrated statistics output into profiler disable workflow

## Building from Source

```bash
cd cpython
git checkout per-call-statistics-tracking
make clean
./configure
make -j8

# Copy built library to modified_lib
cp Modules/_lsprof.cpython-312-x86_64-linux-gnu.so ../modified_lib/
```

## Usage

### With Python Scripts

```python
import cProfile

profiler = cProfile.Profile()
profiler.enable()

your_function()  # Your code here

profiler.disable()  # Statistics printed automatically!
```

### From Command Line

```bash
/path/to/patched/python -m cProfile your_script.py
```

Statistics are automatically printed to stderr when profiling ends.

## Documentation

- **QUICK_REFERENCE.md**: Quick start guide
- **STATISTICS_GUIDE.md**: Detailed usage and interpretation
- **SUMMARY.md**: Complete implementation details
- **meeting_notes.txt**: Development notes and analysis

## Branches

- **cpython**: `per-call-statistics-tracking`
- **python-sys.monitoring**: `per-call-statistics-implementation`
- **cProfiler** (this repo): `per-call-statistics`

## Requirements

- CPython 3.12.7 source code
- GCC compiler
- make
- Linux x86_64 (library is compiled for this platform)

## License

CPython components are under the PSF License.
Modifications and additional scripts are provided as-is for research and development.

## Contributing

This is a research/experimental project. The modifications are designed for profiling analysis and benchmarking.

## Contact

See meeting_notes.txt for detailed implementation notes and analysis.

---

Built with CPython 3.12.7
