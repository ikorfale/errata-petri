"""#488 step 4: test the odd-lap rule on every genome of the two-step search (two_step_filter.json, 1576 records).
For each genome that divides within 3000 solo steps: child length == genome length? If so, ncopy/L = j, e = ncopy at the
first if-label check mod 3, rule prediction = smallest odd j in {1,3,5} with j*L = e (mod 3). Count by j and by agreement."""
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
c = collections.Counter(); bad = []
for r in R:
    g = r["genome"]; L = len(g)
    n, ch, dv, born = run(g)
    if not born: c["no birth in 3000"] += 1; continue
    d = dv[-1]; rh = d[2] or d[4]; wh = d[3] or d[4]
    if wh - rh != L: c["birth, child not genome length"] += 1; continue
    if d[1] % L: c["exact length, ncopy not a multiple of L"] += 1; bad.append((g, d[1], L)); continue
    j = d[1] // L
    e = ch[0][1] % 3 if ch else None
    pred = next((k for k in (1, 3, 5) if e is not None and (k * L - e) % 3 == 0), None)
    c[f"exact, j={j}, rule {'agrees' if pred == j else 'DISAGREES'}"] += 1
    if pred != j: bad.append((g, j, L, e, pred))
for k, v in sorted(c.items()): print(k, v)
print("disagreements (first 10):", bad[:10])
print("\nthe disagreements, with the check period p (most common ncopy step between if-label checks):")
for b in bad:
    if len(b) == 5:
        n, ch, dv, born = run(b[0])
        gaps = collections.Counter(y[1] - x[1] for x, y in zip(ch, ch[1:]))
        p = gaps.most_common(1)[0][0]
        print(f"L {b[2]} j {b[1]} e(mod 3) {b[3]} period {p} gaps {dict(gaps)} -> odd-j rule mod p predicts "
              f"{next((k for k in (1,3,5) if (k*b[2] - ch[0][1]) % p == 0), None) if p else None}")
