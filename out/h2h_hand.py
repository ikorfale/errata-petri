"""zenith 99171: s2 dominant vs its one-step AND mutants, head to head. 20x20, mutation off, 300 updates,
seeds 1-20, both placements. Prints mutant share of the living at updates 100 and 300."""
import json, sys
sys.path.insert(0, ".")
import os, petri
from petri import World, parse
if os.environ.get("AND_EXP"):            # Fable 23.10 control: give AND the ANDN exponent so both sides are x128
    petri.TASKS[:] = [(n, f, int(os.environ["AND_EXP"]) if n == "AND" else b) for n, f, b in petri.TASKS]
P = {m["edit"]: m["genome"] for m in json.load(open("out/and_mutants_s2.json"))}
D = json.load(open("out/s2_dump.json"))
TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
NAME = sys.argv[1]                      # "hand": the hand-built AND+ANDN genome (#451)
MUT = TOP[:84] + "oypcupcncuyq" + TOP[84:] if NAME == "hand" else (TOP if NAME == "self" else P[NAME])
for s in range(1, 21):
    for swap in (0, 1):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        a, b = (0, 210) if swap == 0 else (210, 0)
        w.inject(parse(TOP), "par", cell=a); w.inject(parse(MUT), "mut", cell=b)
        for u in range(300):
            w.run_update()
        live = [o.lineage for o in w.cells if o is not None]
        print(NAME, os.environ.get("AND_EXP", "2"), s, swap, len(live), live.count("mut"), round(live.count("mut") / max(1, len(live)), 3), flush=True)
