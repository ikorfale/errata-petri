"""#481 Fable 25.10 (blocking): merit = copied length, not genome length, and a child may be up to 2x the parent.
Both scans scored fitness with len(genome). Re-run fills 0..NF-1 of seed 1 (same fill sequence as fill_scan/cap_probe)
and score every one-step mutant by the merit actually paid at its first division (kid.merit) per step, CAP 1000, and
the CAP-1000 hitters again at 6300. Reports child lengths and fitter task-gainers under the true merit.
Usage: copylen_probe.py NF SEED [BIG]  (12500 covers net +5 bits at the 2x child limit: 32*194*190/95 = 12416)"""
import sys, json, random, time
sys.path.insert(0, ".")
exec(open("fill_scan.py").read().split("t0, n0 = run(top)")[0])
from petri import World, OPS
def run3(g, cap):
    try:
        w = World(side=5, seed=7, copy_mut=0.0); w.inject(parse(g), "t", cell=0); o = w.cells[0]; n = 0; tasks = set()
        while n < cap:
            b = w.births; w.step(o, 0); n += 1; o = w.cells[0]
            if w.births > b:
                kid = next(x for c, x in enumerate(w.cells) if c != 0 and x is not None)
                return tuple(sorted(w.task_births)), n, len(kid.mem), kid.merit
    except Exception: pass
    return (), cap, 0, 0.0
T0, N0, L0, M0 = run3(top, CAP); F0 = M0 / N0; BIG = int(sys.argv[3]) if len(sys.argv) > 3 else 6300
print(json.dumps({"dominant_tasks": T0, "steps": N0, "child_len": L0, "merit": M0, "len": len(top)}), flush=True)
nf, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
for k in range(nf):
    g = list(top)
    for i in DEAD: g[i] = rng.choice(AL)
    g = "".join(g)
    if run3(g, CAP)[:3] != (T0, N0, L0): continue
    s = time.time(); seen = set(); r = {"fill": k, "div": 0, "long_child": 0, "max_child": 0, "gain": 0, "fitter": 0,
                                        "capped": 0, "div6300": 0, "long6300": 0, "gain6300": 0, "fitter6300": 0, "hits": []}
    for x in neigh(g):
        if x in seen: continue
        seen.add(x); t, n, L, m = run3(x, CAP); big = False
        if n >= CAP:
            r["capped"] += 1
            if BIG <= CAP: continue                         # true-merit rescoring of the CAP-1000 scan only
            t, n, L, m = run3(x, BIG); big = True
            if n >= BIG: continue
        p = "6300" if big else ""
        r["div" + p] += 1; r["max_child"] = max(r["max_child"], L)
        if L > len(x): r[("long" if big else "long_child") if not big else "long6300"] += 1
        if set(t) - set(T0):
            r["gain" + p] += 1
            if m / n > F0: r["fitter" + p] += 1; r["hits"].append({"g": x, "tasks": t, "steps": n, "child": L, "rel": round(m / n / F0, 3)})
    r["sec"] = round(time.time() - s, 1); print(json.dumps(r), flush=True)
