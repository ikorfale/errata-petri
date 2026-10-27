"""Lab job: E3 seeds 8,9,10,11,12,13,14 (PREREG-E3.md). Output in out/e3_b.jsonl."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "out", "e3_b.jsonl"), "w") as f:
    sys.exit(subprocess.call([sys.executable, os.path.join(here, "e3_sweep.py"), "3000", "8,9,10,11,12,13,14",
                              "local:24,28,32;host:24,28,30,32,36,40;updates:24,28,30,32,36"], cwd=here, stdout=f))
