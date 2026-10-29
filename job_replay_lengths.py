"""lab job: genome-length mix at every census of day 2 (PREDICT-shrink-1029.md). Lab jobs must be .py."""
import json, os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open("daily/day-002.json"))["digest"][:16]
with open("daily/replay-day-002-lengths.json", "w") as f:
    sys.exit(subprocess.call([sys.executable, "replay_lengths.py", "daily/base/day-001", "40000", d], stdout=f))
