"""Verdict for PREDICT-lockin-1031.md. Usage: python3 lockin_verdict.py"""
import json
def lock(rows):
    for r in rows:
        L, n = max(r["len_hist"], key=lambda x: x[1])
        if n / r["pop"] >= 0.5: return r["update"], L
    return None, None
res = {}
for s in [12, 15, 17, 29, 13, 19, 20, 18]:
    d = json.load(open(f"out/shrink_carrier_{s}.json"))
    u, L = lock(d["rows"]); top = max(r["top"][0][1] / r["pop"] for r in d["rows"])
    res[s] = (u, d["mismatch_vs_mm1"] == [])
    print(f"seed {s}: lock {u} at length {L}, end median {d['rows'][-1]['glen_med']}, max top-genotype {top:.1%}, valid {res[s][1]}")
L1 = [s for s in (12, 15, 17, 29) if res[s][1] and not (res[s][0] is None or res[s][0] >= 50000)]
L2 = [s for s in (13, 19, 20) if res[s][1] and not (res[s][0] is not None and res[s][0] < 50000)]
print("L1 misses:", L1 or "none", "| L2 misses:", L2 or "none", "->", "PASS" if not L1 and not L2 else "FAIL")
