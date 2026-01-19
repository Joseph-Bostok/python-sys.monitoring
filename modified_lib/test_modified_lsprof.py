#!/usr/bin/env python3
"""
Test script to verify the modified _lsprof library is being used.
This should be run with system Python (3.10) using PYTHONPATH override.
"""
import sys
import cProfile
import pstats
from io import StringIO

# Print which _lsprof is being loaded
print("Python version:", sys.version)
print("Python executable:", sys.executable)

# Try to find where _lsprof is loaded from
import _lsprof
print("_lsprof module:", _lsprof)
print("_lsprof file:", _lsprof.__file__ if hasattr(_lsprof, '__file__') else "built-in")

# Simple workload functions for testing
def fibonacci(n):
    """Calculate fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def calculate_primes(limit):
    """Calculate prime numbers up to limit."""
    primes = []
    for num in range(2, limit):
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

def main():
    """Main workload function."""
    print("\n--- Running test workload ---")

    # Get user input for fibonacci
    try:
        n = int(input("Enter N for fibonacci sequence (try 25-35 for visible timing): "))
    except (ValueError, EOFError):
        n = 25
        print(f"Using default N = {n}")

    # Test fibonacci
    result = fibonacci(n)
    print(f"fibonacci({n}) = {result}")

    # Test primes
    primes = calculate_primes(1000)
    print(f"Primes up to 1000: {len(primes)} found")

    print("--- Workload complete ---\n")

if __name__ == '__main__':
    # Profile the main function
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # Print stats
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())
