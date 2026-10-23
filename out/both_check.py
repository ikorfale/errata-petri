"""Viability and head-to-head for the double-insertion AND+ANDN genotypes found by and_pairs_s2.py.
Solo: 20x20, mutation off, seeds 1-10, pop at update 150 (parent 259.5). H2H vs parent: seeds 1-20 x 2 placements."""
import json, sys, statistics as st
sys.path.insert(0, ".")
from petri import World, parse
D = json.load(open("out/s2_dump.json"))
TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
rows = [l.split() for l in open("out/and_pairs_s2.txt") if l.startswith("BOTH")]
def solo(g):
    out = []
    for s in range(1, 11):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(150): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
def h2h(g):
    sh = []
    for s in range(1, 21):
        for a, b in ((0, 210), (210, 0)):
            w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
            w.inject(parse(TOP), "par", cell=a); w.inject(parse(g), "mut", cell=b)
            for u in range(300): w.run_update()
            live = [o.lineage for o in w.cells if o is not None]
            sh.append(live.count("mut") / max(1, len(live)))
    return st.mean(sh), sum(x >= 0.5 for x in sh)
for r in rows:
    g = r[-1]; edit = " ".join(r[1:5]); tasks = " ".join(r[5:-1])
    p = solo(g)
    line = f"{edit:12s} {tasks:45s} solo pop@150 {p:6.1f}"
    if p >= 259.5 / 2:
        m, k = h2h(g); line += f"  h2h share {m:.3f} ({k}/40 >= 0.5)"
    print(line, flush=True)
