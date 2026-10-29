"""#535 step 0 (free readout before designing new runs): in the final genotype censuses of the 10 evo_and runs (s2 dominant,
default rates, 40,000 updates), which genotypes compute AND, AND+ANDN, at which length mod 3, and do they divide fast?
Same tracer as out/two_step.py (genome_trace, seed 7, cap 2000). Written 29.10 12:57 UTC (date -u).
Usage: python3 and_census_phase.py > out/and_census_phase.txt"""
import json, sys, glob, time
from collections import Counter
sys.path.insert(0, "."); sys.path.insert(0, "out")
from genome_trace import trace
from petri import parse
def run(g, cap=2000):
    try: log, n = trace(parse(g), 7, 1, cap=cap)
    except Exception: return (), cap
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
t0 = time.time(); tot = Counter(); rows = []
for f in sorted(glob.glob("out/evo_and_census_s*.json")):
    seed = f.split("_s")[-1].split(".")[0]; C = json.load(open(f))
    for g, n in C:
        tk, steps = run(g); a = "AND" in tk; b = a and "ANDN" in tk
        tot[("all", len(g) % 3)] += n
        if a: tot[("AND", len(g) % 3)] += n
        if b: tot[("AND+ANDN", len(g) % 3)] += n; rows.append((seed, len(g), steps, n, tk, g))
print(f"genotype-weighted organisms by class and length mod 3 (10 final censuses, {time.time() - t0:.0f}s):")
for k in ("all", "AND", "AND+ANDN"):
    print(f"  {k}: " + ", ".join(f"mod{m} {tot[(k, m)]}" for m in (0, 1, 2)))
print("AND+ANDN genotypes (seed, len, steps to divide or cap 2000, count, tasks):")
for r in sorted(rows, key=lambda r: r[2]): print(" ", r[:5])
# which task sets do the AND carriers have (organism-weighted)?
ts = Counter()
for f in sorted(glob.glob("out/evo_and_census_s*.json")):
    for g, n in json.load(open(f)):
        tk, steps = run(g)
        if "AND" in tk: ts[(tk, "fast" if steps < 300 else ("slow" if steps < 2000 else "cap"))] += n
print("AND carriers by task set and speed (<300 fast, <2000 slow, else cap):")
for k, n in ts.most_common(): print(f"  {n:3d} {k}")
s2 = max(json.load(open("out/s2_dump.json"))["genotypes"], key=lambda g: g["n"])["genome"]
print("s2 dominant:", len(s2), run(s2))
