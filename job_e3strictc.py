"""Lab job #541: e3_brk.py strict seeds 1-7 again, now with the refusal counters (zenith 105858); must equal e3strict_a.jsonl except "ref". Output in out/e3strict_c.jsonl."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "out", "e3strict_c.jsonl"), "w") as f:
    sys.exit(subprocess.call([sys.executable, os.path.join(here, "e3_brk.py"), "3000", "1,2,3,4,5,6,7",
                              "local:24,28,32;host:24,28,30,32,36,40;updates:24,28,30,32,36", "--strict"], cwd=here, stdout=f))
