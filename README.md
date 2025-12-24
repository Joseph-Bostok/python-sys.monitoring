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

