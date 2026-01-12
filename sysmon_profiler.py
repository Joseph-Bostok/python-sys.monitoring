    # add a way to get the number of functions being 
    # and print it out in the end of the program, maybe create a hastable that stores the function with the call time and function count
    # each time its called, add time, or record each time its called. 
    # in the hash table, we know how many times its called, and total time, STDDEV, and highest / lowest time that the function is executed
    # key is function name, value is time and counter

    # try to find a way to separate the workload from the profiler, so that we can run the workload multiple times
    # and average the results. no neeed to change the tool every time we run the workload.
    # (1/6)try a different approach with line numbers, try to use a different identifier when working with mulitple files.
    # how to measure overhead, and see how it differs between other data structures.
    # maybe use a different approach to measure time, like time.perf_counter() or time.process_time()
    # hashtable should not have string as key, needs to be unqieu function identifier, string is not efficient. maybe use integer number, 
    # maybe can use array or other data strcuture to make it more efficient.
    # if we need to connect the profiling with LTTNG since itd in c, then we need to use sys mon, we need to go through the process of calling the functins through c
    #


import sys
import os
import time
from collections import defaultdict
from pathlib import Path
from math import sqrt

from workload import run_workload

mon = sys.monitoring
E = mon.events
TOOL_ID = mon.DEBUGGER_ID


stats = defaultdict(lambda: {
    "calls": 0, # number of times the function is called
    "mean": 0.0,   # mean time of the function calls
    "stddev": 0.0, # standard deviation of the function call times
    "M2": 0.0, # used in Welford's method for computing variance
    "min": float('inf'), # minimum time of the function calls
    "max": 0.0 # maximum time of the function calls
})

#call_stack: list of (code, start_time)
call_stack = []

PROJECT_FILE = Path(__file__).with_name("workload.py").resolve()

def start_handler(code, offset):
    #only profile functions defined in workload.py
    if Path(code.co_filename).resolve() != PROJECT_FILE:
        return

    start = time.perf_counter()
    call_stack.append((code, start))

def return_handler(code, offset, retval):
    # only profile functions defined in workload.py
    if Path(code.co_filename).resolve() != PROJECT_FILE:
        return

    end = time.perf_counter()
    if not call_stack:
        return
    c, start = call_stack.pop()
    if c is not code:
        return

    duration = end - start

    entry = stats[code]
    entry["calls"] += 1

    #online mean / variance method (welford)
    if entry["calls"] == 1:
        entry["mean"] = duration
        entry["M2"] = 0.0
        entry["min"] = duration
        entry["max"] = duration
    else:
        if duration < entry["min"]:
            entry["min"] = duration
        if duration > entry["max"]:
            entry["max"] = duration

        delta = duration - entry["mean"]
        entry["mean"] += delta / entry["calls"]
        entry["M2"] += delta * (duration - entry["mean"])

def init_monitoring():
    mon.use_tool_id(TOOL_ID, "sysmon_profiler")
    mon.register_callback(TOOL_ID, E.PY_START, start_handler)
    mon.register_callback(TOOL_ID, E.PY_RETURN, return_handler)
    mon.set_events(TOOL_ID, E.PY_START | E.PY_RETURN)

def main():
    init_monitoring()

    NUM_RUNS = 50
    for _ in range(NUM_RUNS):
        run_workload()
        if call_stack:
            call_stack.clear()

    #build summary rows
    rows = []
    for code, entry in stats.items():
        calls = entry["calls"]
        if calls == 0:
            continue

        mean = entry["mean"]
        total_time = mean * calls
        variance = entry["M2"] / (calls - 1) if calls > 1 else 0.0
        stddev = sqrt(variance)
        min_time = entry["min"]
        max_time = entry["max"]

        filename = os.path.basename(code.co_filename)
        funcname = code.co_name
        lineno = code.co_firstlineno

        rows.append((total_time, calls, mean, stddev, entry["min"], entry["max"], filename, funcname, lineno))

        #sort rows by total time
        rows.sort(reverse=True, key = lambda r: r[0])

        # Header similar to cProfile
        print(f"{'calls':>7} {'total':>10} {'avg':>10} {'stddev':>10} {'min':>10} {'max':>10}  function")
        for total, calls, mean, stddev, mn, mx, filename, lineno, funcname in rows[:40]:
            print(
                f"{calls:7d} "
                f"{total:10.6f} {mean:10.6f} {stddev:10.6f} "
                f"{mn:10.6f} {mx:10.6f}  "
                f"{filename}:{lineno}({funcname})"
                )

    # Overall counts
    num_functions = len(rows)
    print()
    total_calls = sum(r[1] for r in rows)
    print(f"Total distinct functions profiled: {num_functions}")
    print(f"Total function calls observed:    {total_calls}")

if __name__ == "__main__":
    main()