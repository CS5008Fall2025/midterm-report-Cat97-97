"""
Generate advanced visualizations for Fibonacci empirical data.

Inputs: timings_*.csv and ops_*.csv produced by fib_runner.py.
Outputs: PNG figures saved in the repo for embedding in README.
"""

import csv
from pathlib import Path
from typing import List, Dict
import math
import matplotlib.pyplot as plt


ROOT = Path(__file__).parent


def read_csv(path: Path) -> List[Dict[str, str]]:
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def parse_series(rows: List[Dict[str, str]]):
    n = [int(r["N"]) for r in rows]
    it = [float(r["Iterative"]) if r["Iterative"] != "-" else math.nan for r in rows]
    dp = [float(r["Dynamic Programming"]) if r["Dynamic Programming"] != "-" else math.nan for r in rows]
    rec = [float(r["Recursive"]) if r["Recursive"] != "-" else math.nan for r in rows]
    return n, it, dp, rec


def plot_iter_dp(n, it, dp, title: str, outfile: Path):
    plt.figure(figsize=(8, 5))
    plt.plot(n, it, marker="o", label="Iterative")
    plt.plot(n, dp, marker="s", label="Dynamic Programming")
    plt.title(title)
    plt.xlabel("N")
    plt.ylabel("Time (s)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()


def plot_recursive_log(n, rec, title: str, outfile: Path):
    plt.figure(figsize=(8, 5))
    plt.plot(n, rec, marker="^", color="crimson", label="Recursive")
    plt.yscale("log")
    plt.title(title + " (Log-Scale Y)")
    plt.xlabel("N")
    plt.ylabel("Time (s, log)")
    plt.grid(True, which="both", linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()


def plot_ops(n, it, dp, rec, title: str, outfile: Path):
    plt.figure(figsize=(8, 5))
    plt.plot(n, it, marker="o", label="Iterative Ops")
    plt.plot(n, dp, marker="s", label="DP Ops")
    plt.plot(n, rec, marker="^", label="Recursive Ops")
    plt.title(title)
    plt.xlabel("N")
    plt.ylabel("Operations (unitless)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()


def ratio(a: List[float], b: List[float]) -> List[float]:
    out = []
    for x, y in zip(a, b):
        if x and y and not (math.isnan(x) or math.isnan(y)) and y != 0:
            out.append(x / y)
        else:
            out.append(math.nan)
    return out


def plot_speedup(n, c_times, py_times, label: str, title: str, outfile: Path):
    sp = ratio(py_times, c_times)
    plt.figure(figsize=(8, 5))
    plt.plot(n, sp, marker="d", label=label)
    plt.axhline(1.0, color="gray", linestyle="--", linewidth=1)
    plt.title(title)
    plt.xlabel("N")
    plt.ylabel("Speedup (Python/C)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()


def main():
    # Input files
    t_c = ROOT / "timings_fib_c.csv"
    o_c = ROOT / "ops_fib_c.csv"
    t_py = ROOT / "timings_fib_py.csv"
    o_py = ROOT / "ops_fib_py.csv"

    if not (t_c.exists() and o_c.exists() and t_py.exists() and o_py.exists()):
        print("Missing CSVs. Run fib_runner.py for both C and Python first.")
        return

    c_t_rows = read_csv(t_c)
    c_o_rows = read_csv(o_c)
    py_t_rows = read_csv(t_py)
    py_o_rows = read_csv(o_py)

    n_c, it_c_t, dp_c_t, rec_c_t = parse_series(c_t_rows)
    n_c_ops, it_c_o, dp_c_o, rec_c_o = parse_series(c_o_rows)
    n_py, it_py_t, dp_py_t, rec_py_t = parse_series(py_t_rows)
    n_py_ops, it_py_o, dp_py_o, rec_py_o = parse_series(py_o_rows)

    # Iterative vs DP per language
    plot_iter_dp(n_c, it_c_t, dp_c_t, "C: Iterative vs DP Runtime", ROOT / "iter_vs_dp_c.png")
    plot_iter_dp(n_py, it_py_t, dp_py_t, "Python: Iterative vs DP Runtime", ROOT / "iter_vs_dp_py.png")

    # Recursive log-scale per language
    plot_recursive_log(n_c, rec_c_t, "C: Recursive Runtime", ROOT / "recursive_c_log.png")
    plot_recursive_log(n_py, rec_py_t, "Python: Recursive Runtime", ROOT / "recursive_py_log.png")

    # Ops comparisons
    plot_ops(n_c_ops, it_c_o, dp_c_o, rec_c_o, "C: Operations vs N", ROOT / "ops_c.png")
    plot_ops(n_py_ops, it_py_o, dp_py_o, rec_py_o, "Python: Operations vs N", ROOT / "ops_py.png")

    # Cross-language speedup (Python/C) for each algorithm
    # Align by index; assumes same Ns for both datasets
    if n_c == n_py:
        plot_speedup(n_c, it_c_t, it_py_t, "Iterative", "Speedup (Python/C) - Iterative", ROOT / "speedup_iter.png")
        plot_speedup(n_c, dp_c_t, dp_py_t, "DP", "Speedup (Python/C) - DP", ROOT / "speedup_dp.png")
        # recursive likely missing at higher N; plot where present
        plot_speedup(n_c, rec_c_t, rec_py_t, "Recursive", "Speedup (Python/C) - Recursive", ROOT / "speedup_rec.png")
    else:
        print("N grids differ between C and Python; skipping speedup charts.")

    print("Figures saved:")
    for name in [
        "iter_vs_dp_c.png", "iter_vs_dp_py.png",
        "recursive_c_log.png", "recursive_py_log.png",
        "ops_c.png", "ops_py.png",
        "speedup_iter.png", "speedup_dp.png", "speedup_rec.png",
    ]:
        p = ROOT / name
        if p.exists():
            print(" -", p.name)


if __name__ == "__main__":
    main()


