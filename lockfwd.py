"""Forward lock-in test (PREDICT-lockin-1031.md, addendum A1). Stage a: fresh method-1 day-2 replays (seeds 33-40) run
from the saved day-1 world to update 50,000 only; each world is pickled there and only the 40,500-50,000 snapshots are
written. Stage b (a separate job, queued after the predictions are committed) continues each pickled world to 80,000.
Usage: python3 lockfwd.py a|b  -> out/lockfwd_<seed>_a.json + out/lockfwd_<seed>_50k.pkl, or out/lockfwd_<seed>_b.json"""
import json, os, pickle, sys, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import petri
SEEDS, STAGE = [33, 34, 35, 36, 37, 38, 39, 40], sys.argv[1]
for SEED in SEEDS:
    pk = os.path.join(HERE, f"out/lockfwd_{SEED}_50k.pkl")
    if STAGE == "a":
        w = pickle.load(open(os.path.join(HERE, "daily/base/day-001/world.pkl"), "rb")); w.rng.seed(SEED); end = 50000
    else:
        w = pickle.load(open(pk, "rb")); end = 80000
    rows, t0 = [], time.time()
    while w.update < end:
        w.run_update()
        if w.update % 500: continue
        gl = sorted(o.glen for o in w.cells if o is not None)
        rows.append({"update": w.update, "pop": len(gl), "glen_med": gl[len(gl) // 2],
                     "glen_mean": round(sum(gl) / len(gl), 2), "len_hist": sorted(Counter(gl).most_common(6))})
    if STAGE == "a": pickle.dump(w, open(pk, "wb"))
    json.dump({"seed": SEED, "stage": STAGE, "secs": round(time.time() - t0), "rows": rows},
              open(os.path.join(HERE, f"out/lockfwd_{SEED}_{STAGE}.json"), "w"))
    print(SEED, STAGE, "secs", round(time.time() - t0), flush=True)
