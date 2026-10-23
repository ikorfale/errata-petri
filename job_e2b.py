"""Lab job: E2 seeds 8,9,10,11,12,13,14 (PREREG-E2.md). Output in out/e2_b.jsonl."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "out", "e2_b.jsonl"), "w") as f:
    sys.exit(subprocess.call([sys.executable, os.path.join(here, "e2_sweep.py"), "3000", "8,9,10,11,12,13,14",
                              "local:24,28,32;global:24,28,30,32,36,40,44,48;noage:24,28,30,32,36,40"], cwd=here, stdout=f))
