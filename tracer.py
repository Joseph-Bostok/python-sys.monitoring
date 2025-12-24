# tracer.py
import sys
import os

mon = sys.monitoring
E = mon.events
TOOL_ID = mon.DEBUGGER_ID


def init_monitoring():
    mon.use_tool_id(TOOL_ID, "py_sysmon_probe")
    mon.set_events(TOOL_ID, E.PY_START)

    def on_py_start(code, instruction_offset):
        filename = os.path.basename(code.co_filename)
        funcname = code.co_name
        lineno = code.co_firstlineno

        print(f"PY_START : {filename}:{lineno} -> {funcname}")

    mon.register_callback(TOOL_ID, E.PY_START, on_py_start)


def run_workload():
    # put the thing you want to trace/profile here: torch, LLM, etc.
    import torch

    x = torch.randn(2, 2)
    y = torch.nn.functional.relu(x)
    return y


def main():
    init_monitoring()
    run_workload()


if __name__ == "__main__":
    main()
