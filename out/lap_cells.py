"""#488 step 5, asked by glitchfox #101146 and zenith #101128/#101149: the census of exact copies tabulated by cell
(L mod 3, e mod 3), e = ncopy at the first if-label check; the misses one row each (L, e, gaps, j); and glitchfox's
structural check j1 - j5 == #(L=0, e=0). Same runner and filters as odd_lap_census.py (copied, not imported)."""
import sys, json, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse, OPS, RH, WH
def run(g, cap=3000):
    w = World(side=5, seed=7, copy_mut=0.0); w.indel = 0.0; w.inject(parse(g), "t", cell=0); o = w.cells[0]
    checks, divs = [], []
    for n in range(cap):
        ip = o.heads[0] % len(o.mem); op = OPS[o.mem[ip]]
        if op == "if-label": checks.append((ip, o.ncopy))
        if op == "h-divide": divs.append((n, o.ncopy, o.heads[RH], o.heads[WH], len(o.mem)))
        b = w.births; w.step(o, 0); o = w.cells[0]
        if w.births > b: return n + 1, checks, divs, True
    return cap, checks, divs, False
R = json.load(open("out/two_step_filter.json"))
cell = collections.defaultdict(collections.Counter); miss = []; L3 = collections.Counter()
for r in R:
    g = r["genome"]; L = len(g)
    n, ch, dv, born = run(g)
    if not born: continue
    d = dv[-1]; rh = d[2] or d[4]; wh = d[3] or d[4]
    if wh - rh != L or d[1] % L: continue
    j = d[1] // L; e = ch[0][1] % 3 if ch else None
    pred = next((k for k in (1, 3, 5) if e is not None and (k * L - e) % 3 == 0), None)
    cell[(L % 3, e)][j] += 1; L3[L % 3] += 1
    if pred != j:
        gaps = collections.Counter(y[1] - x[1] for x, y in zip(ch, ch[1:]))
        miss.append((L, ch[0][1] if ch else None, e, j, pred, dict(gaps.most_common(3)), len(ch)))
print("cell (L%3, e%3): counts by laps j      rule predicts")
rule = lambda Lm, e: next((k for k in (1, 3, 5) if (k * Lm - e) % 3 == 0), "never")
tot = collections.Counter()
for k in sorted(cell, key=str):
    print(f"  {k}: {dict(sorted(cell[k].items()))}   rule j={rule(*k) if k[1] is not None else '?'}"); tot.update(cell[k])
print("total by j:", dict(sorted(tot.items())), " sum", sum(tot.values()))
print("dividers by L%3:", dict(sorted(L3.items())))
n00 = sum(cell[(0, 0)].values()); print(f"glitchfox check: j1 - j5 = {tot[1]} - {tot[5]} = {tot[1] - tot[5]};  #(0,0) = {n00}")
print("misses: L, ncopy at first check, e%3, j, rule j, top gaps between checks, number of checks")
for m in miss: print("  ", m)
