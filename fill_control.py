"""#481 positive control for fill_scan.py: same run/fit/neigh code, but the base is a one-step mutant of the dominant
that lost a task and still divides. A working scanner must find at least the reversion: a one-step mutant of the weak
base that gains a task and is fitter than the base. Usage: python3 fill_control.py NBASES SEED"""
import sys, json, random, time
sys.path.insert(0, ".")
src = open("fill_scan.py").read().split("t0, n0 = run(top)")[0]    # definitions only, not the scan loop
exec(src)
t0, n0 = run(top); F0 = fit(top, t0, n0)
nb, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
losers = []
for x in neigh(top):
    tx, nx = run(x)
    if nx < CAP and set(tx) < set(t0): losers.append((x, tx, nx))
print(json.dumps({"dominant_tasks": t0, "losers": len(losers)}), flush=True)
for w, tw, nw in rng.sample(losers, min(nb, len(losers))):
    Fw = fit(w, tw, nw); found = 0; rev = 0; s = time.time(); seen = set()
    for x in neigh(w):
        if x in seen: continue
        seen.add(x); tx, nx = run(x)
        if set(tx) - set(tw) and nx < CAP and fit(x, tx, nx) > Fw:
            found += 1; rev += (x == top)
    print(json.dumps({"lost": sorted(set(t0) - set(tw)), "relfit_base": round(Fw / F0, 3), "gain_fitter": found,
                      "reversion_found": rev, "sec": round(time.time() - s, 1)}), flush=True)
