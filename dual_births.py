"""PREDICT-dualbirths-1029.md: replay one evo_and seed under petri.py fe04506 and log dual (AND+ANDN) divisions and every
distinct mutated child genome. Usage: python3 dual_births.py SEED UPDATES -> out/dual_births_sSEED.json.gz"""
import json, sys, gzip, time
from collections import Counter
sys.path.insert(0, ".")
import petri_fe04506 as P
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
s, ups = int(sys.argv[1]), int(sys.argv[2])
kids_and, kids_other, duals, nd = Counter(), Counter(), [], Counter()
orig_carve, orig_divide = P.World.carve, P.World.divide
def carve(self, o):
    self._cut = orig_carve(self, o); return self._cut
def divide(self, o, c):
    pg = P.show(o.mem[:o.glen]); tk = set(o.tasks); b0 = self.births
    orig_divide(self, o, c)
    if self.births == b0: return
    child = P.show(self._cut[0])
    if {"AND", "ANDN"} <= tk:
        k = (id(o), o.born, pg); nd[k] += 1     # Org has __slots__; key on identity + birth update + genome
        duals.append({"update": self.update, "genome": pg, "div_no": nd[k], "born": o.born, "tasks": sorted(tk)})
    if child != pg:
        (kids_and if "AND" in tk else kids_other)[child] += 1
P.World.carve, P.World.divide = carve, divide
w = P.World(seed=s); t0 = time.time()
for c in range(w.n): w.inject(P.parse(TOP), "s2", cell=c)
for u in range(1, ups + 1):
    w.run_update()
    if u % 5000 == 0: print(u, w.births, w.task_births.get("AND", 0), len(duals), len(kids_and), len(kids_other), round(time.time() - t0), flush=True)
out = {"seed": s, "updates": ups, "births": w.births, "and_births": w.task_births.get("AND", 0), "duals": duals,
       "kids_and": kids_and.most_common(), "kids_other": kids_other.most_common(), "sec": round(time.time() - t0)}
json.dump(out, gzip.open(f"out/dual_births_s{s}.json.gz", "wt"))
print("done", out["births"], out["and_births"], len(duals), out["sec"])
