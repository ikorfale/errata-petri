"""Fable's diagnostic (22.10): are spontaneous parasites dead on arrival? Count injections made by parasite threads
(secondary) against all injections, parasites on, no seeding. Usage: python3 diag_secondary.py SEED UPDATES"""
import json, sys
from petri import World, ANCESTOR
w = World(seed=int(sys.argv[1]), parasites=True); w.inject(ANCESTOR, "ancestor")
for u in range(int(sys.argv[2])):
    w.run_update()
    if (u + 1) % 1000 == 0:
        print(json.dumps({"update": w.update, "injections": w.injections, "secondary": w.secondary,
                          "infected": sum(o is not None and o.para is not None for o in w.cells)}), flush=True)
