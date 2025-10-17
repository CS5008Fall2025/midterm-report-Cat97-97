"""
Batch runner to collect timings and operation counts for Fibonacci implementations
in both C and Python. Outputs CSV files similar to the provided sample midterm.
"""

import subprocess
import sys
import csv
import argparse


EXEC_C = "./fib.exe"
EXEC_PY = "python3 fib.py"
COMMON_ARG_FORMAT = "{n} {type}"
TIMEOUT = 60
OUT_DEFAULT = "fib_run.csv"
OUT_FILE_TIME = "timings_"
OUT_FILE_OPS = "ops_"
CSV_HEADER = "N,Iterative,Dynamic Programming,Recursive"


class RecursionTimeoutError(Exception):
    pass


def run_single(executable: str, n: int, typ: int):
    command = f"{executable} {n} {typ}"
    try:
        results = subprocess.run(
            command.split(), timeout=TIMEOUT, capture_output=True, text=True
        )
    except subprocess.TimeoutExpired:
        raise RecursionTimeoutError(f"Timeout of {TIMEOUT} seconds reached for {command}")

    if results.returncode != 0:
        raise Exception(f"Error running {command}: {results.stderr}")

    results_line = results.stdout.strip().split(",")
    timings = []
    operations = []
    for i in range(0, len(results_line), 2):
        timings.append(results_line[i])
        operations.append(results_line[i + 1])

    return {"timings": timings, "operations": operations}


def save_to_csv(values: list, out_file: str, step: int):
    with open(out_file, "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(CSV_HEADER.split(","))
        for i, row in enumerate(values):
            row = [i * step + 1] + row
            csv_writer.writerow(row)


def main(n: int, step: int, out_file: str, executable: str):
    run_type = 3  # all three
    results = {"timings": [], "operations": []}
    for i in range(1, n + 1, step):
        try:
            result = run_single(executable, i, run_type)
            results["timings"].append(result["timings"])
            results["operations"].append(result["operations"])
        except RecursionTimeoutError:
            run_type = 4  # iterative and dp only
            result = run_single(executable, i, run_type)
            results["timings"].append(result["timings"])
            results["operations"].append(result["operations"])
        except Exception as e:
            print(e, file=sys.stderr)
            break
    save_to_csv(results["operations"], OUT_FILE_OPS + out_file, step)
    save_to_csv(results["timings"], OUT_FILE_TIME + out_file, step)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Fibonacci program and collect data")
    parser.add_argument("n", type=int, help="max N to generate")
    parser.add_argument("--step", type=int, default=1, help="step size")
    parser.add_argument("--out", type=str, default=OUT_DEFAULT, help="base output file name")
    parser.add_argument("--timeout", type=int, default=TIMEOUT, help="timeout seconds")
    parser.add_argument("--exec", type=str, default=EXEC_C, help="executable to run")
    args = parser.parse_args()
    TIMEOUT = args.timeout
    main(args.n, args.step, args.out, args.exec)


