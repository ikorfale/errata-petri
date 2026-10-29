"""Neutral baseline for OR-origin persistence (29.10). Of 108 OR origins on day 2, 107 were seen at one census only (gone
within 500 updates); the 62,369 line was seen at 36. Is that what a neutral new lineage would do? Tag every live organism
in a saved world with its own label (Org.lineage, which the dynamics never read), run 1,000 updates with the world RNG
reseeded, and count at +500 and +1000 the share of labels that still have living descendants, and the share whose living
descendants include one with the ancestor's exact task set (the analogue of "still OR-capable"). Tasks as in the run.
Usage: python3 neutral_survival.py [start_pkl] [seeds]"""
import json, os, pickle, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri
START = sys.argv[1] if len(sys.argv) > 1 else "out/sweeps/w62500.pkl"
SEEDS = range(1, 1 + int(sys.argv[2] if len(sys.argv) > 2 else 4))
def ts(o): return frozenset(o.tasks) | frozenset(getattr(o, "ptasks", None) or ())
print(json.dumps({"start": START}), flush=True)
for seed in SEEDS:
    w = pickle.load(open(START, "rb"))
    live = [o for o in w.cells if o is not None]
    anc = {}
    for i, o in enumerate(live): o.lineage = "L%d" % i; anc[o.lineage] = ts(o)
    w.rng = random.Random(seed); t0 = w.update; out = {"seed": seed, "n0": len(live)}
    for dt in (500, 1000):
        while w.update < t0 + dt: w.run_update()
        alive, kept = set(), set()
        for o in w.cells:
            if o is None or o.lineage not in anc: continue
            alive.add(o.lineage)
            if ts(o) == anc[o.lineage]: kept.add(o.lineage)
        out["+%d" % dt] = {"with_descendants": len(alive), "same_tasks": len(kept)}
    print(json.dumps(out), flush=True)
