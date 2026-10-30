"""lab job: top genotypes per length at every census of day 2 (PREDICT-swaps-1030.md). Lab jobs must be .py."""
import json, os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open("daily/day-002.json"))["digest"][:16]
with open("daily/replay-day-002-swaps.json", "w") as f:
    sys.exit(subprocess.call([sys.executable, "replay_swaps.py", "daily/base/day-001", "40000", d], stdout=f))
