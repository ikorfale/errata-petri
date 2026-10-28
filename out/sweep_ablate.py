# #555 part 2: which of the line's shared changes (pos 0 pop->IO, pos 4 nop-A->if-label, h-copy inserted at 88) carries
# the advantage? Each genome alone in a 5x5 world, no mutation, seeds 1-3: steps to first division and the child's merit.
# Fitness proxy = merit / steps (CPU share is proportional to merit, so replication rate ~ merit / gestation).
import pickle, random, sys, itertools
sys.path.insert(0, '.')
from petri import OPS, World
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
for _ in range(1000): w.run_update()
f0 = list(w.cells[235].mem[:w.cells[235].glen]); op = {n: i for i, n in enumerate(OPS)}
assert OPS[f0[0]] == 'pop' and OPS[f0[4]] == 'nop-A'
def make(m0, m4, ins):
    g = list(f0)
    if m0: g[0] = op['IO']
    if m4: g[4] = op['if-label']
    if ins: g = g[:88] + [op['h-copy']] + g[88:]
    return g
def run(g, seed, steps=20000):
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]
    for i in range(steps):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b:
            kid = next(x for x in v.cells if x is not None and x is not o)
            return i + 1, kid.merit, sorted(o.tasks) if o.tasks else None
    return None
for m0, m4, ins in itertools.product([0, 1], repeat=3):
    g = make(m0, m4, ins); r = [run(g, s) for s in (1, 2, 3)]
    ok = [x for x in r if x]
    fit = sum(x[1] / x[0] for x in ok) / len(ok) if ok else 0
    print(f"pop->IO={m0} nopA->if-label={m4} +h-copy={ins}: len {len(g)}  " +
          "  ".join(f"steps {x[0]} merit {x[1]:.0f}" if x else "no division" for x in r) + f"  merit/step {fit:.1f}", flush=True)
print("founder 80-97:", " ".join(f"{i}:{OPS[x]}" for i, x in enumerate(f0) if 80 <= i))
