"""zenith 105489: is the dual patch's low birth total compounding near criticality (only founders are slow) or a cost
that persists in later generations? Same patch arm as dual_insert.py (seeds, warm-up, 5x6 block at mean merit), with a
generation tag: founders 0, a child = parent's generation + 1. Per generation, over organisms whose life ended (dead
before the cap; alive ones are censored and counted apart): mean offspring, P(divided at least once), updates from birth
to first division, merit at birth / world mean at birth. Residents born after insertion are the comparison group.
Usage: python3 dual_gens.py dual|control SEED[,SEED] [UPDATES] -> out/dual_gens.jsonl"""
import json, sys, time
from collections import defaultdict
from petri import World, parse
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
DUAL = sorted(json.load(open("out/and_andn_dup.json")), key=lambda h: (h["len"], h["a"], h["place"]))[0]["genome"]
arm = sys.argv[1]; seeds = [int(s) for s in sys.argv[2].split(",")]; ups = int(sys.argv[3]) if len(sys.argv) > 3 else 400
for s in seeds:
    w = World(seed=s); t0 = time.time()
    for c in range(w.n): w.inject(parse(TOP), "s2", cell=c)
    cell = w.rng.randrange(w.n)
    for _ in range(50): w.run_update()
    r0, c0 = divmod(cell, w.side)
    cells = [((r0 + i) % w.side) * w.side + (c0 + j) % w.side for i in range(5) for j in range(6)]
    live = [o for o in w.cells if o is not None]; m = sum(o.merit for o in live) / len(live)
    rec = {}   # id(org) -> [org, group, gen, born, kids, first_div_update, merit_ratio_at_birth]
    for x in cells:
        w.inject(parse(DUAL if arm == "dual" else TOP), "seed", cell=x); o = w.cells[x]; o.merit = m
        rec[id(o)] = [o, "seed", 0, w.update, 0, None, 1.0]
    _div, _nb, tgt = w.divide, w.neighbour, [None]
    def nb(c, _nb=_nb, tgt=tgt):
        t = _nb(c); tgt[0] = t; return t
    w.neighbour = nb
    def divide(o, c, _div=_div, w=w, rec=rec, tgt=tgt):
        n0 = w.births; tgt[0] = None; _div(o, c)
        if w.births == n0: return
        r = rec.get(id(o))
        if r is not None and r[0] is not o: r = None
        kid = w.cells[tgt[0]]; lv = [x.merit for x in w.cells if x is not None]; ratio = kid.merit / (sum(lv) / len(lv))
        if r is not None:
            r[4] += 1
            if r[5] is None: r[5] = w.update
            rec[id(kid)] = [kid, r[1], r[2] + 1, w.update, 0, None, ratio]
        elif o.lineage == "s2":
            rec[id(kid)] = [kid, "resident", 0, w.update, 0, None, ratio]
    w.divide = divide
    for u in range(1, ups + 1):
        w.run_update()
        if not any(o is not None and o.lineage == "seed" for o in w.cells): break
    alive = {id(o) for o in w.cells if o is not None}
    gens = defaultdict(lambda: {"n": 0, "censored": 0, "kids": 0, "divided": 0, "t_first": 0.0, "ratio": 0.0})
    for k, (o, grp, g, born, kids, fd, ratio) in rec.items():
        key = "resident" if grp == "resident" else f"g{min(g, 5)}"
        G = gens[key]
        if k in alive:   # rec holds the object, so ids are never reused
            G["censored"] += 1; continue
        G["n"] += 1; G["kids"] += kids; G["ratio"] += ratio
        if fd is not None: G["divided"] += 1; G["t_first"] += fd - born
    row = {"arm": arm, "seed": s, "updates_run": w.update - 50, "sec": round(time.time() - t0), "gens": {}}
    for key in sorted(gens):
        G = gens[key]; n = G["n"]
        row["gens"][key] = {"dead": n, "alive_censored": G["censored"], "mean_kids": round(G["kids"] / max(1, n), 3),
                            "p_divided": round(G["divided"] / max(1, n), 3),
                            "upd_to_first_div": round(G["t_first"] / max(1, G["divided"]), 2),
                            "merit_over_mean_at_birth": round(G["ratio"] / max(1, n), 3)}
    print(json.dumps(row), flush=True)
    open("out/dual_gens.jsonl", "a").write(json.dumps(row) + "\n")
