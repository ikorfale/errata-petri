# First long run: one ancestor, 30x30 grid, 20000 updates, three seeds.
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
for seed in (1, 2, 3):
    subprocess.run([sys.executable, os.path.join(here, "petri.py"), "--updates", "20000",
                    "--side", "30", "--seed", str(seed), "--every", "500",
                    "--out", os.path.join(here, "out", f"first_s{seed}.json")], check=False)
