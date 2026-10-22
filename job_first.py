# First long run: one ancestor, 30x30 grid, 100000 updates, three seeds, under PyPy
# (same output as CPython on a fixed seed, about 4x less CPU time).
# Plus one pilot with parasites on (seed 101): used only to design experiment 1,
# never counted in it.
import os, shutil, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
py = shutil.which("pypy3") or sys.executable
runs = [(s, [], f"first_s{s}.json") for s in (1, 2, 3)] + [(101, ["--parasites"], "pilot_para_s101.json")]
for seed, extra, name in runs:
    subprocess.run([py, os.path.join(here, "petri.py"), "--updates", "100000",
                    "--side", "30", "--seed", str(seed), "--every", "1000",
                    "--out", os.path.join(here, "out", name)] + extra, check=False)
