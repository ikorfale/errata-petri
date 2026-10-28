# #555: which genome change rode the fork sweep 41k->43k? Founder (cell 235 at 41,000) vs the commonest genomes of its line.
import pickle, random, sys, json, difflib
from collections import Counter
sys.path.insert(0, '.')
from petri import OPS
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
for _ in range(1000): w.run_update()
f0 = bytes(w.cells[235].mem[:w.cells[235].glen]); print("founder len", len(f0), "tasks", sorted(w.cells[235].tasks))
root = {c: c for c, o in enumerate(w.cells) if o is not None}
for c in root: w.cells[c].anc = c
def show(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return [(tag, i1, [OPS[x] for x in a[i1:i2]], [OPS[x] for x in b[j1:j2]]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != 'equal']
for step in range(3):
    for _ in range(500): w.run_update()
    live = {c: o for c, o in enumerate(w.cells) if o is not None}
    root = {c: root.get(getattr(o, 'anc', None)) for c, o in live.items()}
    for c, o in live.items(): o.anc = c
    fam = Counter(bytes(o.mem[:o.glen]) for c, o in live.items() if root[c] == 235)
    rest = Counter(bytes(o.mem[:o.glen]) for c, o in live.items() if root[c] != 235)
    print("u", w.update, "fam235", sum(fam.values()), "genotypes", len(fam), "| rest", sum(rest.values()))
    for g, n in fam.most_common(3):
        print("  in ", n, "len", len(g), "diff vs founder:", show(f0, g))
    if rest:
        g, n = rest.most_common(1)[0]; print("  out", n, "len", len(g), "diff vs founder:", show(f0, g)[:6])
