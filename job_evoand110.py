# #481 backup: seed 110 alone, only if the main job (petri-evoand-481) ended before seed 110 reached 40,000 updates.
# evo_and.py appends a new update-0 header; read_evoand.py counts only rows after a seed's last header.
import json, os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
last = 0
for line in open("out/evo_and.jsonl"):
    r = json.loads(line)
    if r["seed"] == 110: last = 0 if r["update"] == 0 else r["update"]
if last >= 40000:
    print("seed 110 already complete in the main job; nothing to do"); sys.exit(0)
print(f"seed 110 stopped at {last}; rerunning from scratch")
sys.exit(subprocess.call([sys.executable, "evo_and.py", "40000", "110"]))
