"""lab job: day-3 replay, top genotypes per length at every census, to see what the coalescence sweeps at 82.5k-83.5k
and 103k-106k carried (no dominant-genotype event fired that day). Lab jobs must be .py."""
import json, os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open("daily/day-003.json"))["digest"][:16]
with open("daily/replay-day-003-swaps.json", "w") as f:
    sys.exit(subprocess.call([sys.executable, "replay_swaps.py", "daily/base/day-002", "40000", d], stdout=f))
