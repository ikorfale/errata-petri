# #554 part 3: replay 41,000 -> 43,000 from the same state under other seeds. Selection: family 235 wins repeatedly. Drift: winners vary.
import pickle, random, sys, json, copy
from collections import Counter
sys.path.insert(0, '.')
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
for _ in range(1000): w.run_update()
assert w.update == 41000
blob = pickle.dumps(w)
for seed in [777, 1, 2, 3, 4, 5]:
    v = pickle.loads(blob); v.rng = random.Random(seed)
    for c, o in enumerate(v.cells):
        if o is not None: o.anc = c
    out = {}
    for _ in range(4):
        for _ in range(500): v.run_update()
        fam = Counter(o.anc for o in v.cells if o is not None)
        out[v.update] = [len(fam), fam.get(235, 0), fam.most_common(1)[0]]
    print(json.dumps({"seed": seed, "per_census[families, fam235, top]": out}), flush=True)
