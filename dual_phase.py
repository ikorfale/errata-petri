"""Is the dual genome's 5x first gestation the copy-loop length phase (README #451: fast only at length = 2 mod 3)?
Insert 1 or 2 no-ops ('q') at every position of the 112-letter dual genome; for each variant: steps to first division alone
(no mutation, cap 3000) and whether that division earns AND and ANDN. Usage: python3 dual_phase.py -> out/dual_phase.txt"""
import json
from collections import Counter
from petri import parse
import fertility_probe as fp
D = fp.DUAL; g0 = parse(D); q = parse("q")[0]
out = []
for k in (1, 2):
    res = Counter(); best = None
    for i in range(len(g0) + 1):
        g = g0[:i] + [q] * k + g0[i:]; r = fp.first_div(g, 1, False)
        if r is None: res["never"] += 1; continue
        both = {"AND", "ANDN"} <= r[1]; fast = r[0] < 400
        res[("fast" if fast else "slow", "AND+ANDN" if both else "lost")] += 1
        if fast and both and (best is None or r[0] < best[1]): best = (i, r[0], sorted(r[1]))
    out.append(f"len {len(g0)+k} (mod3 {(len(g0)+k)%3}): {dict(res)}; fastest keeping both: {best}")
r = fp.first_div(g0, 1, False); out.insert(0, f"len {len(g0)} (mod3 {len(g0)%3}): steps {r[0]} tasks {sorted(r[1])}")
print("\n".join(out)); open("out/dual_phase.txt", "w").write("\n".join(out) + "\n")
