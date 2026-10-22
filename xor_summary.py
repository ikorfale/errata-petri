# Summarise out/xor_trace/s*.txt: XOR/EQU credits explained by a cheaper task on the same pair,
# IP location, and retests (mutation off, 300 gestations) per watched task.
import glob, json, re
from collections import defaultdict
print("p=(3/4)^32 =", f"{0.75**32:.3e}")
tot = defaultdict(int)
for f in sorted(glob.glob("out/xor_trace/s*.txt")):
    L = open(f).read().splitlines()
    head = json.loads(L[0]); s = head["seed"]
    cr = {}
    for l in L:
        m = re.match(r"CREDIT (\w+) (\S+) (\d+)", l)
        if m: cr[(m[1], m[2])] = int(m[3])
    for t in ("XOR", "EQU"):
        n = cr.get((t, "ip-in-parent"), 0) + cr.get((t, "ip-in-child"), 0)
        also = {k[1]: v for k, v in cr.items() if k[0] == t and k[1].startswith("also:")}
        exact = cr.get((t, "exact-only"), 0)
        print(f"seed {s} {t}: credits {n}, in child {cr.get((t,'ip-in-child'),0)}, unexplained {exact}, also {also}, ones {cr.get((t,'a|b=ones'),0)} and0 {cr.get((t,'a&b=0'),0)} subset {cr.get((t,'subset'),0)}")
        tot[t] += n; tot[t + "_unexpl"] += exact; tot[t + "_child"] += cr.get((t, "ip-in-child"), 0)
    for l in L:
        if l.startswith("RETEST"):
            p = l.split(); t = p[1]; g = int(p[5]); w = json.loads(l.split("watched ")[1].split(" all")[0])
            tot[(t, "geno")] += 1; tot[(t, "gest")] += g; tot[(t, "hit")] += w[t]
            if g == 300 and w[t] == 300: tot[(t, "full")] += 1
for k, v in tot.items(): print("TOTAL", k, v)
