"""Check of my guess on zenith 105575: for every single deletion of the dual genome that divides, is the clean
(mutation-off) child an exact copy, how long is it, and does it divide? Usage: python3 delete_kids.py -> out/delete_kids.txt"""
from collections import Counter
from petri import parse
import fertility_probe as fp
g0 = parse(fp.DUAL); rows = []; tally = Counter()
for i in range(len(g0)):
    g = g0[:i] + g0[i + 1:]; r = fp.first_div(g, 1, False)
    if r is None: continue
    kid = r[2]; exact = kid == list(g); c = fp.first_div(kid, 1, False)
    tally[("exact" if exact else "changed", "divides" if c else "never")] += 1
    rows.append(f"del {i}: parent {len(g)} child {len(kid)} (mod3 {len(kid)%3}) {'exact' if exact else 'changed'}, "
                f"child {'divides in ' + str(c[0]) if c else 'never divides'}")
out = [f"{sum(tally.values())} dividing variants: {dict(tally)}"] + rows
print("\n".join(out)); open("out/delete_kids.txt", "w").write("\n".join(out) + "\n")
