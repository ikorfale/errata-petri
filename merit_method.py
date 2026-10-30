"""Does merit = copied size (petri.py:326, like Avida's BASE_MERIT_METHOD 1) pay for unexecuted instructions?
Paired arms from the same saved world (end of day 1, update 40,000): method 1 (Petri's rule) vs method 4 (Avida's
default, min(executed, copied)), same reseeded RNG per pair. Not the long world: no digest, nothing written to daily/.
PREDICT-merit-method-1030.md holds the predictions, written before any arm ran.
Usage: python3 merit_method.py METHOD SEED UPDATES > out/mm_<method>_<seed>.json"""
import inspect, json, os, pickle, sys, time, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri
from petri import World, Org, IP

METHOD, SEED, U = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
SEEN = {}                                   # id(org) -> positions its IP visited this gestation
_step = World.step
def step(self, o, c):
    SEEN.setdefault(id(o), set()).add(o.heads[IP] % len(o.mem))
    return _step(self, o, c)
src = textwrap.dedent(inspect.getsource(World.divide))
old = "bonus = float(min(o.ncopy, len(child)))"
assert src.count(old) == 1 and src.count("kid = Org(") == 1 and src.count("self.restart(o, parent, bonus)") == 1
new = ("ex = sum(1 for p in SEEN.pop(id(o), ()) if p < len(parent)); LOG.append((len(parent), ex, o.ncopy))\n"
       "    bonus = float(min(o.ncopy, len(child)) if METHOD == 1 else min(ex, o.ncopy, len(child)))")
src = src.replace(old, new).replace("kid = Org(", "kid = Org(").replace(
    "self.cells[t] = kid", "SEEN.pop(id(kid), None)\n    self.cells[t] = kid")
assert "SEEN.pop(id(kid)" in src
ns = dict(vars(petri)); ns.update(SEEN=SEEN, METHOD=METHOD, LOG=None)
LOG = []; ns["LOG"] = LOG
exec(src, ns)
World.divide, World.step = ns["divide"], step

w = pickle.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily/base/day-001/world.pkl"), "rb"))
w.rng.seed(SEED)
rows, t0 = [], time.time()
def row():
    live = [o for o in w.cells if o is not None]
    gl = sorted(o.glen for o in live); b = LOG[:]; LOG.clear()
    unexec = [1 - ex / L for L, ex, _ in b] if b else []
    return {"update": w.update, "pop": len(live), "glen_med": gl[len(gl) // 2] if gl else None,
            "glen_mean": round(sum(gl) / len(gl), 2) if gl else None, "births": len(b),
            "unexec_mean": round(sum(unexec) / len(unexec), 4) if unexec else None}
LOG.clear(); rows.append(row())
while w.update - 40000 < U:
    w.run_update()
    if w.update % 1000 == 0:
        rows.append(row())
print(json.dumps({"method": METHOD, "seed": SEED, "updates": U, "secs": round(time.time() - t0), "rows": rows}))
