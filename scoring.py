"""#491 frozen scoring rule: every (prediction, truth) pair maps to hit | miss | abstain | out-of-scope | not-scored.
Revised after two blocking-only reviews (Fable, 24.10): arith split into a lap claim and a premise measurement; static
other-birth predictions are abstentions, reported with their truth; unresolved in either seed is out-of-scope.

Truth classes (laps_truth.truth): exact j | exact-offlap n | rotated n | other-birth len | never | unresolved.
Static classes (static_lap.predict): exact j | exact-offlap n | rotated n | other-birth len | never | abstain.
Arith classes (static_lap.arith): ('exact', j, p, e) | ('never', p, e) | None.

Common: truth unresolved under seed 7 or seed 8 -> out-of-scope.
Static (a non-abstained prediction must be seed-independent: truth differing between the seeds -> miss):
  abstain, other-birth -> abstain (counted, not scored). other-birth is reported with its truth, child-length match and
                 seed stability: in-sample 7 other-birth predictions, 2 seed-stable with matching length, 5 with
                 truth differing between seeds (decided on development data, before any test truth)
  same class and same parameter -> hit (j for exact, ncopy for exact-offlap and rotated; never = never)
  anything else -> miss
Arith lap claim (the arithmetic): scored on the seeds whose truth is an exact copy at a lap.
  None -> abstain; no exact copy under either seed -> not-scored; otherwise hit iff arith is exact j and every seed
  with an exact copy has that j; arith never against any exact copy -> miss. What the other seed did goes to the
  premise, not to the lap claim.
Arith premise ("a non-abstained arith meets, under both seeds, an exact copy at a lap or no birth"): a measurement,
  not a hypothesis; holds iff both seeds give exact or never; failures broken down by (arith class, truth classes).
  Arith never vs truth never is a within-horizon (10 laps) confirmation only.
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
    trs = [t for t in (tr, tr2) if t is not None]
    if any(t[0] == "unresolved" for t in trs): return "out-of-scope"
    ex = [t for t in trs if t[0] == "exact"]
    if not ex: return "not-scored"
    return "hit" if a[0] == "exact" and all(t[1] == a[1] for t in ex) else "miss"

def arith_premise(a, tr, tr2=None):
    """True / False for non-abstained arith with resolved truth under both seeds, else None."""
    trs = [t for t in (tr, tr2) if t is not None]
    if a is None or any(t[0] == "unresolved" for t in trs): return None
    return all(t[0] in ("exact", "never") for t in trs)

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
