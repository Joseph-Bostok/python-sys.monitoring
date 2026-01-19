#!/bin/bash
echo "========================================"
echo "COMPARISON: Standard vs Modified cProfile"
echo "========================================"
echo ""
echo "Running fibonacci(30) with MODIFIED cProfile (with statistics)..."
echo ""
echo "30" | /home/jbostok/cProfiler/cpython/python test_modified_lsprof.py 2>&1 | grep -A 15 "PER-CALL"
