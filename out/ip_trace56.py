"""zenith 100881 guess: in the 56 one-step AND+ANDN activators, control enters the block and never returns to the copy loop.
For each, run 20000 steps alone and record the ip visits: last 2000 steps' ip range, whether ip visits the parent's
copy-loop indices (59..92 in the parent coordinates; shifted by +1/-1 for edits before them) after first entering the block."""
import sys, json, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse
from two_step_check import edit, top, blk
starts = [(s["p"], s["first"]) for s in json.load(open("out/two_step.json"))]
res = collections.Counter(); rows = []
for p, e in starts:
    g = edit(top[:p] + blk + top[p + 12:], e)
    w = World(side=5, seed=7, copy_mut=0.0); w.inject(parse(g), "t", cell=0); o = w.cells[0]
    ips = []
    for n in range(20000):
        ips.append(o.heads[0] % len(o.mem)); w.step(o, 0); o = w.cells[0]
    tail = ips[-2000:]
    entered = next((i for i, x in enumerate(ips) if p <= x < p + 12), None)
    after = ips[entered:] if entered is not None else []
    back = any(x >= 60 for x in after)
    loop = sorted(set(tail))
    rows.append((p, e, entered, back, min(tail), max(tail), len(loop)))
    res[(entered is not None, back)] += 1
for r in rows: print(r)
print("(entered block, returned to >=60 after):", dict(res))
