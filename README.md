to run this: python .\tracer.py

PY_START fires at the start of every Python function:
It triggers immediately after the call is made.
The callee’s frame is on the stack.
No instructions from that function have executed yet.
Your callback prints:(f"PY_START : {filename}:{lineno} -> {funcname}")

So each line of output is:
filename – the file the function comes from (library.py, utils.py, etc.)
lineno – the first line number of that function definition
funcname – the function name being entered

example : 
PY_START : library.py:436 -> _del_library
PY_START : utils.py:31 -> destroy
PY_START : fake_impl.py:78 -> deregister_fake_kernel
PY_START : weakref.py:585 -> __call__
...
12/9/2025 - testing and comparing cProfile vs sys.mon on a simple pytorch program

this area `
python -m cProfile -o cprofile_stats.dat workload.py

this commands starts the cProfile as the runner, meaning we can now run the cProfile module as a script. 

pythom -m cProfile workload.py will run workload under the profiler.

12/19 update

this MUST be on python 3.12+ because it uses new sys.monintoring API. I have been using a VENV to keep everythin isolated and somewhat reproducible. if you dont, you will get an error saying something like "module 'sys' has no attributes to 'monitoring'

pytorch and numPy need to be installed to the same interpeter running the same profiling.

step 1: check python version (needs to be 3.12)
-to install python 3.12 (mac)
brew install python@3.12

-check version with 
python3.12 -V

step 2: create the VENV
cd /path/to/python-sys.monitoring

/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv

^^ this will create the VENV we need 

-to activate: source .venv/bin/activate
-to leave: deactivate

step 3: install dependecies to VENV:
-pip install torch numpy

-to check installation success: 
python -c "import sys, torch, numpy; print(sys.version); print(torch.__version__, numpy.__version__)"


step 4: run the profiler
-base profiler: python -m cProfile -o cprofile_stats.dat workload.py
-sys.monitoring profiler: python sysmon_profiler.py

you will then be able to re-run python sysmon_profiler.py to see performance changes

in the cprofiler: you can run sort cumulative, then stats 20. use "quit" to leave whenever.

all commands needed for this:

# 1) Run sys.monitoring profiler (your callbacks)
python sysmon_profiler.py

# 2) Run cProfile
python -m cProfile -o cprofile_stats.dat workload.py

# 3) Inspect cProfile results
python -m pstats cprofile_stats.dat
sort cumulative
stats 20
quit


1/6 project updates
we are using python 3.12 plus to access the sys.mon, need pytorch and numpy installed on the same interpreter the profiler runs on

# 1) workload
right now the sys.mon and cProfile give similar outputs, but need to be validated
potential plan: 
For run_workload, train_step, forward_pass, record from both:
ncalls from cProfile vs calls from sysmon.
cumtime from cProfile vs total_time from sysmon.
Compute differences (percentage error).
Deliverable:
A short table + paragraph: “here is how close sys.monitoring’s numbers are to cProfile on a PyTorch workload, and where they differ.”

# 2) evolving pylttng from stub -> C extension using LTTng-UST (linux)
this would be the first real step to using LTTNG
On a Linux machine, write a minimal C extension module pylttng that exposes trace_function_stats(...) to Python.
Inside that, define and call an LTTng-UST tracepoint (e.g. tracepoint(sysmon, function_stats, ...)) with fields:
filename, lineno, funcname, calls, total_time, avg_time, etc.
Keep the Python API identical to your current stub so sysmon_profiler.py doesn’t change at all.
Use the LTTng CLI to create a session and capture those events.
Deliverable:
A working Python script on Linux that:
Runs the same sysmon_profiler.py
Produces actual LTTng traces you can inspect with Babeltrace. (or anything else ) - this is a log viewer for LTTng and other CTF traces.
Babeltrace is basically the log viewer / converter for LTTng and other CTF traces.

# 4) babeltrace

LTTng writes traces in CTF (Common Trace Format) – that’s a binary format.

Babeltrace is a tool + library that can:

Read those CTF trace directories.

Dump them as human-readable text (like less for traces).

Convert between formats (e.g., CTF ⇄ other trace formats).

Let you write scripts that process traces programmatically (via its library bindings).

So the workflow looks like:

Your Python + pylttng + C extension emit LTTng-UST tracepoints.

LTTng records those into a CTF trace directory.

You use Babeltrace to:

Inspect events:

babeltrace /path/to/trace


Filter, grep, sort, or post-process them.

Feed them into analysis scripts (Python, etc.) if you use the library side.

sys.monitoring + pylttng = how you generate events

LTTng = how you log them efficiently

Babeltrace = how you look at and analyze those logs after the fact (including token timings, function stats, etc.).
