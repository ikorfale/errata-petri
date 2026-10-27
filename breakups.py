"""#537: how many births in an evolving world are half-copy breakups (the parent keeps < 75% of its genome; the
child is then a rotation, see delete_kids_heads.py)? Default world from the ancestor, mutation on.
Usage: python3 breakups.py SEED UPDATES [SIDE] -> one JSON line per 250 updates and a final line."""
import json, sys, time
from petri import World, ANCESTOR
seed, U = int(sys.argv[1]), int(sys.argv[2]); side = int(sys.argv[3]) if len(sys.argv) > 3 else 20
w = World(side=side, seed=seed); w.inject(ANCESTOR, "ancestor")
n = {"births": 0, "breakup": 0, "breakup_parent_lens": {}}
_div = w.divide
def div(o, c):
    g0 = o.glen; b = w.births; _div(o, c)
    if w.births > b:
        n["births"] += 1
        if o.glen < 0.75 * g0:
            n["breakup"] += 1; k = f"{g0}->{o.glen}"; n["breakup_parent_lens"][k] = n["breakup_parent_lens"].get(k, 0) + 1
w.divide = div
t0 = time.time()
for u in range(U):
    w.run_update()
    if (u + 1) % 250 == 0 or u + 1 == U:
        top = sorted(n["breakup_parent_lens"].items(), key=lambda x: -x[1])[:5]
        print(json.dumps({"seed": seed, "update": u + 1, "births": n["births"], "breakup": n["breakup"],
                          "share": round(n["breakup"] / max(1, n["births"]), 4), "top": top, "sec": round(time.time() - t0)}), flush=True)
