"""zenith 100725: can AND+ANDN arrive without changing length? (A) overwrite top[p:p+L] with the block (L=12 with the
trailing no-op, L=11 without) for every p; trace one gestation (cap 20000), tasks + steps. (B) single substitution
neutrality map: is the sub silent (same tasks, same steps)? Mutation off, tracer seed 7 like and_mutants.py."""
import sys, json, string, collections
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase
def run(g):
    try:
        log, n = trace(parse(g), 7, 1, cap=20000)
    except Exception:
        return ("ERR",), -1
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
def cls(n): return "never" if n >= 20000 or n < 0 else ("fast" if n < 300 else "slow")
bt, bn = run(top); print("dominant", len(top), bt, bn)
res = {"dominant": [bt, bn], "overwrite": [], "subs": []}
for blk in ("oypcupcncuyq", "oypcupcncuy"):
    c = collections.Counter(); hits = []
    for p in range(len(top) - len(blk) + 1):
        g = top[:p] + blk + top[p + len(blk):]; assert len(g) == len(top)
        t, n = run(g); c[cls(n)] += 1
        res["overwrite"].append({"blk": blk, "p": p, "tasks": t, "steps": n})
        if "AND" in t and "ANDN" in t: hits.append((p, n, t))
    print(f"block {blk} ({len(blk)}): {sum(c.values())} positions, classes {dict(c)}; AND+ANDN at {len(hits)}")
    for h in hits: print("   p", h[0], "steps", h[1], cls(h[1]), h[2])
silent = []
for i in range(len(top)):
    s = 0
    for ch in AL:
        if ch == top[i]: continue
        t, n = run(top[:i] + ch + top[i + 1:])
        s += (t == bt and n == bn)
        res["subs"].append([i, ch, t, n])
    silent.append(s)
print("silent subs per index (of 25):", silent)
print("indices with >=1 silent sub:", sum(x > 0 for x in silent), "with >=20:", sum(x >= 20 for x in silent))
json.dump(res, open("out/inplace_block.json", "w"))
