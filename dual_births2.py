"""PREDICT-dualbirths-1029.md, follow-up: the 11 in-world AND+ANDN dividers of seed 101 never compute AND+ANDN when their
genome at division is traced alone (out/dual_seeds_s101.txt, 0/1100). Replay seed 101 again and keep each organism's
genome at birth, so every dual division can be compared with what that organism was born as (self-overwrite during
copying vs input/state dependence). Usage: python3 dual_births2.py SEED UPDATES -> out/dual_births2_sSEED.json"""
import json, sys, time
sys.path.insert(0, ".")
import petri_fe04506 as P
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
s, ups = int(sys.argv[1]), int(sys.argv[2])
born_as, duals = {}, []
orig_carve, orig_divide = P.World.carve, P.World.divide
def carve(self, o):
    self._cut = orig_carve(self, o); return self._cut
def divide(self, o, c):
    pg = P.show(o.mem[:o.glen]); tk = set(o.tasks); b0 = self.births
    orig_divide(self, o, c)
    if self.births == b0: return
    if {"AND", "ANDN"} <= tk:
        b = born_as.get(id(o)); b = b[1] if b and b[0] == o.born else None
        duals.append({"update": self.update, "born": o.born, "at_division": pg, "at_birth": b, "tasks": sorted(tk)})
P.World.carve, P.World.divide = carve, divide
w = P.World(seed=s); t0 = time.time()
for c in range(w.n): w.inject(P.parse(TOP), "s2", cell=c)
for u in range(1, ups + 1):
    w.run_update()
    for o in w.cells:                      # newborns are not run in their birth update, so this is the genome at birth
        if o is not None and born_as.get(id(o), (None,))[0] != o.born:
            born_as[id(o)] = (o.born, P.show(o.mem[:o.glen]))
    if u % 1000 == 0: born_as = {id(o): born_as[id(o)] for o in w.cells if o is not None and id(o) in born_as}
    if u % 5000 == 0: print(u, w.births, w.task_births.get("AND", 0), len(duals), round(time.time() - t0), flush=True)
json.dump({"seed": s, "births": w.births, "and_births": w.task_births.get("AND", 0), "duals": duals}, open(f"out/dual_births2_s{s}.json", "w"))
print("done", w.births, len(duals))
