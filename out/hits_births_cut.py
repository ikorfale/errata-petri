"""#451 audit follow-up (Fable 23.10): for each one-off birth in out/hits_births_s2.txt, log what carve() actually cut:
child and residual parent genomes, compared with the mother genome (faithful copy or mis-cut fragment?)."""
import json, sys
sys.path.insert(0, ".")
import petri
from petri import World, parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = "abcdefghijklmnopqrstuvwxyz"
def sub(g, i, a, j, b): return g[:i] + a + g[i + 1:j] + b + g[j + 1:]
cases = [("low 5 y 82 h", sub(top, 5, "y", 82, "h"), 5), ("low 12 b 84 v", sub(top, 12, "b", 84, "v"), 5),
         ("del-first parent[93]", top[:93] + top[94:], 1), ("parent", top, 1)]
dec = lambda m: "".join(AL[x] if x < 26 else "?" for x in m)
for name, g, s in cases:
    w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
    cuts = []; orig = w.carve
    def carve(o, orig=orig):
        r = orig(o)
        if r is not None and len(cuts) < 1: cuts.append((w.update, dec(o.mem[:o.glen]), dec(r[0]), dec(r[1])))
        return r
    w.carve = carve; w.inject(parse(g), "x", cell=0)
    for u in range(150): w.run_update()
    print(f"== {name} seed {s}: births {w.births}")
    for up, mother, child, par in cuts:
        print(f"  update {up}: genome {g}\n  child  {child} (len {len(child)}, == genome: {child == g})\n  parent {par} (len {len(par)}, == genome: {par == g})")
