"""In-sample check of static_lap.predict and arith on the 1576 census genomes (development data, NOT the test).
Scored only through scoring.py (the frozen rule); truth under seeds 7 and 8."""
import sys, json, collections
sys.path.insert(0, ".")
from petri import parse
from static_lap import predict, arith
from laps_truth import truth
from scoring import score_static, score_arith
if __name__ == "__main__":
    R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "out/two_step_filter.json"))
    st = collections.Counter(); ar = collections.Counter(); ex = []
    for r in R:
        g = parse(r["genome"]) if isinstance(r["genome"], str) else r["genome"]
        pr = predict(g); a = arith(g); tr = truth(g); tr2 = truth(g, seed=8)
        s = score_static(pr, tr, tr2); sa = score_arith(a, tr, tr2)
        st[(pr[0], tr[0], s)] += 1
        ar[("none" if a is None else a[0], tr[0], sa)] += 1
        if "miss" in (s, sa) and len(ex) < 12: ex.append((len(g), pr, a, tr, tr2))
    print("genomes", len(R))
    print("static (pred, truth, score):"); [print(" ", k, v) for k, v in sorted(st.items())]
    print("arith (pred, truth, score):"); [print(" ", k, v) for k, v in sorted(ar.items())]
    for name, c in (("static", st), ("arith", ar)):
        tot = collections.Counter()
        for k, v in c.items(): tot[k[2]] += v
        print(name, "totals", dict(sorted(tot.items())))
    print("misses:", *ex, sep="\n  ")
