#!/bin/bash
# Simple interactive test of modified _lsprof

PATCHED_PYTHON="/home/jbostok/cProfiler/cpython/python"

echo "==================================================================="
echo "Testing Modified _lsprof with Interactive Fibonacci"
echo "==================================================================="
echo ""

if [ ! -f "$PATCHED_PYTHON" ]; then
    echo "ERROR: Patched Python not found at $PATCHED_PYTHON"
    exit 1
fi

echo "Python version: $($PATCHED_PYTHON --version)"
echo "Modified _lsprof loaded from: /home/jbostok/cProfiler/modified_lib/"
echo ""

# Run with profiling and user input
$PATCHED_PYTHON -m cProfile -s cumulative test_modified_lsprof.py

echo ""
echo "==================================================================="
echo "Profile saved to test_stats.dat"
echo ""
echo "To analyze later, run:"
echo "  $PATCHED_PYTHON -m pstats test_stats.dat"
echo "==================================================================="
