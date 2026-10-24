"""Scoring driver for #491: applies scoring.py (the frozen rule) to a genome list. In-sample = the 1576 census genomes
(development data, NOT the test). Truth under seeds 7 and 8. Writes a summary to stdout and every miss and premise
failure, with its genome, to <out>.misses.json.
Usage: python3 static_insample.py [genomes.json] [out_prefix]"""
import sys, json, collections
sys.path.insert(0, ".")
from petri import parse
from static_lap import predict, arith
from laps_truth import truth
from math import gcd
from scoring import score_static, static_len, score_arith, arith_premise
if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "out/two_step_filter.json"
    pref = sys.argv[2] if len(sys.argv) > 2 else "out/static_insample"
    R = json.load(open(src))
    st = collections.Counter(); ar = collections.Counter(); pm = collections.Counter(); ln = collections.Counter()
    arj = collections.Counter(); cells = collections.Counter()
    tot = {"static": collections.Counter(), "arith-lap": collections.Counter()}; misses = []
    for r in R:
        gr = r["genome"] if isinstance(r, dict) else r
        g = parse(gr) if isinstance(gr, str) else gr
        pr = predict(g); a = arith(g)
        if isinstance(r, dict) and "static" in r:   # committed predictions must be what the frozen predictors give
            assert list(pr) == list(r["static"]) and (a is None and r["arith"] is None or list(a) == list(r["arith"])), r
        tr = truth(g); tr2 = truth(g, seed=8)
        s = score_static(pr, tr, tr2); sa = score_arith(a, tr, tr2); prem = arith_premise(a, tr, tr2)
        st[(pr[0], tr[0], s)] += 1; tot["static"][s] += 1
        ar[("none" if a is None else a[0], tr[0], sa)] += 1; tot["arith-lap"][sa] += 1
        if a is not None and sa in ("hit", "miss"):
            jk = "never" if a[0] == "never" else ("j=1" if a[1] == 1 else "j>=3")
            arj[(jk, "gcd>1" if gcd(len(g), a[1 + (a[0] == "exact")]) > 1 else "gcd=1", sa)] += 1
        if isinstance(r, dict) and "cell" in r:
            cells[(tuple(r["cell"]), "static " + s, "arith " + sa)] += 1
        if pr[0] == "other-birth": ln[(tr[0], static_len(pr, tr), tr == tr2)] += 1
        if prem is not None: pm[(a[0], tr[0] if tr2 == tr else tr[0] + "/" + tr2[0], prem)] += 1
        if s == "miss" or sa == "miss" or prem is False:
            misses.append({"genome": list(g), "L": len(g), "static": list(pr), "arith": None if a is None else list(a),
                           "truth7": list(tr), "truth8": list(tr2), "static_score": s, "arith_lap_score": sa,
                           "premise": prem})
    print("source", src, "genomes", len(R))
    print("static (pred, truth, score):"); [print(" ", k, v) for k, v in sorted(st.items())]
    print("static other-birth (reported, not scored): (truth7 class, length match, seed-stable):", dict(ln))
    print("arith lap claim (pred, truth, score):"); [print(" ", k, v) for k, v in sorted(ar.items())]
    print("arith lap claim by j and gcd(L, p) (j class, gcd, score):"); [print(" ", k, v) for k, v in sorted(arj.items())]
    if cells: print("targeted cells (cell, static score, arith lap score):"); [print(" ", k, v) for k, v in sorted(cells.items())]
    print("arith premise (pred, truth, holds):"); [print(" ", k, v) for k, v in sorted(pm.items())]
    for k, c in tot.items(): print(k, "totals", dict(sorted(c.items())))
    print("premise holds", sum(v for k, v in pm.items() if k[2]), "of", sum(pm.values()))
    json.dump(misses, open(pref + ".misses.json", "w"))
    print("misses and premise failures written:", len(misses), "->", pref + ".misses.json")
