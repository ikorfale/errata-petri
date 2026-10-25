"""#481 positive control re-scored with the true merit (Fable 25.10): same bases as fill_control.py (same seed, same
loser list), but fitness = merit paid at the first division / steps (run3 from copylen_probe.py), CAP 1000.
Usage: python3 fill_control_merit.py NBASES SEED"""
import sys, json, random, time
sys.path.insert(0, ".")
exec(open("fill_scan.py").read().split("t0, n0 = run(top)")[0])
exec(open("copylen_probe.py").read().split("T0, N0, L0, M0 = run3")[0].split("from petri import World, OPS")[1])
from petri import World, OPS
t0, n0 = run(top); T0, N0, L0, M0 = run3(top, CAP); F0 = M0 / N0
nb, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
losers = []
for x in neigh(top):
    tx, nx = run(x)
    if nx < CAP and set(tx) < set(t0): losers.append((x, tx, nx))
print(json.dumps({"dominant_tasks": T0, "losers": len(losers)}), flush=True)
for w, tw, nw in rng.sample(losers, min(nb, len(losers))):
    Tw, Nw, Lw, Mw = run3(w, CAP); Fw = Mw / Nw if Nw < CAP else 0.0; found = 0; rev = 0; s = time.time(); seen = set()
    for x in neigh(w):
        if x in seen: continue
        seen.add(x); t, n, L, m = run3(x, CAP)
        if n < CAP and set(t) - set(Tw) and m / n > Fw:
            found += 1; rev += (x == top)
    print(json.dumps({"lost": sorted(set(T0) - set(Tw)), "relfit_base": round(Fw / F0, 3), "gain_fitter": found,
                      "reversion_found": rev, "sec": round(time.time() - s, 1)}), flush=True)
