"""lab job: merit method 1 vs 4, seeds 20-21-22 (merit method 1030d, PREDICT-merit-glen-1030.md), 40k updates each (PREDICT-merit-method-1030b.md)."""
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rc = 0
for s in (20,21,22):
    for m in (1, 4):
        with open(f"out/mm_{m}_{s}.json", "w") as f:
            rc |= subprocess.call([sys.executable, "merit_method.py", str(m), str(s), "40000"], stdout=f)
sys.exit(rc)
