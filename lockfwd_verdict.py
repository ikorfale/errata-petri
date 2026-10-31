"""Scorer for addendum A1 of PREDICT-lockin-1031.md. Usage: python3 lockfwd_verdict.py a (lock status at 50k only,
prints the rule's predictions) | b (scores them against end medians at 80,000)."""
import json, sys
SEEDS = [33, 34, 35, 36, 37, 38, 39, 40]
def lock(rows):
    for r in rows:
        L, n = max(r["len_hist"], key=lambda x: (x[1], x[0]))
        if n / r["pop"] >= 0.5: return r["update"], L
    return None, None
hits = misses = 0
for s in SEEDS:
    a = json.load(open(f"out/lockfwd_{s}_a.json"))["rows"]
    u, L = lock(a)
    pred = "long (>=95)" if (u is not None and L >= 95) else "short (<=94)" if u is None else "short (<=94, locked short)"
    line = f"seed {s}: lock by 50k {u} at length {L}, median at 50k {a[-1]['glen_med']} -> predicted end {pred}"
    if sys.argv[1] == "b":
        end = json.load(open(f"out/lockfwd_{s}_b.json"))["rows"][-1]["glen_med"]
        ok = (end >= 95) == pred.startswith("long"); hits += ok; misses += not ok
        line += f" | end median {end} {'HIT' if ok else 'MISS'}"
    print(line)
if sys.argv[1] == "b": print(f"hits {hits} of {hits + misses}")
