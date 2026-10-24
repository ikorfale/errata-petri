"""In-sample check of static_lap.predict on the 1576 census genomes (development data, NOT the test)."""
import sys, json, collections
sys.path.insert(0, ".")
from petri import World, parse
from static_lap import predict, arith
def truth(g, cap):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(list(g), "t", cell=0); o = w.cells[0]
    for n in range(cap):
        b = w.births; L = len(o.mem); nc = o.ncopy
        w.step(o, 0)
        if w.births > b:
            kid = [c for c in w.cells if c is not None and c is not o]
            ch = bytes(kid[0].mem[:kid[0].glen]) if kid else None
            if ch == bytes(g): return ("exact", nc // len(g)) if nc % len(g) == 0 else ("exact?", nc)
            if ch is not None and len(ch) == len(g): return ("rotated", nc)
            return ("other-birth", len(ch) if ch else None)
        o = w.cells[0]
    return ("never", "cap")
if __name__ == "__main__":
    R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "out/two_step_filter.json"))
    tab = collections.Counter(); ex = []; ar = collections.Counter()
    for r in R:
        g = parse(r["genome"]) if isinstance(r["genome"], str) else r["genome"]
        pr = predict(g); tr = truth(g, 40 * len(g))
        pk = pr[0] if pr[0] in ("abstain", "filtered", "never") else pr
        tk = tr if tr[0] in ("exact", "rotated") else (tr[0],)
        if pr[0] == "other-birth": pk = ("other-birth",)
        ok = (pk == tk) or (pr[0] == "never" and tr[0] == "never")
        tab[(pr[0], tr[0], "ok" if ok else "MISS")] += 1
        a = arith(g)
        if tr[0] == "exact": ar[("arith", "none" if a is None else a[0], "ok" if a and a[0] == "exact" and a[1] == tr[1] else "MISS" if a else "-")] += 1
        elif tr[0] == "never" and a: ar[("arith on never", a[0])] += 1
        if not ok and pr[0] not in ("abstain", "filtered") and len(ex) < 12: ex.append((len(g), pr, tr))
    for k, v in sorted(tab.items()): print(k, v)
    for k, v in sorted(ar.items()): print(k, v)
    print("misses:", *ex, sep="\n  ")
