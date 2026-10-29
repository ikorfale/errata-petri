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
ap.add_argument("--digest", default=None); ap.add_argument("--max-tests", type=int, default=3000000)
ap.add_argument("--edges", type=float, default=0.0, help="share of mutated births whose edge is tested")
ap.add_argument("--survival", default=None, help="write lineage lifetimes of origins and a matched baseline of mutated births here (JSON)")
ap.add_argument("--founders", default=None, help="write genome bytes of the origins at the last census and of their parents here (JSON)")
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
live_ids = {}
perf = {}                                  # census update -> [birth ids of TASK performers]
u0, t0 = w.update, time.time()
last = {}                                  # birth id -> last update seen alive (added 29.10 for --survival)
while w.update - u0 < a.updates:
    w.run_update()
    if a.survival:
        for o in w.cells:
            if o is not None: last[uid[id(o)]] = w.update
    if w.update % daily.SAMPLE == 0:
        _, lin_prev = daily.lineage_census(w, lin_prev)
        uid = {id(o): uid[id(o)] for o in w.cells if o is not None}   # dead organisms' ids are freed and may be reused
        if w.update > a.after:
            live_ids[w.update] = [uid[id(o)] for o in w.cells if o is not None]
            perf[w.update] = [uid[id(o)] for o in w.cells if o is not None and (a.task in o.tasks or a.task in getattr(o, "ptasks", ()))]
petri.Org = _Org
del w.divide
dig = hashlib.sha256(canon_s(w).encode()).hexdigest()
if a.digest and not dig.startswith(a.digest):
    sys.exit(f"replay ended on digest {dig[:16]}, expected {a.digest}: not the same day, results discarded")
sys.stderr.write(f"replayed {w.update - u0} updates, {len(parent)} ids, {time.time() - t0:.0f}s\n")

# The isolation test, fixed before day 2 (zenith 106694): the genome alone in a 5x5 world, no mutation, input seeds
# 1, 2, 3, at most STEPS instructions to its first division. "Capable" = TASK in the first gestation in at least 1 of
# the 3 seeds. It is a pure function of the genome bytes, so capability cannot switch on across an exact copy; the
# gain edges are still checked for a mutation and any without one is reported.
SEEDS, STEPS = (1, 2, 3), 20000
def first_div(g, seed):
    """Tasks of the first gestation of genome g alone, or None if it does not divide within STEPS."""
    v = World(side=5, seed=seed, copy_mut=0.0, indel=0.0); v.inject(list(g), "t", cell=0); o = v.cells[0]; snap = []
    _d = v.divide
    def d(o2, c): snap.append(set(o2.tasks)); _d(o2, c)
    v.divide = d
    for _ in range(STEPS):
        b = v.births; v.step(o, 0)
        if v.cells[0] is not o: return None
        if v.births > b: return snap[-1]
    return None
cap, nodiv, tests = {}, set(), [0]
def capable_g(g):
    if g not in cap:
        if tests[0] >= a.max_tests: raise RuntimeError("test budget spent")
        tests[0] += 1; r = [first_div(g, s) for s in SEEDS]
        cap[g] = any(a.task in (x or ()) for x in r)
        if all(x is None for x in r): nodiv.add(g)
    return cap[g]
def capable(i): return capable_g(genome[i])
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
rows, incap, incap_nodiv = [], 0, 0
for u, ids in sorted(perf.items()):
    per = Counter(); ps = set(ids)
    for i in ids:
        if not capable(i):                         # expressed TASK in the world, but its genome alone does not
            incap += 1; incap_nodiv += genome[i] in nodiv; continue
        per[find_origin(i)] += 1
    silent = sum(1 for i in live_ids[u] if i not in ps and capable(i))
    rows.append({"update": u, "performers": len(ids), "capable_not_performing": silent, "origins": {str(k): v for k, v in per.items()}})
