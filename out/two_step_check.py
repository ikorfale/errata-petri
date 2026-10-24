"""#484 check before any claim: for the fastest second-step hits, does the child equal the parent (indel 0, mutation off),
and does a solo population grow (20x20, seeds 1-5, 150 updates) like the parent's (246)?"""
import sys, json, statistics as st
sys.path.insert(0, ".")
from petri import World, parse, show
from genome_trace import trace
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
blk = "oypcupcncuyq"
def edit(g, e):
    k = e.split()
    i = int(k[1])
    return g[:i] + k[2] + g[i:] if k[0] == "ins" else (g[:i] + g[i + 1:] if k[0] == "del" else g[:i] + k[2] + g[i + 1:])
def child(g):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0)
    for _ in range(400):
        w.run_update()
        kids = [show(o.mem) for c, o in enumerate(w.cells) if o is not None and c != 0]
        if kids: return kids[0]
    return None
def solo(g, n=150):
    out = []
    for s in range(1, 6):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(n): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
if __name__ == "__main__":
    print("parent solo", solo(top))
    for p, e1, e2 in [(39, "sub 21 h", "sub 10 e"), (39, "sub 21 h", "sub 2 s"), (39, "sub 21 h", "ins 31 z"), (39, "ins 22 h", "del 55")]:
        g = edit(edit(top[:p] + blk + top[p + 12:], e1), e2)
        log, n = trace(parse(g), 7, 1, cap=20000)
        t = sorted(set().union(*[set(r[7]) for r in log])) if log else []
        c = child(g)
        print(p, e1, "+", e2, "len", len(g), "steps", n, t, "| child==parent:", c == g, "child len", len(c) if c else None, "| solo", solo(g), flush=True)
    # order of the one real route: is the second edit alone (before the activator) neutral?
    g0 = top[:39] + blk + top[51:]
    for name, g in (("block@39 only", g0), ("block@39 + ins 31 z", edit(g0, "ins 31 z")), ("block@39 + sub 21 h", edit(g0, "sub 21 h"))):
        log, n = trace(parse(g), 7, 1, cap=20000)
        t = sorted(set().union(*[set(r[7]) for r in log])) if log else []
        c = child(g)
        print(name, "len", len(g), "steps", n, t, "| child==parent:", c == g, "| solo", solo(g), flush=True)
