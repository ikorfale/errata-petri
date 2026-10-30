"""lab job: merit method 1 vs 4, seeds 11-13, 40k updates each (PREDICT-merit-method-1030.md)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rc = 0
for s in (11, 12, 13):
    for m in (1, 4):
        with open(f"out/mm_{m}_{s}.json", "w") as f:
            rc |= subprocess.call([sys.executable, "merit_method.py", str(m), str(s), "40000"], stdout=f)
sys.exit(rc)
