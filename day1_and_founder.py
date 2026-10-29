"""Day-1 AND sweep at 31.5k (plan #568): the founder (birth 1328814, born update 30783; 389 of 423 AND performers at
31.5k descend from it) and its parent, alone in a 5x5 world, seeds 1-3 (sweep_iso.run): steps to first division,
child's merit, tasks in that gestation. Did the same two point mutations add AND and remove NOT?
Reads out/day1_and_founders.json (replay_origins.py --no-lineage, day 1 from World(seed=20261028), digest 141ea0cf matched)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import OPS
from sweep_iso import run
f = json.load(open("out/day1_and_founders.json"))["1328814"]
g, p = bytes(f["genome"]), bytes(f["parent_genome"])
print("len", len(g), len(p), "diffs", [(i, OPS[p[i]], OPS[g[i]]) for i in range(len(g)) if g[i] != p[i]])
for name, x in (("parent", p), ("founder", g)):
    for s in (1, 2, 3): print(name, s, run(x, s))
for i in [i for i in range(len(g)) if g[i] != p[i]]:   # each mutation alone on the parent
    y = bytearray(p); y[i] = g[i]; print("parent+only", i, [run(bytes(y), s) for s in (1, 2, 3)])
