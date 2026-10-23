# Plan #449: rerun tagged seed 2 exactly as job_tagged.py did (same World args, same update loop) and dump every
# genotype alive at update 100,000 with its count and current tasks, so the rare AND carriers can be traced.
# Reproduction check: the top genotype must equal out/tagged_s2.json's last "top".
import json, os, sys, shutil, platform
if platform.python_implementation() != 'PyPy' and shutil.which('pypy3'):
    os.execv(shutil.which('pypy3'), ['pypy3', os.path.abspath(__file__)])   # ~4x faster in CPU time
from collections import Counter, defaultdict
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from petri import World, ANCESTOR, show
w = World(side=30, seed=2, copy_mut=0.0075, parasites=False, raw_inputs=False)
w.inject(ANCESTOR, "ancestor")
for u in range(100000):
    w.run_update()
live = [o for o in w.cells if o is not None]
g = Counter(show(o.mem[:o.glen]) for o in live)
tasks = defaultdict(Counter)
for o in live:
    tasks[show(o.mem[:o.glen])][",".join(sorted(o.tasks))] += 1
ref = json.load(open(os.path.join(here, "out", "tagged_s2.json")))[-1]["top"]
out = {"update": w.update, "pop": len(live), "top_matches_tagged_s2": g.most_common(1)[0][0] == ref,
       "genotypes": [{"genome": k, "n": n, "tasks": dict(tasks[k])} for k, n in g.most_common()]}
json.dump(out, open(os.path.join(here, "out", "s2_dump.json"), "w"))
print(out["pop"], len(g), "genotypes; top matches:", out["top_matches_tagged_s2"])
