"""Fable 23.10 on #451: is the 9-insertion route to the five-task genotype passable one insertion at a time?
For each prefix k = 0..9 of the block 'ycuopcuyq' inserted before parent position 84: tasks in one gestation
(trace, seed 7), instructions per gestation, replication fidelity (distinct genomes after 150 solo updates, seeds 1-3),
and the merit proxy length * 2^bonus / gestation (rate relative to the parent)."""
import json, collections, sys
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, parse, show, TASKS
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
BON = {n: b for n, _, b in TASKS}; BLOCK = "ycuopcuyq"
def rate(g):
    log, n = trace(parse(g), 7, 1)
    t = sorted(set().union(*[set(r[7]) for r in log])) if log else []
    born = any(r[3] == "h-divide" for r in log)
    return t, n, len(g) * 2 ** sum(BON[x] for x in t) / n if n else 0
_, _, r0 = rate(TOP)
for k in range(10):
    g = TOP[:84] + BLOCK[:k] + TOP[84:]
    t, n, r = rate(g)
    fid = []
    for s in (1, 2, 3):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(150): w.run_update()
        c = collections.Counter(show(o.mem[:o.glen]) for o in w.cells if o is not None)
        fid.append((sum(c.values()), c.get(g, 0)))
    print(f"k={k} +{BLOCK[:k]:9s} len {len(g)} mod3 {len(g)%3} instr/gest {n:5d} tasks {','.join(t):26s} "
          f"rel.rate {r / r0:5.2f}  solo pop, parent-identical: {fid}", flush=True)
