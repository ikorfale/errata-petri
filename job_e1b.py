"""Lab job: E1 seeds 8,9,10,11,12,13,14 (PREREG-E1.md, commit 9625b47). Output in out/e1_b.jsonl."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "out", "e1_b.jsonl"), "w") as f:
    sys.exit(subprocess.call([sys.executable, os.path.join(here, "e1_sweep.py"), "3000", "8,9,10,11,12,13,14",
                              "16,20,24,28,32,36,40,44,48"], cwd=here, stdout=f))
