"""#491 frozen scoring rule: every (prediction, truth) pair maps to hit | miss | abstain | out-of-scope.

Truth classes (laps_truth.truth): exact j | exact-offlap n | rotated n | other-birth len | never | unresolved.
Static classes (static_lap.predict): exact j | exact-offlap n | rotated n | other-birth len | never | abstain.
Arith classes (static_lap.arith): ('exact', j, p, e) | ('never', p, e) | None.

Static:
  abstain                          -> abstain (counted, not scored)
  truth unresolved                 -> out-of-scope (counted)
  truth differs between seeds 7, 8 -> miss (a non-abstained prediction must be seed-independent)
  same class and same parameter    -> hit (j for exact, ncopy for exact-offlap and rotated, child length for
                                      other-birth; never = never)
  anything else                    -> miss
Arith (claims only the lap of an exact copy, and 'no birth' within the horizon):
  None                             -> abstain
  truth unresolved                 -> out-of-scope
  truth differs between seeds      -> miss
  exact j with j > 10 and truth never -> out-of-scope (the predicted birth lies beyond the 10-lap truth horizon)
  exact j                          -> hit iff truth is ('exact', j); any other resolved truth (exact at another lap,
                                      offlap, rotated, other-birth, never) is a miss
  never                            -> hit iff truth is never; any birth is a miss
"""

def score_static(pr, tr, tr2=None):
    if pr[0] == "abstain": return "abstain"
    if tr[0] == "unresolved": return "out-of-scope"
    if tr2 is not None and tr2 != tr: return "miss"
    if pr[0] == "never": return "hit" if tr[0] == "never" else "miss"
    return "hit" if (pr[0], pr[1]) == (tr[0], tr[1]) else "miss"

def score_arith(a, tr, tr2=None):
    if a is None: return "abstain"
    if tr[0] == "unresolved": return "out-of-scope"
    if tr2 is not None and tr2 != tr: return "miss"
    if a[0] == "exact" and a[1] > 10 and tr[0] == "never": return "out-of-scope"
    if a[0] == "never": return "hit" if tr[0] == "never" else "miss"
    return "hit" if tr == ("exact", a[1]) else "miss"

PRED_STATIC = [("exact", 1), ("exact", 3), ("exact-offlap", 7), ("rotated", 7), ("other-birth", 40), ("never", "x"),
               ("abstain", "x")]
PRED_ARITH = [("exact", 1, 3, 0), ("exact", 3, 3, 1), ("exact", 11, 13, 5), ("never", 4, 2), None]
TRUTH = [("exact", 1), ("exact", 3), ("exact-offlap", 7), ("rotated", 7), ("rotated", 8), ("other-birth", 40),
         ("other-birth", 41), ("never", "no birth"), ("unresolved", "step cap")]

def table():
    """The full contingency table over representative classes; printed into PREREG-laps.md."""
    rows = []
    for p in PRED_STATIC:
        rows.append(("static", p, [score_static(p, t) for t in TRUTH]))
    for a in PRED_ARITH:
        rows.append(("arith", a, [score_arith(a, t) for t in TRUTH]))
    return rows

if __name__ == "__main__":
    print("truth:", *TRUTH, sep=" | ")
    for kind, p, cells in table():
        print(kind, p, "->", " ".join(c[:4] for c in cells))
