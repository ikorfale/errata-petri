"""Readout of out/life_day2.json per PREDICT-life-1029.md (written before the run)."""
import json, random
from math import comb
d = json.load(open("out/life_day2.json")); S = 500
nc = lambda b: (b // S + 1) * S
org = {int(k): v for k, v in d["origins"].items()}
founder = max(org, key=lambda k: org[k]["life_any"])
rest = {k: v for k, v in org.items() if k != founder}
print("origins", len(org), "founder", founder, org[founder])
g1 = sum(v["life_any"] >= 131 for v in rest.values()); g1c = sum(v["life_capable_run"] >= 131 for v in rest.values())
print("G1 raw >=131 updates: any descendant", g1, "of", len(rest), "| capable run", g1c)
auto = sum(v["next_census"] - v["born"] >= 131 for v in rest.values())
print("   born >=131 before their first census (automatic pass if seen there):", auto)
def reach(b, life, k):  # alive at census k after birth (k=1 first)
    return b + life >= nc(b) + (k - 1) * S
for lab, key in (("any", "life_any"), ("capable", "life_capable_run")):
    c1 = [v for v in rest.values() if reach(v["born"], v[key], 1)]
    c2 = [v for v in c1 if reach(v["born"], v[key], 2)]
    print(f"origins {lab}: reach census1 {len(c1)}, of them census2 {len(c2)}")
base = d["baseline_mutated_births"]
b1 = [(b, l) for b, l in base if reach(b, l, 1)]; b2 = [x for x in b1 if reach(*x, 2)]
p = len(b2) / len(b1)
print(f"baseline mutated births: {len(base)} sampled of {d['n_mutated_births_after']}, reach census1 {len(b1)} ({len(b1)/len(base):.3%}), of them census2 {len(b2)} ({p:.1%})")
b131 = sum(l >= 131 for b, l in b1) / len(b1)
print(f"baseline, census-reaching, life >=131: {b131:.1%}")
c1 = [v for v in rest.values() if reach(v["born"], v["life_any"], 1)]
k = sum(reach(v["born"], v["life_any"], 2) for v in c1); n = len(c1)
lo = sum(comb(n, i) * p**i * (1-p)**(n-i) for i in range(k + 1))
print(f"G4 binomial vs baseline rate: {k}/{n} observed, expected {n*p:.1f}, P(X<={k}) = {lo:.3g}")
