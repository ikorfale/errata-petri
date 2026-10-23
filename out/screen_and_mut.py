"""Viability screen of all 38 one-step AND mutants of the s2 dominant: alone, 20x20, mutation off, seeds 1-10,
population at update 150 (parent ~ 250). Viable = mean pop >= half the parent's."""
import json, sys, statistics as st
sys.path.insert(0, ".")
from petri import World, parse
M = json.load(open("out/and_mutants_s2.json"))
D = json.load(open("out/s2_dump.json"))
TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
def pop150(g):
    out = []
    for s in range(1, 11):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(150): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
base = pop150(TOP)
print(f"parent pop@150 mean {base:.1f}")
for m in M:
    p = pop150(m["genome"])
    print(f"{m['edit']:12s} {','.join(m['tasks']):22s} pop@150 {p:6.1f} {'VIABLE' if p >= base / 2 else 'not viable'}", flush=True)
