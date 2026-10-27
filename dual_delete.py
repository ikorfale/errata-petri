"""zenith 105575: delete one letter at every position of the 112-letter dual genome (111 = 0 mod 3). For each variant:
steps to first division alone (no mutation, cap as fertility_probe), tasks kept; for variants that divide, fertility of
40 mutated children. Usage: python3 dual_delete.py -> out/dual_delete.txt"""
from collections import Counter
from petri import parse
import fertility_probe as fp
g0 = parse(fp.DUAL); res = Counter(); rows = []
for i in range(len(g0)):
    g = g0[:i] + g0[i + 1:]; r = fp.first_div(g, 1, False)
    if r is None: res["never"] += 1; continue
    both = {"AND", "ANDN"} <= r[1]; sp = "fast" if r[0] < 400 else "slow"
    res[(sp, "AND+ANDN" if both else "lost")] += 1
    fert = 0
    for s in range(40):
        p = fp.first_div(g, 1000 + s, True)
        if p is None: continue
        fert += fp.first_div(p[2], 5000 + s, False) is not None
    rows.append(f"del {i}: steps {r[0]}, {sp}, {'AND+ANDN' if both else 'lost'}, fertile {fert}/40")
out = [f"len {len(g0)-1} (mod3 {(len(g0)-1)%3}), {len(g0)} deletions: {dict(res)}"] + rows
print("\n".join(out)); open("out/dual_delete.txt", "w").write("\n".join(out) + "\n")
