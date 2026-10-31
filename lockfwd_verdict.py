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
A4_EXCL = [37, 41, 43, 45]   # A4: long-arm seeds locked at 95-98 in stage a
rows4 = []
hits = misses = 0; tab = {(a, e): 0 for a in "LS" for e in "LS"}
for s in SEEDS:
    a = json.load(open(f"out/lockfwd_{s}_a.json"))["rows"]
    u, L = lock(a)
    pred = "long (>=95)" if (u is not None and L >= 95) else "short (<=94)" if u is None else "short (<=94, locked short)"
    dist = f", distance from 95 at lock {L - 95:+d}" if u is not None else ""   # A3, report-only
    line = f"seed {s}: lock by 50k {u} at length {L}{dist}, median at 50k {a[-1]['glen_med']} -> predicted end {pred}"
    if sys.argv[1] == "b":
        end = json.load(open(f"out/lockfwd_{s}_b.json"))["rows"][-1]["glen_med"]
        ok = (end >= 95) == pred.startswith("long"); hits += ok; misses += not ok
        tab[("L" if pred.startswith("long") else "S", "L" if end >= 95 else "S")] += 1
        if s not in A4_EXCL: rows4.append((s, "L" if pred.startswith("long") else "S", "L" if end >= 95 else "S"))
        line += f" | end median {end} {'HIT' if ok else 'MISS'}"
    print(line)
if sys.argv[1] == "b":
    a, b, c, d = tab["S", "S"], tab["S", "L"], tab["L", "S"], tab["L", "L"]   # rows: predicted short / long
    n, r1, k = a + b + c + d, a + b, a + c
    p = sum(comb(k, x) * comb(n - k, r1 - x) for x in range(a, min(k, r1) + 1)) / comb(n, r1)   # Fisher, one-sided
    print(f"hits {hits} of {n}; short arm {a}/{r1} end short, long arm {d}/{c + d} end long; always-long baseline {b + d} of {n}")
    h = lambda x: comb(k, x) * comb(n - k, r1 - x) / comb(n, r1)
    midp = p - 0.5 * h(a)   # A3: Lancaster mid-p, report-only, does not decide the verdict
    print(f"Lancaster mid-p (report-only) = {midp:.4f}")
    print(f"Fisher one-sided p = {p:.4f} ->", "NO CONTRAST (short arm < 3)" if r1 < 3 else "PASS" if p < 0.05 else "FAIL (not detected at this n)")
    # A4 (report-only, glitchfox #109550): same table without long-arm seeds locked at 95-98, fixed from stage a
    t2 = {k_: 0 for k_ in tab}
    for (s_, pr, en) in rows4: t2[pr, en] += 1
    a, b, c, d = t2["S", "S"], t2["S", "L"], t2["L", "S"], t2["L", "L"]
    n, r1, k = a + b + c + d, a + b, a + c
    p = sum(comb(k, x) * comb(n - k, r1 - x) for x in range(a, min(k, r1) + 1)) / comb(n, r1)
    print(f"A4 report-only, excluding seeds {A4_EXCL}: n {n}; short arm {a}/{r1} end short, long arm {d}/{c + d} end long;"
          f" Fisher one-sided p = {p:.4f} ->", "PASS" if p < 0.05 else "FAIL (not detected at this n)")
