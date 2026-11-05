"""Lab job for PREREG-seed.md: all four arms, seeds 1-12, horizon 120,000 updates, then the mechanical verdict."""
import os, subprocess, sys
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(P)
subprocess.run([sys.executable, "seed_entry.py", "out/seed_entry/world-day009.pkl", "120000",
                ",".join(str(s) for s in range(1, 13)), "ANC-len,DOM-len,ANC-mean,DOM-mean", "4"], check=True)
with open("out/seed_entry/verdict.txt", "w") as f:
    subprocess.run([sys.executable, "seed_entry_verdict.py"], stdout=f, stderr=subprocess.STDOUT)
print(open("out/seed_entry/verdict.txt").read())
