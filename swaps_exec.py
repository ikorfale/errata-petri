"""Is 90's 1-3% merit-per-step edge an unexecuted instruction paid for by merit = copied size (petri.py:326, Avida's
BASE_MERIT_METHOD 1; Avida's default is 4 = min(executed, copied))? Top 3 genotypes of 89 and 90 at the 68k-72k flip,
alone in a 5x5 world, no mutation, seed 1: genome positions the IP visits during the first gestation."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import World, IP
C = {c["update"]: c for c in json.load(open("daily/replay-day-002-swaps.json"))["censuses"]}
for u in (70000, 72000):
    for l in ("89", "90"):
        for t in C[u]["top"][l]:
            g = bytes.fromhex(t["g"]); v = World(side=5, seed=1, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0)
            o = v.cells[0]; seen = set()
            for i in range(20000):
                b = v.births; seen.add(o.heads[IP] % len(g)); v.step(o, 0)
                if v.births > b: break
            print(f"{u} len {l} {t['n']:>3} copies: executed {len(seen)} of {len(g)}, never executed {len(g) - len(seen)}")
