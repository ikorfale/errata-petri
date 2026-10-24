"""zenith 100725 follow-up: are the fully silent indices silent because they are never executed? Then build the block
in the silent stretch (neutral by construction) and ask whether ONE further point mutation (sub/ins/del) routes
execution into it: AND+ANDN and still fast. Mutation off, tracer seed 7."""
import sys, json, string, collections
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, OPS, parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase
def executed(g, cap=20000):
    w = World(side=5, seed=7, copy_mut=0.0); w.inject(parse(g), "t", cell=0); o = w.cells[0]; seen = set(); n = 0
    b = w.births
    while w.births == b and n < cap:
        seen.add(o.heads[0] % len(o.mem)); w.step(o, 0); o = w.cells[0]; n += 1
    return seen
def run(g):
    try: log, n = trace(parse(g), 7, 1, cap=20000)
    except Exception: return ("ERR",), -1
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
ex = executed(top)
print("executed indices", len(ex), "of", len(top), ":", sorted(ex))
dead = [i for i in range(len(top)) if i not in ex]
print("never executed:", dead)
blk = "oypcupcncuyq"
starts = [p for p in range(len(top) - 11) if all(q in dead for q in range(p, p + 12))]
print("12-runs fully inside dead code start at", starts)
for p in starts[:: max(1, len(starts) // 4)] if starts else []:
    g = top[:p] + blk + top[p + 12:]
    t0, n0 = run(g); print(f"\nblock at {p}: tasks {t0} steps {n0}")
    hits = []
    for i in range(len(g) + 1):
        for c in AL:
            cand = [("ins", g[:i] + c + g[i:])]
            if i < len(g):
                cand.append(("del", g[:i] + g[i + 1:])) if c == "a" else None
                if c != g[i]: cand.append(("sub", g[:i] + c + g[i + 1:]))
            for k, x in cand:
                t, n = run(x)
                if "AND" in t and "ANDN" in t: hits.append((k, i, c, n, len(x)))
    print(f"  one-step activators giving AND+ANDN: {len(hits)}; fast (<300): {sum(h[3] < 300 for h in hits)}")
    for h in sorted(hits, key=lambda h: h[3])[:12]: print("   ", h)
