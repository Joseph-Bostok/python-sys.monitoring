#!/bin/bash
# Test script to run the modified _lsprof library

echo "==================================================================="
echo "Testing Modified _lsprof Library"
echo "==================================================================="
echo ""

# Path to patched Python 3.12
PATCHED_PYTHON="/home/jbostok/cProfiler/cpython/python"

# Check if patched Python exists
if [ ! -f "$PATCHED_PYTHON" ]; then
    echo "ERROR: Patched Python not found at $PATCHED_PYTHON"
    echo "You need to build it first. See instructions below."
    exit 1
fi

echo "Step 1: Checking Python version"
echo "-------------------------------------------------------------------"
$PATCHED_PYTHON --version
echo ""

echo "Step 2: Verifying _lsprof module location"
echo "-------------------------------------------------------------------"
$PATCHED_PYTHON -c "import _lsprof; print('_lsprof loaded from:', _lsprof.__file__ if hasattr(_lsprof, '__file__') else 'built-in')"
echo ""

echo "Step 3: Running simple cProfile test"
echo "-------------------------------------------------------------------"
$PATCHED_PYTHON -m cProfile -s cumulative test_modified_lsprof.py
echo ""

echo "Step 4: Running cProfile with output file"
echo "-------------------------------------------------------------------"
$PATCHED_PYTHON -m cProfile -o test_stats.dat test_modified_lsprof.py
echo ""

echo "Step 5: Analyzing profile stats"
echo "-------------------------------------------------------------------"
$PATCHED_PYTHON << 'PYSCRIPT'
import pstats
from pstats import SortKey

# Load the stats
p = pstats.Stats('test_stats.dat')

print("\n=== Top 10 functions by cumulative time ===")
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(10)

print("\n=== Fibonacci function calls ===")
p.print_stats('fibonacci')

print("\n=== Prime calculation function calls ===")
p.print_stats('calculate_primes')
PYSCRIPT

echo ""
echo "==================================================================="
echo "Test Complete!"
echo "==================================================================="
echo ""
echo "Generated files:"
echo "  - test_stats.dat (profile data)"
echo ""
echo "To examine stats interactively:"
echo "  $PATCHED_PYTHON -m pstats test_stats.dat"
echo ""
