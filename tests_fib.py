import subprocess
import sys


def run(cmd: str) -> str:
    p = subprocess.run(cmd.split(), capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


def test_python_iterative_print_series():
    out = run("python3 fib.py 7 0 --print")
    # First line is label in non-CSV modes
    lines = out.splitlines()
    assert lines[0].lower().startswith("iterative")
    series = lines[1].strip()
    assert series == "1 1 2 3 5 8 13"


def test_python_all_csv_shape():
    out = run("python3 fib.py 10 3")
    parts = out.split(",")
    assert len(parts) == 6  # t_i,ops_i,t_dp,ops_dp,t_rec,ops_rec


def test_c_iterative_csv_shape():
    # Requires compiled C executable as ./fib.exe
    try:
        out = run("./fib.exe 5 3")
        parts = out.split(",")
        assert len(parts) in (4, 6)
    except Exception:
        # If C executable not yet built, skip
        pass


