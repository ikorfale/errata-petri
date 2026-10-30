"""merit method 1 vs 4, seeds 23-32, 40k updates each (PREDICT-merit-ex-1030.md); serial, skips arms already done."""
import os, subprocess, sys, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rc = 0
for s in range(23, 33):
    for m in (1, 4):
        out = f"out/mm_{m}_{s}.json"
        try:
            json.load(open(out)); continue
        except Exception: pass
        with open(out + ".tmp", "w") as f:
            r = subprocess.call([sys.executable, "merit_method.py", str(m), str(s), "40000"], stdout=f)
        if r == 0: os.replace(out + ".tmp", out)
        rc |= r
sys.exit(rc)
