"""Viability control for h2h_and_mut: each genome alone, 20x20, mutation off, seeds 1-20.
Prints population at updates 50, 100 and the update the grid first fills (>=399)."""
import json, sys
sys.path.insert(0, ".")
from petri import World, parse
P = {m["edit"]: m["genome"] for m in json.load(open("out/and_mutants_s2.json"))}
D = json.load(open("out/s2_dump.json"))
TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
for name in ("parent", "del 71", "sub 69 y>a", "ins 71 a"):
    g = TOP if name == "parent" else P[name]
    rows = []
    for s in range(1, 21):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        p50 = p100 = full = None
        for u in range(1, 301):
            w.run_update()
            n = sum(o is not None for o in w.cells)
            if u == 50: p50 = n
            if u == 100: p100 = n
            if full is None and n >= 399: full = u
        rows.append((p50, p100, full))
    import statistics as st
    fulls = [r[2] for r in rows if r[2]]
    print(f"{name:12s} pop@50 mean {st.mean(r[0] for r in rows):6.1f}  pop@100 mean {st.mean(r[1] for r in rows):6.1f}  "
          f"filled in {len(fulls)}/20, median update {st.median(fulls) if fulls else None}", flush=True)
