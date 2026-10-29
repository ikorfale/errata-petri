"""PREDICT-dualbirths-1029.md, step 2: trace every distinct mutated child in out/dual_births_sSEED.json.gz (genome_trace,
seed 7, cap 2000, as swapback.py) and count AND+ANDN children by route. Usage: python3 dual_births_trace.py SEED and|other"""
import json, sys, gzip, time
sys.path.insert(0, "."); sys.path.insert(0, "out")
from genome_trace import trace
from petri import parse
def run(g, cap=2000):
    try: log, n = trace(parse(g), 7, 1, cap=cap)
    except Exception: return (), cap
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
s, which = sys.argv[1], sys.argv[2]
D = json.load(gzip.open(f"out/dual_births_s{s}.json.gz", "rt")); K = D["kids_and" if which == "and" else "kids_other"]
t0 = time.time(); hits = []; births = sum(n for _, n in K)
for i, (g, n) in enumerate(K):
    tk, st = run(g)
    if "AND" in tk and "ANDN" in tk: hits.append({"genome": g, "births": n, "steps": st, "tasks": tk, "len_mod3": len(g) % 3})
    if i % 50000 == 0: print(i, len(K), len(hits), round(time.time() - t0), flush=True, file=sys.stderr)
print(json.dumps({"seed": s, "route": which, "distinct_children": len(K), "child_births": births, "dual_genotypes": len(hits),
                  "dual_births": sum(h["births"] for h in hits), "dividing_lt2000": sum(h["steps"] < 2000 for h in hits),
                  "hits": hits, "sec": round(time.time() - t0)}))
