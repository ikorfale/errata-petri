"""Mechanical verdict for PREREG-seed.md from out/seed_entry/*_s{1..12}.json. Exit 1 if any run is missing."""
import json, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "seed_entry")
SEEDS, ARMS = range(1, 13), ["ANC-len", "DOM-len", "ANC-mean", "DOM-mean"]
R, miss = {}, []
for a in ARMS:
    for s in SEEDS:
        p = os.path.join(D, f"{a}_s{s}.json")
        if os.path.exists(p): R[a, s] = json.load(open(p))
        else: miss.append(f"{a}_s{s}")
if miss: print("missing:", " ".join(miss)); sys.exit(1)
for a in ARMS:
    rs = [R[a, s] for s in SEEDS]
    print(a, "| end:", {e: sum(r["end"] == e for r in rs) for e in ("extinct", "fixed", "horizon")},
          "| end update:", [r["end_du"] for r in rs], "| seed births:", [r["seed_births"] for r in rs],
          "| peak:", [r["max_seed"] for r in rs])
def ext(a): return [R[a, s] for s in SEEDS if R[a, s]["end"] == "extinct"]
def zero(a): return sum(R[a, s]["seed_births"] == 0 for s in SEEDS)
p1 = len(ext("ANC-len")) == 12 and zero("ANC-len") >= 11
p2 = len(ext("DOM-len")) == 12 and zero("DOM-len") >= 11
p3 = len(ext("ANC-mean")) == 12 and all(r["end_du"] < 5000 for r in ext("ANC-mean"))
def life(r): return float("inf") if r["end"] != "extinct" else r["end_du"]
longer = sum(life(R["DOM-mean", s]) > life(R["DOM-len", s]) for s in SEEDS)
fixed = sum(R["DOM-mean", s]["end"] == "fixed" for s in SEEDS)
p4 = longer >= 11 and fixed <= 1
print(f"P1 {'held' if p1 else 'FAILED'}; P2 {'held' if p2 else 'FAILED'}; P3 {'held' if p3 else 'FAILED'}; "
      f"P4 {'held' if p4 else 'FAILED'} (DOM-mean longer in {longer}/12, fixed {fixed}/12)")
