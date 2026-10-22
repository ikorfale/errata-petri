"""Epoch 1 world (plan #433): a fresh world from the ancestor, current rules (tagged inputs, no parasites),
run to update 2000 and saved, so seeds can be inserted into exactly this state. Writes out/epoch1_world.pkl
and out/epoch1_incumbents.json (top genotypes by count). Usage: python3 epoch_world.py [SEED] [UPDATES]"""
import json, pickle, sys, hashlib
from collections import Counter
from petri import World, ANCESTOR, show
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 2026; ups = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
w = World(seed=seed); w.inject(ANCESTOR, "ancestor")
for _ in range(ups): w.run_update()
pickle.dump(w, open("out/epoch1_world.pkl", "wb"))
live = [o for o in w.cells if o is not None]; g = Counter(show(o.mem[:o.glen]) for o in live)
out = {"world_seed": seed, "update": w.update, "pop": len(live), "genotypes": len(g), "census": w.census()["tasks_now"],
       "top": [{"genome": k, "count": n, "len": len(k), "sha256": hashlib.sha256(k.encode()).hexdigest()} for k, n in g.most_common(10)],
       "pickle_sha256": hashlib.sha256(open("out/epoch1_world.pkl", "rb").read()).hexdigest()}
json.dump(out, open("out/epoch1_incumbents.json", "w"), indent=1); print(json.dumps(out)[:600])
