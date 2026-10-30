"""glitchfox's check (108218) of flip 2 (89 -> 90 at 68k-72k): does the 90s' 1-3% merit-per-step lead survive Avida's
default merit rule, min(executed, copied) (BASE_MERIT_METHOD 4), instead of Petri's copied size (method 1)?
Top 3 genotypes of 89 and of 90 at 68k, 70k and 72k, alone in a 5x5 world, no mutation, seeds 1-3 (same as
swaps_flip.py). "Executed" = distinct positions inside the parent genome the IP visits in the first gestation
(as in merit_method.py). Method-4 merit = method-1 merit * min(executed, copied) / min(copied, len) (tasks multiply the base)."""
import json, os, sys
from statistics import median
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import World, IP
C = {c["update"]: c for c in json.load(open("daily/replay-day-002-swaps.json"))["censuses"]}

def run(g, seed, steps=20000):
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]
    seen = set()
    for i in range(steps):
        b = v.births; seen.add(o.heads[IP] % len(o.mem)); nc = o.ncopy; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b:
            kid = next(x for x in v.cells if x is not None and x is not o)
            ex = sum(1 for p in seen if p < len(g)); base1 = min(nc, len(kid.mem))
            return i + 1, kid.merit, kid.merit * min(ex, base1) / base1, ex
    return None

for u in (68000, 70000, 72000):
    c = C[u]; L = c["lens"]; a, b = L.get("89", 0), L.get("90", 0)
    print(f"== {u}: f89 = {a / (a + b):.2f}")
    for l in ("89", "90"):
        for t in c["top"].get(l, []):
            r = [x for x in (run(bytes.fromhex(t["g"]), s) for s in (1, 2, 3)) if x]
            if not r: print(f"   len {l} {t['n']:>3} copies sterile alone"); continue
            st = median(x[0] for x in r); m1 = median(x[1] for x in r); m4 = median(x[2] for x in r); ex = median(x[3] for x in r)
            print(f"   len {l} {t['n']:>3} copies  steps {st:>5}  executed {ex:>3}  m1/s {m1 / st:>7.0f}  m4/s {m4 / st:>7.0f}")
