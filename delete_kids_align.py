"""Alignment of each clean child (delete_kids.py) to its parent: best cyclic shift s (k[j] == g[(j+s) % n]) and how many
letters match. Usage: python3 delete_kids_align.py -> out/delete_kids_align.txt"""
from collections import Counter
from petri import parse
import fertility_probe as fp
g0 = parse(fp.DUAL); sh = Counter(); out = []
for i in range(len(g0)):
    g = g0[:i] + g0[i + 1:]; r = fp.first_div(g, 1, False)
    if r is None: continue
    k = r[2]; n = len(g)
    best = max(range(n), key=lambda s: sum(k[j] == g[(j + s) % n] for j in range(n)))
    m = sum(k[j] == g[(j + best) % n] for j in range(n)); s = best - n if best > n // 2 else best; sh[s] += 1
    out.append(f"del {i}: best cyclic shift {s}, {m}/{n} letters match")
out.append(f"shifts: {dict(sh)}")
print("\n".join(out)); open("out/delete_kids_align.txt", "w").write("\n".join(out) + "\n")
