"""Exact origins of a task in one day of the long world (plan #553; glitchfox 106647, zenith 106650). Census ancestry
cannot count origins: a silenced allele opens several clades, and on this engine random pairs of organisms share an
ancestor within 4 censuses 14-28% of the time, so any merge by shared ancestor also merges unrelated re-inventions.

This replays one day from the previous day's saved world (the world is deterministic; the replay runs the same lineage
censuses as daily.py and must end on the same digest, or it stops). Every birth gets an id and its parent's id; the
genome is kept per birth (shared with the parent when the copy was exact). At the end, for every performer of TASK at a
census after --after, it walks up the line and tests each ancestor's genome alone (a 5x5 world, no mutation, two input
seeds): can it compute TASK in its first gestation? The origin of a performer is the oldest ancestor of the unbroken
run of capable genomes that ends at it; a run that reaches the start of the day is "older than the day". Whether the
task was expressed in between does not matter, which is the point.
Usage: python3 replay_origins.py BASE_DIR UPDATES [--task OR] [--after 41500] [--digest HEX] > out.json"""
import argparse, json, os, pickle, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri, daily
from petri import World
from world_digest import canon_s
import hashlib

ap = argparse.ArgumentParser(); ap.add_argument("base"); ap.add_argument("updates", type=int)
ap.add_argument("--task", default="OR"); ap.add_argument("--after", type=int, default=41500)
ap.add_argument("--digest", default=None); ap.add_argument("--max-tests", type=int, default=60000)
a = ap.parse_args()
w = pickle.load(open(os.path.join(a.base, "world.pkl"), "rb")); st = json.load(open(os.path.join(a.base, "state.json")))
assert hashlib.sha256(canon_s(w).encode()).hexdigest() == st["digest"], "base world does not match its state digest"

parent, genome, birth_u = [], [], []          # per birth id
uid = {}                                   # id(org) -> birth id, for live organisms
for o in w.cells:
    if o is not None:
        uid[id(o)] = len(parent); parent.append(-1); genome.append(bytes(o.mem[:o.glen])); birth_u.append(w.update)
cur_parent = [None]
_Org = petri.Org
class TOrg(_Org):                          # records each new organism; adds no state, draws no random numbers
    __slots__ = ()
    def __init__(self, g, lineage, merit=1.0, born=0):
        _Org.__init__(self, g, lineage, merit, born)
        p = cur_parent[0]; pid = uid.get(id(p), -1) if p is not None else -1; gb = bytes(g)
        uid[id(self)] = len(parent); parent.append(pid); birth_u.append(w.update)
        genome.append(genome[pid] if pid >= 0 and genome[pid] == gb else gb)
TOrg.__name__ = TOrg.__qualname__ = "Org"   # the digest names each object's class
petri.Org = TOrg
_div = w.divide
def div(o, c):
    cur_parent[0] = o
    try: _div(o, c)
    finally: cur_parent[0] = None
w.divide = div

if "lin_prev" in st:
    lin_prev = {md: {k: {int(c): v for c, v in m.items()} for k, m in st.get("lin_prev" + md, {}).items()} for md in daily.MODES}
    lin_prev["_gen"] = [(u, {int(c): x for c, x in m.items()}) for u, m in st.get("lin_gen", [])]
    lin_prev["_deepf"] = st.get("lin_deepf", {})
else: _, lin_prev = daily.lineage_census(w, {})
perf = {}                                  # census update -> [birth ids of TASK performers]
u0, t0 = w.update, time.time()
while w.update - u0 < a.updates:
    w.run_update()
    if w.update % daily.SAMPLE == 0:
        _, lin_prev = daily.lineage_census(w, lin_prev)
        uid = {id(o): uid[id(o)] for o in w.cells if o is not None}   # dead organisms' ids are freed and may be reused
        if w.update > a.after:
            perf[w.update] = [uid[id(o)] for o in w.cells if o is not None and (a.task in o.tasks or a.task in getattr(o, "ptasks", ()))]
petri.Org = _Org
del w.divide
dig = hashlib.sha256(canon_s(w).encode()).hexdigest()
if a.digest and not dig.startswith(a.digest):
    sys.exit(f"replay ended on digest {dig[:16]}, expected {a.digest}: not the same day, results discarded")
sys.stderr.write(f"replayed {w.update - u0} updates, {len(parent)} ids, {time.time() - t0:.0f}s\n")

def first_div(g, seed):
    """The genome alone in a 5x5 world without mutation: tasks of its first gestation (as fertility_probe.first_div)."""
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]; snap = []
    _d = v.divide
    def d(o2, c): snap.append(set(o2.tasks)); _d(o2, c)
    v.divide = d
    for _ in range(3000):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b: return snap[-1]
    return None
cap, tests = {}, [0]
def capable(i):
    g = genome[i]
    if g not in cap:
        if tests[0] >= a.max_tests: raise RuntimeError("test budget spent")
        tests[0] += 1
        cap[g] = any(a.task in (first_div(g, s) or ()) for s in (1, 2))
    return cap[g]
origin = {}
def find_origin(i):
    path = []
    while i not in origin:
        path.append(i)
        p = parent[i]
        if p < 0 or not capable(p):
            origin[i] = ("start:%d" % i) if p < 0 else i; break
        i = p
    o = origin[i]
    for j in path: origin[j] = o
    return o
rows, incap = [], 0
for u, ids in sorted(perf.items()):
    per = Counter()
    for i in ids:
        if not capable(i): incap += 1; continue    # expressed TASK but its genome alone cannot: input luck, counted apart
        per[find_origin(i)] += 1
    rows.append({"update": u, "performers": len(ids), "origins": {str(k): v for k, v in per.items()}})
allo = {o for r in rows for o in r["origins"]}
print(json.dumps({"task": a.task, "after": a.after, "updates": [u0, w.update], "digest16": dig[:16], "ids": len(parent),
                  "genome_tests": tests[0], "performers_not_capable_alone": incap, "origins_total": len(allo),
                  "origins_older_than_day": sum(1 for o in allo if str(o).startswith("start")),
                  "origin_born": {str(o): birth_u[int(o)] for o in allo if not str(o).startswith("start")},
                  "censuses": rows}, indent=1))
