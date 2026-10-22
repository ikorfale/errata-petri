# Rerun of the first experiment with tagged inputs (v0.2): one ancestor, 30x30 grid,
# 100000 updates, three seeds, under PyPy. Compare with out/first_s*.json (v0.1, raw inputs),
# where XOR and EQU credits were input coincidences (out/xor_trace_summary.txt).
import os, shutil, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
py = shutil.which("pypy3") or sys.executable
for seed in (1, 2, 3):
    subprocess.run([py, os.path.join(here, "petri.py"), "--updates", "100000",
                    "--side", "30", "--seed", str(seed), "--every", "1000",
                    "--out", os.path.join(here, "out", f"tagged_s{seed}.json")], check=False)
