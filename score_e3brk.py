"""Score PREDICT-e3brk-1028 P1-P3 (default rule) from out/e3brk_{a,b}.jsonl vs out/e3_{a,b}.jsonl.
Per-mode share pooled over worlds, interval = bootstrap over seeds (2000 draws, rng 541)."""
import json, random
from collections import defaultdict
def load(fs):
    W, A = {}, {}
    for f in fs:
        for line in open(f):
            r = json.loads(line)
            if "warm" in r: W[r["warm"]["seed"]] = r["warm"]
            else: A[(r["seed"], r["mode"], r["L"])] = r
    return W, A
Wb, Ab = load(["out/e3brk_a.jsonl", "out/e3brk_b.jsonl"]); W0, A0 = load(["out/e3_a.jsonl", "out/e3_b.jsonl"])
print("worlds", len(Ab), "orig", len(A0), "warm", len(Wb))
mism = [k for k in A0 if k not in Ab or Ab[k]["h_arm"] != A0[k]["h_arm"] or Ab[k]["census"] != A0[k]["census"]]
print("P3 mismatches", len(mism), mism[:5], "missing", [k for k in A0 if k not in Ab][:5])
rng = random.Random(541)
def share(keys):
    b = sum(Ab[k]["brk"][0] for k in keys); x = sum(Ab[k]["brk"][1] for k in keys); return x / b
bymode = defaultdict(list); bymL = defaultdict(list)
for k in Ab: bymode[k[1]].append(k); bymL[(k[1], k[2])].append(k)
seeds = sorted({k[0] for k in Ab})
for m, ks in sorted(bymode.items()):
    boots = []
    for _ in range(2000):
        ss = [rng.choice(seeds) for _ in seeds]
        kk = [k for s in ss for k in ks if k[0] == s]
        boots.append(share(kk))
    boots.sort()
    print(f"P1 {m:8s} n={len(ks):3d} share={100*share(ks):.3f}%  95%CI {100*boots[50]:.3f}-{100*boots[1949]:.3f}")
Ls = sorted({k[2] for k in Ab})
for L in Ls:
    ms = {m: share(bymL[(m, L)]) for m in bymode if (m, L) in bymL}
    if len(ms) > 1:
        print(f"P2 L={L} " + " ".join(f"{m}={100*v:.3f}%" for m, v in ms.items()) + f"  spread={100*(max(ms.values())-min(ms.values())):.3f} pts")
wb = sum(w["brk_warm"][1] for w in Wb.values()) / sum(w["brk_warm"][0] for w in Wb.values())
print(f"warm-up pooled share {100*wb:.3f}%")
