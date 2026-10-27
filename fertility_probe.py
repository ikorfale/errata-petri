"""zenith 105489 follow-up: is there a per-generation cost of the 112-letter dual genome? A parent alone in a 5x5 world
with the real mutation rates (copy_mut 0.0075, indel 0.05) divides once; the child is then run alone without mutation
for up to CAP steps. Per genome: instructions the parent needs to its first division, share of children that ever
divide (fertile), and share whose first division still earns AND and ANDN. Usage: python3 fertility_probe.py N"""
import json, sys
from petri import World, parse
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
DUAL = sorted(json.load(open("out/and_andn_dup.json")), key=lambda h: (h["len"], h["a"], h["place"]))[0]["genome"]
N = int(sys.argv[1]); CAP = 3000
def first_div(g, seed, mut):
    w = World(side=5, seed=seed, copy_mut=0.0075 if mut else 0.0, indel=0.05 if mut else 0.0)
    w.inject(list(g), "t", cell=0); o = w.cells[0]; n = 0; snap = []
    _div = w.divide
    def div(o2, c, _div=_div): snap.append(set(o2.tasks)); _div(o2, c)
    w.divide = div
    while n < CAP:
        b = w.births; w.step(o, 0); n += 1
        if w.cells[0] is not o: return None
        if w.births > b:
            kid = next(x for i, x in enumerate(w.cells) if i and x is not None)
            return n, snap[-1], list(kid.mem[:kid.glen])
    return None
for name, g in (("resident", TOP), ("dual", DUAL)):
    r = first_div(parse(g), 1, False); fert = keep = 0; steps = []
    for s in range(N):
        p = first_div(parse(g), 1000 + s, True)
        if p is None: continue
        c = first_div(p[2], 5000 + s, False)
        if c is None: continue
        fert += 1; steps.append(c[0]); keep += {"AND", "ANDN"} <= c[1]
    print(json.dumps({"genome": name, "len": len(parse(g)), "steps_to_first_div_clean": r[0] if r else None, "children": N,
                      "fertile": fert, "p_fertile": round(fert / N, 3), "p_child_keeps_AND_ANDN": round(keep / N, 3), "tasks_clean": sorted(r[1]) if r else None, "median_child_steps": sorted(steps)[len(steps)//2] if steps else None}))
