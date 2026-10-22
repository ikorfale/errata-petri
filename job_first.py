# First long run: one ancestor, 30x30 grid, 100000 updates, three seeds, under PyPy
# (same output as CPython on a fixed seed, about 10x faster on a full grid).
import os, shutil, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
py = shutil.which("pypy3") or sys.executable
for seed in (1, 2, 3):
    subprocess.run([py, os.path.join(here, "petri.py"), "--updates", "100000",
                    "--side", "30", "--seed", str(seed), "--every", "1000",
                    "--out", os.path.join(here, "out", f"first_s{seed}.json")], check=False)
