"""#488: why do L=96 AND+ANDN exact copiers divide fast when the parent's rule says L=96 never does?
Hypothesis (copy loop checks the label every 3 copies, exit when the last copied pair is the genome's end):
fast iff (L - r0) = c0 (mod 3), where r0 is the read head at the first h-copy. So an edit that moves r0 shifts e.
For the parent, block genomes and the 52 + 8 exact copiers: r0, copies at first division, L, (L - r0) mod 3."""
import sys, json, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse, OPS, RH
from two_step_check import edit, top, blk
def probe(g, cap=3000):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0); o = w.cells[0]
    r0 = None
    for n in range(cap):
        if OPS[o.mem[o.heads[0] % len(o.mem)]] == "h-copy" and r0 is None: r0 = o.heads[RH]
        b = w.births; nc = o.ncopy; w.step(o, 0); o = w.cells[0]
        if w.births > b: return r0, nc, n + 1   # h-divide does not copy (Fable 24.10: was nc + 1)
    return r0, None, cap
print("parent", len(top), probe(top), "(L-r0)%3 =", (len(top) - probe(top)[0]) % 3)
R = json.load(open("out/two_step_filter.json"))
good = [r for r in R if r["faithful"] and r["solo"] >= 195]
c = collections.Counter()
for r in good:
    r0, nc, n = probe(r["genome"])
    L = r["len"]; c[(L, r0, (L - r0) % 3, nc)] += 1
for k, v in sorted(c.items()): print("L, r0, (L-r0)%3, copies:", k, "x", v)
