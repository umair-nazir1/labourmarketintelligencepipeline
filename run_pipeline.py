"""Run the whole pipeline in order: fetch -> clean -> load.

Stops at the first failing step, so later steps never run on bad or stale data.
Run it from the project root:  python run_pipeline.py
"""

import subprocess
import sys
import time

# Each step is a (name, script path) pair, in the order they must run.
STEPS = [
    ("fetch", "src/fetch_jobs.py"),
    ("clean", "src/clean_jobs.py"),
    ("load", "src/load_to_db.py"),
]

pipeline_start = time.time()

for name, script in STEPS:
    print(f"--- Running step: {name} ---")
    step_start = time.time()

    # Run the script with the same Python that is running this file (the venv one).
    result = subprocess.run([sys.executable, script])

    elapsed = time.time() - step_start

    # An exit code of 0 means success; anything else means the step failed.
    if result.returncode != 0:
        print(f"Step '{name}' FAILED with exit code {result.returncode}. Stopping the pipeline.")
        sys.exit(result.returncode)

    print(f"Step '{name}' finished in {elapsed:.1f}s")

print(f"Pipeline finished successfully in {time.time() - pipeline_start:.1f}s")