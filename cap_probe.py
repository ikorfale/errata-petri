"""#481 Fable 25.10: CAP=1000 censors fitter gainers of OR/NOR/XOR/EQU. Re-run every one-step mutant of NF neutral fills
that hit CAP=1000 with CAP=6300 (EQU breakeven 6208) and count fitter task-gainers among them. Usage: cap_probe.py NF SEED"""
import sys, json, random, time
sys.path.insert(0, ".")
exec(open("fill_scan.py").read().split("t0, n0 = run(top)")[0])
from genome_trace import trace
from petri import parse
def run2(g, cap, seed=7):
    try: log, n = trace(parse(g), seed, 1, cap=cap)
    except Exception: return (), cap
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
t0, n0 = run(top); F0 = fit(top, t0, n0); BIG = 6300
nf, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
for k in range(nf):
    g = list(top)
    for i in DEAD: g[i] = rng.choice(AL)
    g = "".join(g); t, n = run(g)
    if not (t == t0 and n == n0): continue
    s = time.time(); seen = set(); capped = done = gain = fitter = 0; hits = []
    for x in neigh(g):
        if x in seen: continue
        seen.add(x); tx, nx = run(x)
        if nx < CAP: continue
        capped += 1; ty, ny = run2(x, BIG)
        if ny < BIG:
            done += 1
            if set(ty) - set(t0):
                gain += 1; f = len(x) * 2 ** sum(BON[z] for z in ty) / ny / F0
                if f > 1: fitter += 1; hits.append({"g": x, "tasks": ty, "steps": ny, "relfit": round(f, 3)})
    print(json.dumps({"fill": k, "capped": capped, "divide_by_6300": done, "gain": gain, "fitter": fitter,
                      "hits": hits, "sec": round(time.time() - s, 1)}), flush=True)
