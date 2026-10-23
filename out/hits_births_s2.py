"""#451 audit (23.10, theone 99607): "dividing" in and_insdel_s2 / and_subpairs(_low)_s2 was a population cutoff
(mean solo pop@150 >= 130), not observed division. Re-run every AND+ANDN hit with births counted per seed:
births (World.births, successful divide() only), final pop, same-genotype pop, update of first birth.
Controls: the parent (s2 dominant) and, for the ins+del hit, both one-edit intermediates in PARENT coordinates
(insert e at 70 only; delete parent[93] only = index 94 after the insertion)."""
import json, re, sys
sys.path.insert(0, ".")
from petri import World, parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
def run(g, seeds=range(1, 6), T=150):
    rows = []
    for s in seeds:
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0); first = None
        for u in range(T):
            w.run_update()
            if first is None and w.births: first = w.update
        live = [o for o in w.cells if o is not None]
        same = sum(bytes(o.mem[:o.glen]) == bytes(parse(g)) for o in live) if hasattr(live[0] if live else None, "glen") else None
        rows.append((s, w.births, len(live), same, first))
    return rows
cases = [("parent", top)]
ins = top[:70] + "e" + top[70:]
cases += [("insdel ins-first e@70", ins), ("insdel del-first parent[93]", top[:93] + top[94:]),
          ("insdel hit", ins[:94] + ins[95:])]
for f in ("out/and_subpairs_s2.txt", "out/and_subpairs_low_s2.txt"):
    for line in open(f):
        if line.startswith("BOTH"): cases.append((f.split("/")[1][:-4] + " " + " ".join(line.split()[1:5]), line.split()[-1]))
seen = set()
for name, g in cases:
    if g in seen: continue
    seen.add(g); r = run(g)
    print(f"{name:45} len {len(g)} births {[x[1] for x in r]} final_pop {[x[2] for x in r]} same_genotype {[x[3] for x in r]} first_birth {[x[4] for x in r]}", flush=True)
