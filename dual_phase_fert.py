"""For every 113-letter dual variant (one 'q' inserted) that divides fast (<400 steps) keeping AND+ANDN alone: fertility of
40 mutated children (fertility_probe method). Picks the variant to re-run the falsifier with. -> out/dual_phase_fert.txt"""
import fertility_probe as fp
from petri import parse
g0 = parse(fp.DUAL); q = parse("q")[0]; rows = []
for i in range(len(g0) + 1):
    g = g0[:i] + [q] + g0[i:]; r = fp.first_div(g, 1, False)
    if r is None or r[0] >= 400 or not {"AND", "ANDN"} <= r[1]: continue
    fert = keep = 0
    for s in range(40):
        p = fp.first_div(g, 1000 + s, True)
        if p is None: continue
        c = fp.first_div(p[2], 5000 + s, False)
        if c is None: continue
        fert += 1; keep += {"AND", "ANDN"} <= c[1]
    rows.append((fert, keep, -r[0], i)); 
rows.sort(reverse=True)
lines = [f"pos {i}: steps {-st}, fertile {f}/40, keep AND+ANDN {k}/40" for f, k, st, i in rows]
print(len(rows), "variants"); print("\n".join(lines[:8])); print("fertility counts:", sorted(r[0] for r in rows))
open("out/dual_phase_fert.txt", "w").write("\n".join(lines) + "\n")
