"""L drift of the breakup share (board 105982, 'not explained'): does it follow parasite load?
Default-rule E3 worlds (out/e3brk_*.jsonl), per world: breakup share brk[1]/brk[0] and mean infected share inf/pop over
the census. Prints per-L means and the within-L correlation. Written 29.10 16:13 UTC (date -u)."""
import json, numpy as np, collections
by = collections.defaultdict(list)
for f in ["out/e3brk_a.jsonl", "out/e3brk_b.jsonl"]:
    for l in open(f):
        r = json.loads(l)
        if "warm" in r or r.get("strict"): continue
        inf = np.mean([x["inf"] / max(x["pop"], 1) for x in r["census"]])
        by[r["L"]].append((r["brk"][1] / r["brk"][0], inf))
for L in sorted(by):
    a = np.array(by[L])
    print(f"L={L} worlds={len(a)} share={a[:,0].mean():.4f} infected={a[:,1].mean():.3f} r_within={np.corrcoef(a[:,0], a[:,1])[0,1]:.2f}")
