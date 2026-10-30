"""Day 3 (replay-day-003-swaps.json, digest-checked): the two sweep windows of post-003 (82,500-83,500 and 103,000-106,000)
and the brief plurality of length 87 at 101,500-102,000. Top 3 genotypes of the competing length classes at each census,
alone in a 5x5 world (sweep_iso.run, seeds 1-3): steps to first division, child merit, merit per step, tasks."""
import json, os, sys
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ns = {"__file__": os.path.abspath("sweep_iso.py")}
exec(compile(open("sweep_iso.py").read().split("def profile")[0], "sweep_iso.py", "exec"), ns); run = ns["run"]
C = {c["update"]: c for c in json.load(open("daily/replay-day-003-swaps.json"))["censuses"]}
for u, ls in ((82000, ("89", "90", "91")), (83000, ("89", "91")), (100500, ("87", "91")), (101500, ("87", "91")),
              (102000, ("87", "91")), (103000, ("87", "91")), (106000, ("91",))):
    c = C[u]; print(f"== {u}: lens {sorted(((int(k), v) for k, v in c['lens'].items()), key=lambda x: -x[1])[:4]}")
    for l in ls:
        for t in c["top"].get(l, []):
            r = [x for x in (run(bytes.fromhex(t["g"]), s) for s in (1, 2, 3)) if x]
            if not r: print(f"   len {l} {t['n']:>3} copies sterile alone  {t['g'][:16]}"); continue
            st = median(x[0] for x in r); me = median(x[1] for x in r)
            print(f"   len {l} {t['n']:>3} copies  steps {st:>5}  merit {me:>9.0f}  m/s {me / st:>7.0f}  {t['g'][:16]}  {'+'.join(r[0][2])}")
