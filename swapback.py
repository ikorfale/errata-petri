"""#535 (PREDICT-swapback-1029.md): from every fast-enough AND-without-ANDN genotype in the evo_and final censuses, every
one-step mutant that computes AND+ANDN. Usage: python3 swapback.py > out/swapback.txt"""
import json, sys, glob, string, time
from statistics import median
sys.path.insert(0, "."); sys.path.insert(0, "out")
from genome_trace import trace
from petri import parse
AL = string.ascii_lowercase
def run(g, cap=2000):
    try: log, n = trace(parse(g), 7, 1, cap=cap)
    except Exception: return (), cap
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
def neigh(g):
    for i in range(len(g) + 1):
        for c in AL: yield f"ins {i} {c}", g[:i] + c + g[i:]
    for i in range(len(g)):
        yield f"del {i}", g[:i] + g[i + 1:]
        for c in AL:
            if c != g[i]: yield f"sub {i} {c}", g[:i] + c + g[i + 1:]
t0 = time.time(); par = {}
for f in sorted(glob.glob("out/evo_and_census_s*.json")):
    for g, n in json.load(open(f)):
        if g in par: par[g][1] += n; continue
        tk, s = run(g)
        if "AND" in tk and "ANDN" not in tk and s < 2000: par[g] = [s, n, tk]
print(f"parents: {len(par)} distinct AND-without-ANDN genotypes dividing <2000 steps")
allhits = []
for g, (s, n, tk) in sorted(par.items(), key=lambda x: x[1][0]):
    hits = []
    for lab, m in neigh(g):
        t2, s2 = run(m)
        if "AND" in t2 and "ANDN" in t2: hits.append((s2, len(m) % 3, lab, t2))
    hits.sort(); allhits += hits
    div = [h for h in hits if h[0] < 2000]
    print(f"parent len {len(g)} (mod3 {len(g) % 3}) steps {s} n {n} {tk}: AND+ANDN mutants {len(hits)}, dividing {len(div)}, "
          f"fast {sum(h[0] < 300 for h in hits)}; fastest {hits[:3]}", flush=True)
div = [h for h in allhits if h[0] < 2000]
print(f"total AND+ANDN one-step mutants {len(allhits)}, dividing <2000 {len(div)}, fast <300 {sum(h[0] < 300 for h in allhits)}")
for m in (0, 1, 2):
    d = [h[0] for h in div if h[1] == m]
    print(f"  dividing at mod3 {m}: {len(d)}" + (f", median steps {median(d)}" if d else ""))
print(f"{time.time() - t0:.0f}s")
