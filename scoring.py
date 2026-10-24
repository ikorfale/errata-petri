"""#491 frozen scoring rule: every (prediction, truth) pair maps to hit | miss | abstain | out-of-scope | not-scored.
Revised after a blocking-only review (Fable, 24.10): arith split into a lap claim and a premise measurement; static
other-birth scored on class only, length reported separately; unresolved in either seed is out-of-scope.

Truth classes (laps_truth.truth): exact j | exact-offlap n | rotated n | other-birth len | never | unresolved.
Static classes (static_lap.predict): exact j | exact-offlap n | rotated n | other-birth len | never | abstain.
Arith classes (static_lap.arith): ('exact', j, p, e) | ('never', p, e) | None.

Common: truth unresolved under seed 7 or seed 8 -> out-of-scope. A non-abstained prediction whose resolved truth
differs between the two seeds -> miss.
Static:
  abstain -> abstain (counted, not scored)
  same class and same parameter -> hit (j for exact, ncopy for exact-offlap and rotated; never = never)
  other-birth -> abstain, reported with its truth: in-sample 3 of the 5 seed-resolved other-birth predictions were
                 seed-dependent (a non-abstaining predictor must be seed-independent), and the child length matched in
                 2 of 5; the class is treated as an abstention rather than scored (decided on development data)
  anything else -> miss
Arith lap claim (the arithmetic): scored only when truth is an exact copy at a lap, ('exact', j).
  None -> abstain; no exact copy under either seed -> not-scored (goes to the premise); exact under one seed only
  -> miss; exact j -> hit iff j matches; never -> miss
Arith premise ("when arith does not abstain, the first birth is an exact copy at a lap, or there is none"):
  a measurement, not a hypothesis: for each non-abstained arith, holds iff truth is ('exact', j') or never; the
  failures are broken down by (arith class, truth class). Arith never vs truth never is a within-horizon (10 laps)
  confirmation only.
"""

def _common(pred_abstains, tr, tr2):
    if pred_abstains: return "abstain"
    if tr[0] == "unresolved" or (tr2 is not None and tr2[0] == "unresolved"): return "out-of-scope"
    if tr2 is not None and tr2 != tr: return "miss"
    return None

def score_static(pr, tr, tr2=None):
    c = _common(pr[0] in ("abstain", "other-birth"), tr, tr2)
    if c: return c
    if pr[0] == "never": return "hit" if tr[0] == "never" else "miss"
    return "hit" if (pr[0], pr[1]) == (tr[0], tr[1]) else "miss"

def static_len(pr, tr):
    """For other-birth predictions: does the predicted child length match the seed-7 truth? (reported only)"""
    return pr[1] == tr[1] if pr[0] == tr[0] == "other-birth" else None

def score_arith(a, tr, tr2=None):
    """Lap claim."""
    if a is None: return "abstain"
    if tr[0] == "unresolved" or (tr2 is not None and tr2[0] == "unresolved"): return "out-of-scope"
    if tr[0] != "exact" and (tr2 is None or tr2[0] != "exact"): return "not-scored"   # no exact copy under either seed
    if tr2 is not None and tr2 != tr: return "miss"
    return "hit" if a[0] == "exact" and a[1] == tr[1] else "miss"

def arith_premise(a, tr, tr2=None):
    """True / False for non-abstained arith with in-scope seed-stable truth, else None."""
    if a is None or tr[0] == "unresolved" or (tr2 is not None and (tr2[0] == "unresolved" or tr2 != tr)): return None
    return tr[0] in ("exact", "never")

PRED_STATIC = [("exact", 1), ("exact", 3), ("exact-offlap", 7), ("rotated", 7), ("other-birth", 40), ("never", "x"),
               ("abstain", "x")]
PRED_ARITH = [("exact", 1, 3, 0), ("exact", 3, 3, 1), ("exact", 11, 13, 5), ("never", 4, 2), None]
TRUTH = [("exact", 1), ("exact", 3), ("exact-offlap", 7), ("rotated", 7), ("rotated", 8), ("other-birth", 40),
         ("other-birth", 41), ("never", "no birth"), ("unresolved", "step cap")]

def table():
    """The full contingency table over representative classes (seed-stable truth); printed into PREREG-laps.md."""
    rows = []
    for p in PRED_STATIC:
        rows.append(("static", p, [score_static(p, t) for t in TRUTH]))
    for a in PRED_ARITH:
        rows.append(("arith-lap", a, [score_arith(a, t) for t in TRUTH]))
    return rows

if __name__ == "__main__":
    print("truth:", *TRUTH, sep=" | ")
    for kind, p, cells in table():
        print(kind, p, "->", " ".join(c[:4] for c in cells))
