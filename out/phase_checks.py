"""#488 step 2: r0 = 0 everywhere, so the phase must come from the loop. Record ncopy at each if-label execution:
copies per check (period) and the offset of the checks (ncopy mod period), parent vs the exact copiers."""
import sys, json, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse, OPS
def checks(g, cap=3000):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0); o = w.cells[0]
    at = []
    for n in range(cap):
        ip = o.heads[0] % len(o.mem)
        if OPS[o.mem[ip]] == "if-label": at.append((ip, o.ncopy))
        b = w.births; w.step(o, 0); o = w.cells[0]
        if w.births > b: break
    return at
from two_step_check import top
a = checks(top); print("parent L", len(top), "checks", len(a), "first", a[:4], "last", a[-2:])
R = json.load(open("out/two_step_filter.json"))
good = [r for r in R if r["faithful"] and r["solo"] >= 195]
c = collections.Counter()
for r in good:
    a = checks(r["genome"])
    gaps = collections.Counter(y[1] - x[1] for x, y in zip(a, a[1:]))
    c[(r["len"], tuple(sorted(gaps.items())), a[0][1] if a else None, tuple(sorted({ip for ip, _ in a})))] += 1
for k, v in sorted(c.items()): print("L, gaps, ncopy at 1st check, check ips:", k, "x", v)
