"""lab job: merit method 1 vs 4, seeds 14-16, 40k updates each (PREDICT-merit-method-1030b.md)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rc = 0
for s in (14, 15, 16):
    for m in (1, 4):
        with open(f"out/mm_{m}_{s}.json", "w") as f:
            rc |= subprocess.call([sys.executable, "merit_method.py", str(m), str(s), "40000"], stdout=f)
sys.exit(rc)
