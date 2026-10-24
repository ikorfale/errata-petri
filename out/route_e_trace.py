"""#488 step 3 (glitchfox 100934/100948, zenith 100943): for the three site-84 probe routes R1-R3 at k = 0..5, read e
directly instead of fitting it. Per gestation: if-label checks (ip, ncopy), the ncopy step between checks, ncopy at the
first check (e), every h-divide attempt (ncopy, rh, wh, memory length, carved or not), and the copied span wh-rh at the
divide that succeeds. Deterministic: copy_mut 0, indel 0, seed 7, solo world (same as phase_good.py / phase_checks.py)."""
import sys, collections
sys.path.insert(0, "."); sys.path.insert(0, "out")
from petri import World, parse, OPS, RH, WH
from two_step_check import edit, top, blk
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
routes = [("R1", 39, "sub 21 h", "ins 31 z", 85), ("R3", 39, "sub 21 h", "ins 10 n", 85), ("R2", 47, "sub 28 c", "sub 45 f", 84)]
print("parent", "L", len(top))
for name, p, e1, e2, site in routes:
    g = edit(edit(top[:p] + blk + top[p + 12:], e1), e2)
    for k in range(6):
        x = g[:site] + "q" * k + g[site:]
        n, ch, dv, born = run(x)
        gaps = collections.Counter(b[1] - a[1] for a, b in zip(ch, ch[1:]))
        ips = sorted({i for i, _ in ch})
        e0 = ch[0][1] if ch else None
        print(f"{name} k{k} L{len(x)} mod3 {len(x)%3} steps {n if born else 'never(<'+str(n)+')'} checks {len(ch)} "
              f"ips {ips} ncopy@1st {e0} gaps {dict(gaps)} ncopy@last {ch[-1][1] if ch else None}")
        for d in dv[:4]:
            print(f"    divide@{d[0]} ncopy {d[1]} rh {d[2]} wh {d[3]} mem {d[4]} span {(d[3] or d[4]) - (d[2] or d[4])}")
        if len(dv) > 4: print(f"    ... {len(dv)} divide attempts in total")
print("\nsuccessful divide: child length vs genome length (the cell after birth holds the parent; the child is the newest org)")
for name, p, e1, e2, site in routes:
    g = edit(edit(top[:p] + blk + top[p + 12:], e1), e2)
    for k in range(6):
        x = g[:site] + "q" * k + g[site:]
        n, ch, dv, born = run(x)
        if born:
            d = dv[-1]; rh = d[2] or d[4]; wh = d[3] or d[4]
            print(f"{name} k{k} L{len(x)} last divide ncopy {d[1]} child {wh-rh} {'EXACT LENGTH' if wh-rh == len(x) else 'TRUNCATED/OTHER'}")
print("\nparent mirror: k no-op 'q' at site 84 of the parent (the series behind 'slow' 847/875 in 100923)")
for k in range(7):
    x = top[:84] + "q" * k + top[84:]
    n, ch, dv, born = run(x)
    d = dv[-1] if dv else None
    span = ((d[3] or d[4]) - (d[2] or d[4])) if d else None
    print(f"parent k{k} L{len(x)} mod3 {len(x)%3} steps {n if born else 'never'} ncopy@1st {ch[0][1] if ch else None} "
          f"checks {len(ch)} last-divide ncopy {d[1] if d else None} child {span if born else '-'} {'EXACT' if born and span == len(x) else ''}")
