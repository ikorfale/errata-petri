"""Plan #426, PREREG-seed.md: can a seed sent under the SUBMIT.md rules live in the mature daily world?
Loads a copy of daily/world.pkl (never writes it), injects 9 copies of one genome under the label "seed", and runs
until the label is extinct, fixed (every living organism carries it: then only total extinction could end it), or the
horizon. Arms: genome ANC (the hand-designed ancestor) or DOM (the world's most common genome at load), start merit
"len" (the SUBMIT rule: merit = genome length) or "mean" (the population's mean merit at injection).
Usage: python3 seed_entry.py WORLD.pkl HORIZON SEEDS(1,2,..) [ARMS ANC-len,DOM-len,ANC-mean,DOM-mean] [PROCS]"""
import json, os, pickle, random, sys, time
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri
from petri import ANCESTOR, show
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "seed_entry")
K, LOG_EVERY = 9, 500

def run(job):
    path, horizon, seed, arm = job
    w = pickle.load(open(path, "rb"))
    live = [o for o in w.cells if o is not None]
    for o in live:
        o.lineage = "native"
    dom = Counter(bytes(o.mem[:o.glen]) for o in live).most_common(1)[0][0]
    g = list(ANCESTOR) if arm.startswith("ANC") else list(dom)
    mean = sum(o.merit for o in live) / len(live)
    cells = random.Random(7000 + seed).sample(range(w.n), K)   # same cells for every arm of a seed
    w.rng = random.Random(9000 + seed)                           # same world RNG for every arm of a seed
    for c in cells:
        w.inject(g, "seed", cell=c)
        if arm.endswith("mean"):
            w.cells[c].merit = mean
    u0, rows, end, seedbirths, mx = w.update, [], "horizon", 0, K
    t0 = time.time()
    while w.update - u0 < horizon:
        before = set(o for o in w.cells if o is not None and o.lineage == "seed")   # objects kept alive: no id reuse
        w.run_update()
        now = [o for o in w.cells if o is not None]
        s = [o for o in now if o.lineage == "seed"]
        seedbirths += sum(1 for o in s if o not in before)
        mx = max(mx, len(s))
        du = w.update - u0
        if du % LOG_EVERY == 0 or not s or len(s) == len(now):
            rows.append({"du": du, "seed": len(s), "pop": len(now), "seed_births": seedbirths})
        if not s:
            end = "extinct"; break
        if len(s) == len(now):
            end = "fixed"; break
    res = {"seed": seed, "arm": arm, "genome_len": len(g), "genome_sha12": __import__("hashlib").sha256(show(g).encode()).hexdigest()[:12],
           "start_merit": len(g) if arm.endswith("len") else mean, "mean_merit": mean, "cells": cells,
           "end": end, "end_du": w.update - u0, "seed_births": seedbirths,
           "max_seed": mx, "secs": round(time.time() - t0), "rows": rows}
    with open(os.path.join(OUT, f"{arm}_s{seed}.json"), "w") as f:
        json.dump(res, f)
    print(arm, seed, end, res["end_du"], "births", seedbirths, "max", res["max_seed"], flush=True)
    return res

if __name__ == "__main__":
    path, horizon = sys.argv[1], int(sys.argv[2])
    seeds = [int(x) for x in sys.argv[3].split(",")]
    arms = (sys.argv[4] if len(sys.argv) > 4 else "ANC-len,DOM-len,ANC-mean,DOM-mean").split(",")
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    os.makedirs(OUT, exist_ok=True)
    jobs = [(path, horizon, s, a) for a in arms for s in seeds]
    with Pool(procs) as p:
        p.map(run, jobs, chunksize=1)
