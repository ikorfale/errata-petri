"""Plan #560 (zenith 107333): is each OR origin worse than its parent, alone? Same assay as sweep_iso.py: the genome alone
in a 5x5 world, no mutation, seeds 1-3; steps to first division and the child's merit; replication rate ~ merit / steps.
Ratio = (origin merit/step) / (parent merit/step). Baseline: 400 random mutated births of the same day that were alive at
their next census (same conditioning as the origins), same ratio against their parents. Guesses: PREDICT-merit-1029.md.
Usage: python3 origin_merit.py out/origin_genomes_day2.json > out/origin_merit_day2.txt"""
import json, os, sys
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import World

def run(g, seed, steps=20000):
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]
    for i in range(steps):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b:
            kid = next(x for x in v.cells if x is not None and x is not o)
            return i + 1, kid.merit, tuple(sorted(v.task_births))
    return None
memo = {}
def rate(g):
    g = bytes(g)
    if g not in memo:
        r = [x for x in (run(g, s) for s in (1, 2, 3)) if x]
        memo[g] = (median(x[1] for x in r) / median(x[0] for x in r), r[0][2]) if r else (0.0, ())
    return memo[g]
def ratios(rows):
    out = []
    for x in rows:
        if x["parent_genome"] is None: continue
        c, ct = rate(x["genome"]); p, pt = rate(x["parent_genome"])
        out.append((c / p if p else float("nan"), len(ct) - len(pt), x))
    return out
d = json.load(open(sys.argv[1]))
for lab, rows in (("origins (founder 62,369 excluded)", [v for k, v in d["origins"].items() if v["born"] != 62369]),
                  ("baseline census-reaching mutated births", d["baseline_census_reaching"])):
    r = [x for x in ratios(rows) if x[0] == x[0]]; q = sorted(x[0] for x in r); n = len(q)
    print(f"== {lab}: n {n}")
    if not n: continue
    print(f"  ratio median {median(q):.3f}, q25 {q[n//4]:.3f}, q75 {q[3*n//4]:.3f}")
    print(f"  worse (<0.95) {sum(v < 0.95 for v in q)}, ~equal {sum(0.95 <= v <= 1.05 for v in q)}, better (>1.05) {sum(v > 1.05 for v in q)}, sterile alone {sum(v == 0 for v in q)}")
    print(f"  task count change vs parent: " + ", ".join(f"{k:+d}:{sum(x[1] == k for x in r)}" for k in sorted({x[1] for x in r})))
fo = [v for v in d["origins"].values() if v["born"] == 62369]
if fo: print("founder 62,369 ratio (check, 1.004 expected from 107295):", round(rate(fo[0]["genome"])[0] / rate(fo[0]["parent_genome"])[0], 3))
