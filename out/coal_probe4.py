# #554 part 4: branch at 42,000 of the original fork (seed 777 from the day-1 state; family 235 then ~464/865, merit +12%).
# Does family 235 still fix by 43,000-43,500 under other seeds? Yes in most -> its line carried an advantage by 42,000.
import pickle, random, sys, json
from collections import Counter
sys.path.insert(0, '.')
def census_step(w, root):
    """advance 500 updates; root maps cell -> founder at 41,000 via anc set at the previous census"""
    for _ in range(500): w.run_update()
    live = {c: o for c, o in enumerate(w.cells) if o is not None}
    root = {c: root.get(getattr(o, 'anc', None)) for c, o in live.items()}
    for c, o in live.items(): o.anc = c
    return root
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
for _ in range(1000): w.run_update()
root = {c: c for c, o in enumerate(w.cells) if o is not None}
for c in root: w.cells[c].anc = c
for _ in range(2): root = census_step(w, root)
f = Counter(root.values()); print(json.dumps({"u": w.update, "fam235": f.get(235, 0), "families": len(f), "top": f.most_common(2)}), flush=True)
blob = pickle.dumps((w, root))
for seed in [None, 11, 12, 13, 14, 15]:
    v, r = pickle.loads(blob)
    if seed is not None: v.rng = random.Random(seed)
    row = {}
    for _ in range(3):
        r = census_step(v, r); f = Counter(r.values()); row[v.update] = [len(f), f.get(235, 0), sum(f.values())]
    print(json.dumps({"seed": seed or "777-continued", "u: [families, fam235, live]": row}), flush=True)
