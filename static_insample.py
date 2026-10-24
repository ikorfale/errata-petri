"""In-sample check of static_lap.predict on the 1576 census genomes (development data, NOT the test)."""
import sys, json, collections
sys.path.insert(0, ".")
from petri import World, parse
from static_lap import predict, arith
from laps_truth import truth
if __name__ == "__main__":
    R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "out/two_step_filter.json"))
    tab = collections.Counter(); ex = []; ar = collections.Counter()
    for r in R:
        g = parse(r["genome"]) if isinstance(r["genome"], str) else r["genome"]
        pr = predict(g); tr = truth(g)
        if pr[0] not in ("abstain",) and truth(g, seed=8) != tr: tab[("SEED-DEPENDENT", pr[0])] += 1
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
