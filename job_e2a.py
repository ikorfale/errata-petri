"""Lab job: E2 seeds 1,2,3,4,5,6,7 (PREREG-E2.md). Output in out/e2_a.jsonl."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "out", "e2_a.jsonl"), "w") as f:
    sys.exit(subprocess.call([sys.executable, os.path.join(here, "e2_sweep.py"), "3000", "1,2,3,4,5,6,7",
                              "local:24,28,32;global:24,28,30,32,36,40,44,48;noage:24,28,30,32,36,40"], cwd=here, stdout=f))
