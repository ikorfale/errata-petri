# #554 part 2b (theone 106797: glen next to len(mem)): is the 41,000 -> 43,000 coalescence a selective sweep? Track descendants of each census-41000 cell.
import pickle, random, sys, json
from collections import Counter, defaultdict
sys.path.insert(0, '.')
import daily
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
prevs = {}; root = {}   # root[cell at current census] = cell at census 41000 it descends from
for step in range(5):
    if step:
        for _ in range(500): w.run_update()
    live = {c: o for c, o in enumerate(w.cells) if o is not None}
    if w.update == 41000: root = {c: c for c in live}
    elif w.update > 41000: root = {c: root.get(o.anc) for c, o in live.items()}
    ls, prevs = daily.lineage_census(w, prevs)
    if w.update >= 41000:
        fam = Counter(root.values()); top = fam.most_common(1)[0]
        ins = [o for c, o in live.items() if root[c] == top[0]]; outs = [o for c, o in live.items() if root[c] != top[0]]
        def prof(os_):
            if not os_: return None
            t = Counter(k for o in os_ for k in (o.tasks | getattr(o, 'ptasks', set())))
            return {"n": len(os_), "merit": round(sum(o.merit for o in os_) / len(os_), 1),
                    "memlen": round(sum(len(o.mem) for o in os_) / len(os_), 1), "glen": round(sum(o.glen for o in os_) / len(os_), 1), "tasks": {k: round(v / len(os_), 2) for k, v in sorted(t.items())}}
        print(json.dumps({"u": w.update, "coal": ls["coal"], "top41000": top, "families": len(fam), "in": prof(ins), "out": prof(outs)}), flush=True)
