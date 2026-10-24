"""Are the 81 'child of genome length, ncopy not k*L' births of the census (odd_lap_census.py, #101122) rotations of
the parent? Carve the child exactly as petri does at the dividing step and compare it with every cyclic shift."""
import sys, json, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse, OPS, RH, WH
R = json.load(open("out/two_step_filter.json")); c = collections.Counter(); shifts = collections.Counter()
for r in R:
    g = r["genome"]; L = len(g)
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0); o = w.cells[0]
    for n in range(3000):
        ip = o.heads[0] % len(o.mem)
        if OPS[o.mem[ip]] == "h-divide":
            cut = w.carve(o)
            if cut is not None:
                child = bytes(cut[0]); par = bytes(o.mem[:o.glen]); nc = o.ncopy; break
        w.step(o, 0); o = w.cells[0]
    else:
        c["no carve in 3000"] += 1; continue
    if len(child) != L: c["child not genome length"] += 1; continue
    if nc % L == 0: c["exact (ncopy = jL)"] += 1; continue
    rot = [k for k in range(L) if child == par[k:] + par[:k]]
    c["ncopy not jL: rotation of parent" if rot else "ncopy not jL: NOT a rotation"] += 1
    if rot: shifts[(nc % (2 * L), rot[0])] += 1
for k, v in sorted(c.items()): print(k, v)
print("(ncopy mod 2L, rotation shift): count, top 8:", shifts.most_common(8))

# do the rotated children reproduce? run each one solo the same way, and classify its own first carve
from petri import OPS as _O
def first_carve(gb):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(bytearray(gb), "t", cell=0); o = w.cells[0]
    for n in range(3000):
        if _O[o.mem[o.heads[0] % len(o.mem)]] == "h-divide":
            cut = w.carve(o)
            if cut is not None: return bytes(cut[0]), o.ncopy, n
        w.step(o, 0); o = w.cells[0]
    return None, None, None
k2 = collections.Counter()
for r in R:
    g = r["genome"]; L = len(g); par = bytes(parse(g))
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0); o = w.cells[0]
    ch = None
    for n in range(3000):
        if _O[o.mem[o.heads[0] % len(o.mem)]] == "h-divide":
            cut = w.carve(o)
            if cut is not None: ch, nc = bytes(cut[0]), o.ncopy; break
        w.step(o, 0); o = w.cells[0]
    if ch is None or len(ch) != L or nc % L == 0: continue
    gc, nc2, steps = first_carve(ch)
    if gc is None: k2["rotated child: no carve in 3000"] += 1
    elif gc == ch: k2["rotated child: copies itself exactly"] += 1
    elif gc == par: k2["rotated child: gives back the parent"] += 1
    elif len(gc) == L and any(gc == ch[s:] + ch[:s] for s in range(L)): k2["rotated child: another rotation"] += 1
    else: k2[f"rotated child: other child, length {len(gc)}"] += 1
for k, v in sorted(k2.items()): print(k, v)