allo = {o for r in rows for o in r["origins"]}
no_mut_gains = sum(1 for o in allo if not str(o).startswith("start") and parent[int(o)] >= 0 and genome[int(o)] is genome[parent[int(o)]])
start_cap = sum(1 for i, p in enumerate(parent) if p < 0 and capable(i))
# gain and loss edges over every mutated birth after --after (zenith 106694 point 3): parent capable -> child not = loss
gains = losses = sampled = 0
if a.edges:
    import random; rs = random.Random(20261029)   # a sample of mutated births: testing all of them takes hours
    for i, p in enumerate(parent):
        if p < 0 or birth_u[i] <= a.after or genome[i] is genome[p] or rs.random() >= a.edges: continue
        sampled += 1
        cp, ci = capable(p), capable(i); gains += ci and not cp; losses += cp and not ci
# Added 29.10 after the freeze, reporting only (glitchfox 107031): how many of the run-origins an "earliest ancestor
# whose genome computes TASK" rule would have folded into an older line, i.e. some ancestor above the gap is capable.
def folded(o):
    p = parent[int(o)]
    while p >= 0:
        if capable(p): return True
        p = parent[p]
    return False
n_folded = sum(1 for o in allo if not str(o).startswith("start") and folded(o))
print(json.dumps({"task": a.task, "origins_an_earliest_ancestor_rule_would_fold": n_folded, "after": a.after, "updates": [u0, w.update], "digest16": dig[:16], "ids": len(parent),
                  "test": {"seeds": SEEDS, "steps": STEPS, "capable": "task in first gestation in >= 1 of 3 seeds"},
                  "start_capable": start_cap, "gain_edges_without_mutation": no_mut_gains,
                  "edges": {"sample_share": a.edges, "mutated_births_tested": sampled, "gains": gains, "losses": losses} if a.edges else None,
                  "genome_tests": tests[0], "performers_not_capable_alone": incap,
                  "of_them_never_divide_alone": incap_nodiv, "origins_total": len(allo),
                  "origins_older_than_day": sum(1 for o in allo if str(o).startswith("start")),
                  "origin_born": {str(o): birth_u[int(o)] for o in allo if not str(o).startswith("start")},
                  "censuses": rows}, indent=1))
if a.founders:                             # added 29.10 (board 107280): the founder genome and its parent's, as opcode lists
    last = rows[-1]["origins"] if rows else {}
    json.dump({o: {"born": birth_u[int(o)], "performers_at_last_census": n, "genome": list(genome[int(o)]),
                   "parent": parent[int(o)], "parent_genome": list(genome[parent[int(o)]]) if parent[int(o)] >= 0 else None,
                   "parent_capable": capable(parent[int(o)]) if parent[int(o)] >= 0 else None}
               for o, n in last.items() if not str(o).startswith("start")}, open(a.founders, "w"), indent=1)

if a.survival:                             # added 29.10 (zenith 107333/107347): how long did each origin's line last?
    import numpy as np, random
    par = np.array(parent); order = np.argsort(par, kind="stable"); ps = par[order]
    def kids(i):
        lo, hi = np.searchsorted(ps, i), np.searchsorted(ps, i, side="right"); return order[lo:hi].tolist()
    def lifetime(i, only_capable=False):   # last update any descendant (incl. i) was alive, minus birth of i
        best, stack = last.get(i, birth_u[i]), [i]
        while stack:
            j = stack.pop(); best = max(best, last.get(j, birth_u[j]))
            if best >= E: break                # alive at the end of the day: no need to walk the rest
            stack.extend(k for k in kids(j) if not only_capable or capable(k))
        return best - birth_u[i]
    S = a.after; E = w.update
    def nextc(b): return (b // daily.SAMPLE + 1) * daily.SAMPLE
    org = {}
    for o in allo:
        if str(o).startswith("start"): continue
        o = int(o); org[o] = {"born": birth_u[o], "next_census": nextc(birth_u[o]), "life_any": lifetime(o), "life_capable_run": lifetime(o, True)}
    rs = random.Random(1029); base = []
    cand = [i for i in range(len(parent)) if parent[i] >= 0 and S < birth_u[i] <= E - 1000 and genome[i] is not genome[parent[i]]]
    for i in rs.sample(cand, min(20000, len(cand))):
        base.append((birth_u[i], lifetime(i)))
    json.dump({"origins": org, "baseline_mutated_births": base, "n_mutated_births_after": len(cand)}, open(a.survival, "w"))
