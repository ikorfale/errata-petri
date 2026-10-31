"""Scorer for addendum A1 of PREDICT-lockin-1031.md. Usage: python3 lockfwd_verdict.py a (lock status at 50k only,
prints the rule's predictions) | b (scores them against end medians at 80,000)."""
import json, sys
from math import comb
SEEDS = list(range(33, 49))   # A2: 16 seeds
def lock(rows):
    for r in rows:
        L, n = max(r["len_hist"], key=lambda x: (x[1], x[0]))
        if n / r["pop"] >= 0.5: return r["update"], L
    return None, None
hits = misses = 0; tab = {(a, e): 0 for a in "LS" for e in "LS"}
for s in SEEDS:
    a = json.load(open(f"out/lockfwd_{s}_a.json"))["rows"]
    u, L = lock(a)
    pred = "long (>=95)" if (u is not None and L >= 95) else "short (<=94)" if u is None else "short (<=94, locked short)"
    line = f"seed {s}: lock by 50k {u} at length {L}, median at 50k {a[-1]['glen_med']} -> predicted end {pred}"
    if sys.argv[1] == "b":
        end = json.load(open(f"out/lockfwd_{s}_b.json"))["rows"][-1]["glen_med"]
        ok = (end >= 95) == pred.startswith("long"); hits += ok; misses += not ok
        tab[("L" if pred.startswith("long") else "S", "L" if end >= 95 else "S")] += 1
        line += f" | end median {end} {'HIT' if ok else 'MISS'}"
    print(line)
if sys.argv[1] == "b":
    a, b, c, d = tab["S", "S"], tab["S", "L"], tab["L", "S"], tab["L", "L"]   # rows: predicted short / long
    n, r1, k = a + b + c + d, a + b, a + c
    p = sum(comb(k, x) * comb(n - k, r1 - x) for x in range(a, min(k, r1) + 1)) / comb(n, r1)   # Fisher, one-sided
    print(f"hits {hits} of {n}; short arm {a}/{r1} end short, long arm {d}/{c + d} end long; always-long baseline {b + d} of {n}")
    print(f"Fisher one-sided p = {p:.4f} ->", "NO CONTRAST (short arm < 3)" if r1 < 3 else "PASS" if p < 0.05 else "FAIL")
