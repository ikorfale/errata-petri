"""zenith-claude 107785: pre-check for "the 58 dual genotypes are overwritten before their first division".
Replay seed 101 (as dual_births.py, petri.py fe04506, TOP of s2_dump, 40000 updates) and follow every organism born with
one of the 58 dual genotypes of out/dual_births_trace_other.json: birth update, death update, cause (old age: age over
20 x max(glen,10); otherwise overwritten by a neighbour's child), instructions executed (o.age) at death, divisions in
the world. Compare age at death with each genotype's isolation division step (genome_trace, cap 2000).
Usage: python3 dual_deaths.py SEED UPDATES -> out/dual_deaths_sSEED.json. Written 29.10 15:47 UTC (date -u)."""
import json, sys, time
sys.path.insert(0, ".")
import petri_fe04506 as P
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
H = json.load(open("out/dual_births_trace_other.json"))["hits"]; STEP = {h["genome"]: h["steps"] for h in H}
s, ups = int(sys.argv[1]), int(sys.argv[2])
_Org = P.Org; last = [None]
def Org(*a, **k):
    o = _Org(*a, **k); last[0] = o; return o
P.Org = Org
alive, dead, divs = {}, [], {}
orig_carve, orig_divide = P.World.carve, P.World.divide
def carve(self, o):
    self._cut = orig_carve(self, o); return self._cut
def divide(self, o, c):
    b0 = self.births; orig_divide(self, o, c)
    if self.births == b0: return
    if id(o) in alive: divs[id(o)] = divs.get(id(o), 0) + 1
    g = P.show(self._cut[0])
    if g in STEP:
        kid = last[0]; cell = next(i for i, x in enumerate(self.cells) if x is kid)
        alive[id(kid)] = (kid, cell, g, self.update)
P.World.carve, P.World.divide = carve, divide
w = P.World(seed=s); t0 = time.time()
for c in range(w.n): w.inject(P.parse(TOP), "s2", cell=c)
for u in range(1, ups + 1):
    w.run_update()
    for k in [k for k, (o, cell, g, b) in alive.items() if w.cells[cell] is not o]:
        o, cell, g, b = alive.pop(k)
        dead.append({"genome": g, "born": b, "died": u, "age": o.age, "glen": o.glen,
                     "cause": "age" if o.age > 20 * max(o.glen, 10) else "overwritten",
                     "divisions": divs.pop(k, 0), "iso_step": STEP[g]})
    if u % 5000 == 0: print(u, len(dead), len(alive), round(time.time() - t0), flush=True)
out = {"seed": s, "updates": ups, "dead": dead,
       "alive_at_end": [{"genome": g, "born": b, "age": o.age, "divisions": divs.get(k, 0), "iso_step": STEP[g]}
                        for k, (o, cell, g, b) in alive.items()], "sec": round(time.time() - t0)}
json.dump(out, open(f"out/dual_deaths_s{s}.json", "w"))
print("done", len(dead), len(out["alive_at_end"]), out["sec"])
