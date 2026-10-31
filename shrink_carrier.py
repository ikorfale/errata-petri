"""Which genotype carries the day-2 shrink? Exploratory (31.10, plan #581). Re-runs method-1 replays of day 2 from the
saved day-1 world with Petri's own rule (unpatched engine), recording the top genotypes every 500 updates. Each arm
must reproduce out/mm_1_<seed>.json (glen_med, glen_mean every 1000 updates); a mismatch is recorded, not hidden.
Usage: python3 shrink_carrier.py [SEED ...] (default 14 28 11 21 23 26)  -> out/shrink_carrier_<seed>.json, one per seed"""
import json, os, pickle, sys, time, hashlib
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import petri
from petri import show
END = int(os.environ.get("SC_END", 80000))         # SC_END=41000 for a smoke test
for SEED in [int(s) for s in sys.argv[1:]] or [14, 28, 11, 21, 23, 26]:
    ref = {r["update"]: r for r in json.load(open(os.path.join(HERE, f"out/mm_1_{SEED}.json")))["rows"]}
    w = pickle.load(open(os.path.join(HERE, "daily/base/day-001/world.pkl"), "rb")); w.rng.seed(SEED)
    rows, bad, t0 = [], [], time.time()
    while w.update < END:
        w.run_update()
        if w.update % 500: continue
        live = [o for o in w.cells if o is not None]
        g = Counter(show(o.mem[:o.glen]) for o in live)
        gl = sorted(o.glen for o in live)
        med, mean = gl[len(gl) // 2], round(sum(gl) / len(gl), 2)
        if w.update in ref and (ref[w.update]["glen_med"], ref[w.update]["glen_mean"]) != (med, mean):
            bad.append([w.update, med, mean, ref[w.update]["glen_med"], ref[w.update]["glen_mean"]])
        rows.append({"update": w.update, "pop": len(live), "glen_med": med, "glen_mean": mean,
                     "len_hist": sorted(Counter(gl).most_common(6)),
                     "top": [[hashlib.sha256(s.encode()).hexdigest()[:12], n, len(s)] for s, n in g.most_common(5)]})
    json.dump({"seed": SEED, "secs": round(time.time() - t0), "mismatch_vs_mm1": bad, "rows": rows}, open(os.path.join(HERE, f"out/shrink_carrier_{SEED}" + ("" if END == 80000 else "_smoke") + ".json"), "w"))
    print(SEED, "secs", round(time.time() - t0), "mismatches", len(bad), "end med", rows[-1]["glen_med"], flush=True)
