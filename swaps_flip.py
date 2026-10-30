"""The three majority flips of day 2 (89's share of 89+90 crossing 0.8 <-> 0.2, glitchfox's definition, 108163): top 3
genotypes of 89 and of 90 at the census before and after each flip, alone in a 5x5 world (sweep_iso.run, seeds 1-3):
steps to first division, child merit, merit per step (replication rate ~ merit / gestation), tasks."""
import json, os, sys
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ns = {"__file__": os.path.abspath("sweep_iso.py")}
exec(compile(open("sweep_iso.py").read().split("def profile")[0], "sweep_iso.py", "exec"), ns); run = ns["run"]
C = {c["update"]: c for c in json.load(open("daily/replay-day-002-swaps.json"))["censuses"]}
for u in (56500, 57500, 68000, 70000, 72000, 74500, 75500):
    c = C[u]; L = c["lens"]; a, b = L.get("89", 0), L.get("90", 0)
    print(f"== {u}: f89 = {a / (a + b):.2f}")
    for l in ("89", "90"):
        for t in c["top"].get(l, []):
            r = [x for x in (run(bytes.fromhex(t["g"]), s) for s in (1, 2, 3)) if x]
            if not r: print(f"   len {l} {t['n']:>3} copies sterile alone"); continue
            st = median(x[0] for x in r); me = median(x[1] for x in r)
            print(f"   len {l} {t['n']:>3} copies  steps {st:>5}  merit {me:>9.0f}  m/s {me / st:>7.0f}  {'+'.join(r[0][2])}")
