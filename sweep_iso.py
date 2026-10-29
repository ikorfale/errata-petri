"""Day-2 sweeps, step 2 (promise 106752/107230): did each coal-flagged sweep come from copy speed or from a task?
For each sweep, the 8 most common genotypes just before it and at its first flagged census go alone into a 5x5 world
(no mutation, seeds 1-3, same settings as the daily world): steps to first division, the child's merit, tasks done in
that first gestation, merit per step (CPU share ~ merit, so replication rate ~ merit / gestation).
Speed sweep: the sweep's genotypes divide in fewer steps. Task sweep: same steps, higher merit from a new task.
Usage: python3 sweep_iso.py [PRE:AT ...] > out/sweep_iso.txt (needs out/sweeps/w*.pkl from sweep_snaps.py)"""
import os, pickle, sys
from collections import Counter
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import OPS, World
SWEEPS = [(56500, 57500), (61500, 63000), (65500, 66500), (74500, 75500)]   # (before, first flagged census)
K = 8
if len(sys.argv) > 1: SWEEPS = [tuple(map(int, a.split(':'))) for a in sys.argv[1:]]   # e.g. 61500:63000

def run(g, seed, steps=20000):
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]
    for i in range(steps):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b:
            kid = next(x for x in v.cells if x is not None and x is not o)
            return i + 1, kid.merit, tuple(sorted(v.task_births))   # tasks of the gestation that just ended
    return None

def profile(u):
    w = pickle.load(open(f"out/sweeps/w{u}.pkl", "rb"))
    live = [o for o in w.cells if o is not None]
    cnt = Counter(bytes(o.mem[:o.glen]) for o in live)
    rows = []
    for g, n in cnt.most_common(K):
        r = [x for x in (run(g, s) for s in (1, 2, 3)) if x]
        if not r: rows.append((n, len(g), None, None, None, ())); continue
        st = median(x[0] for x in r); me = median(x[1] for x in r)
        rows.append((n, len(g), st, me, me / st, r[0][2]))
    return len(live), rows

for pre, at in SWEEPS:
    print(f"== sweep flagged at {at:,} (before: {pre:,})", flush=True)
    for u in (pre, at):
        pop, rows = profile(u)
        ok = [r for r in rows if r[2]]
        print(f"  {u:,}: pop {pop}; top {K} genotypes (copies, len, steps, merit, merit/step, tasks):")
        for r in rows:
            print(f"    {r[0]:3d} len {r[1]:3d} " + (f"steps {r[2]:.0f} merit {r[3]:.0f} m/s {r[4]:.0f} {'+'.join(r[5])}" if r[2] else "no division"))
        if ok:
            print(f"  median of top {K}: steps {median(r[2] for r in ok):.0f}, merit/step {median(r[4] for r in ok):.0f}, "
                  f"OR in first gestation {sum('OR' in r[5] for r in ok)}/{len(ok)}", flush=True)
