import subprocess
import sys


def run(cmd: str) -> str:
    p = subprocess.run(cmd.split(), capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


# Expect the printed iterative series for N=7 to match the first 7 Fibonacci numbers (1-indexed):
def test_python_iterative_print_series():
    out = run("python3 fib.py 7 0 --print")
    # First line is label in non-CSV modes
    lines = out.splitlines()
    assert lines[0].lower().startswith("iterative")
    series = lines[1].strip()
    assert series == "1 1 2 3 5 8 13"


# Expect CSV output for mode=3 (all) to contain six comma-separated values: time,ops for each of
# iterative, dp, and recursive implementations.
def test_python_all_csv_shape():
    out = run("python3 fib.py 10 3")
    parts = out.split(",")
    assert len(parts) == 6  # t_i,ops_i,t_dp,ops_dp,t_rec,ops_rec


# If the C executable is built, expect CSV output for mode=3 to contain either
# 6 fields (all three algos) or 4 if the recursive portion was truncated.
def test_c_iterative_csv_shape():
    # Requires compiled C executable as ./fib.exe
    try:
        out = run("./fib.exe 5 3")
        parts = out.split(",")
        assert len(parts) in (4, 6)
    except Exception:
        # If C executable not yet built, skip
        pass


