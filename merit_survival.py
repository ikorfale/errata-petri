"""Plan #560 follow-up (guesses in PREDICT-merit2-1029.md, 57e71d9): among census-reaching mutated births (baseline 1000,
lineage life saved by replay_origins.py --baseline-n), does merit alone (same assay as origin_merit.py) predict whether the
line also reaches the census after next (born + life >= next_census + SAMPLE)? Also checks the first 400 reproduce
out/origin_merit_day2.txt. Usage: python3 merit_survival.py out/origin_genomes_day2_r2.json"""
import json, os, sys, random
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily
from petri import World
def run(g, seed, steps=20000):
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]
    for i in range(steps):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b:
            kid = next(x for x in v.cells if x is not None and x is not o)
            return i + 1, kid.merit
    return None
memo = {}
def rate(g):
    g = bytes(g)
    if g not in memo:
        r = [x for x in (run(g, s) for s in (1, 2, 3)) if x]
        memo[g] = median(x[1] for x in r) / median(x[0] for x in r) if r else 0.0
    return memo[g]
d = json.load(open(sys.argv[1])); B = d['baseline_census_reaching']
rows = []
for x in B:
    if x['parent_genome'] is None: continue
    p = rate(x['parent_genome']); c = rate(x['genome'])
    if not p: continue
    rows.append((c / p, x['born'] + x['life'] >= x['next_census'] + daily.SAMPLE))
q = sorted(r[0] for r in rows[:400]); print(f"first 400 check: n {len(q)}, median {median(q):.3f}, equal-or-better {sum(v >= .95 for v in q)}")
def share(s): return (sum(r[1] for r in s), len(s))
cls = {'equal-or-better (>=0.95)': [r for r in rows if r[0] >= .95], 'worse (<0.95, >0)': [r for r in rows if 0 < r[0] < .95],
       'sterile alone (0)': [r for r in rows if r[0] == 0]}
for k, s in cls.items():
    a, n = share(s); print(f"{k}: reach second census {a}/{n} = {a / n:.3f}" if n else f"{k}: n 0")
ne, wo = [r[1] for r in cls['equal-or-better (>=0.95)']], [r[1] for r in rows if r[0] < .95]
diff = sum(ne) / len(ne) - sum(wo) / len(wo); rng = random.Random(1029); bs = []
for _ in range(5000):
    a = [rng.choice(ne) for _ in ne]; b = [rng.choice(wo) for _ in wo]; bs.append(sum(a) / len(a) - sum(b) / len(b))
bs.sort(); print(f"neutral minus worse: {diff:+.3f}, 95% bootstrap {bs[125]:+.3f} .. {bs[4874]:+.3f}")
pn, pw = sum(ne) / len(ne), sum(wo) / len(wo)
print(f"N3: origins' mix 7 neutral + 96 worse -> expected at second census {7 * pn + 96 * pw:.1f} (unweighted baseline rate x 103 = {103 * sum(r[1] for r in rows) / len(rows):.1f})")
