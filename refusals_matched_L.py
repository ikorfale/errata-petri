"""#541 theone 106354 pt 3: refusals per arm restricted to the L values all three modes share ({24, 28, 32}),
per L and pooled over the shared grid, from out/e3strict_c.jsonl (seeds 1-7, strict rule, with counters).
Also per-seed spread at the shared grid so a gap can be read against seed noise."""
import json
from collections import defaultdict
rows = [json.loads(l) for l in open("out/e3strict_c.jsonl")]
rows = [r for r in rows if "warm" not in r]
Ls = {m: sorted({r["L"] for r in rows if r["mode"] == m}) for m in ("local", "host", "updates")}
shared = sorted(set.intersection(*map(set, Ls.values())))
print("L grids:", Ls, "shared:", shared)
def rate(rs):
    B = sum(r["brk"][0] for r in rs); v = sum(r["ref"]["viable_refusals"] for r in rs); e = sum(r["ref"]["episodes"] for r in rs)
    return B, 1000 * v / B, 1000 * e / B, (v / e if e else float("nan"))
print("\nmode     L    worlds  births   viable/1k  episodes/1k  viable/episode")
for L in shared + ["shared"]:
    for m in ("local", "host", "updates"):
        rs = [r for r in rows if r["mode"] == m and (r["L"] == L if L != "shared" else r["L"] in shared)]
        B, v, e, ve = rate(rs)
        print(f"{m:8s} {str(L):6s} {len(rs):4d} {B:9d} {v:10.1f} {e:11.2f} {ve:10.1f}")
print("\nper seed, shared grid: viable/1k (local, host, updates)")
for s in sorted({r["seed"] for r in rows}):
    print(s, *(f"{rate([r for r in rows if r['seed']==s and r['mode']==m and r['L'] in shared])[1]:7.1f}" for m in ("local","host","updates")))
