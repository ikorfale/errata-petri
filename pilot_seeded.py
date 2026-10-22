"""Pilot for experiment 1 (plan #421): spontaneous parasites never established (pilot_para_s101: 2,759 injections in
100k updates, never more than 3 hosts infected), so E1 needs a hand-seeded parasite. Does a hand-made one spread?
The parasite is the ancestor with h-divide replaced by inject + nop-B (label B, matches any host holding nop-C).
Young world (ancestor, parasites on) for WARM updates, then the parasite is placed as a thread in K random hosts.
Usage: python3 pilot_seeded.py SEED [WARM] [AFTER] [K] [PAD]"""
import json, sys, time
from petri import World, ANCESTOR, CODE, Org, show
def make_parasite(pad=85):
    """The ancestor with h-divide -> inject + nop-B and its nop-C padding cut from 85 to PAD."""
    g = list(ANCESTOR)
    i = g.index(CODE["h-divide"])
    g[i:i + 1] = [CODE["inject"], CODE["nop-B"]]
    return g[:6] + g[6 + 85 - pad:] if pad < 85 else g
PARASITE = make_parasite()
if __name__ != "__main__": raise SystemExit
seed = int(sys.argv[1]); warm, after, k, pad = (int(a) for a in (sys.argv[2:6] + ['2000', '5000', '9', '85'][len(sys.argv[2:6]):]))
PARASITE = make_parasite(pad)
w = World(seed=seed, parasites=True)
w.inject(ANCESTOR, "ancestor")
t0 = time.time()
for u in range(warm):
    w.run_update()
hosts = [o for o in w.cells if o is not None and o.para is None]
w.rng.shuffle(hosts)
for h in hosts[:k]:
    p = Org(PARASITE, "seeded-parasite", merit=0.0, born=w.update); p.is_para = True; h.para = p
print(json.dumps({"seed": seed, "parasite": show(PARASITE), "len": len(PARASITE), "seeded": min(k, len(hosts)),
                  "pop_at_seed": sum(o is not None for o in w.cells)}), flush=True)
for u in range(after):
    w.run_update()
    if (u + 1) % 250 == 0:
        live = [o for o in w.cells if o is not None]
        inf = [o.para for o in live if o.para is not None]
        print(json.dumps({"update": w.update, "pop": len(live), "infected": len(inf),
                          "seeded_lineage": sum(p.lineage == "seeded-parasite" for p in inf),
                          "injections": w.injections, "sec": round(time.time() - t0, 1)}), flush=True)
