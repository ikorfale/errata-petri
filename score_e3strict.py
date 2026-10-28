"""Score PREDICT-e3brk-1028 P4-P5 (strict division rule) from out/e3strict_{a,b}.jsonl vs out/e3brk_{a,b}.jsonl.
Also checks out/e3strict_c.jsonl (seeds 1-7 rerun with refusal counters) equals e3strict_a except the "ref" fields.
L50 and the seed-cluster bootstrap are e2_verdict.py's, unchanged."""
import json
from collections import defaultdict
from e2_verdict import outcome, l50, boot
def load(fs):
    W, A = {}, {}
    for f in fs:
        for line in open(f):
            r = json.loads(line)
            if "warm" in r: W[r["warm"]["seed"]] = r["warm"]
            else: A[(r["seed"], r["mode"], r["L"])] = r
    return W, A
Ws, As = load(["out/e3strict_a.jsonl", "out/e3strict_b.jsonl"]); Wd, Ad = load(["out/e3brk_a.jsonl", "out/e3brk_b.jsonl"])
Wc, Ac = load(["out/e3strict_c.jsonl"])
strip = lambda r: {k: v for k, v in r.items() if k not in ("ref", "ref_warm", "cpu_s")}
print("strict-c equals strict-a outside ref:", all(strip(Ac[k]) == strip(As[k]) for k in Ac) and all(strip(Wc[s]) == strip(Ws[s]) for s in Wc), len(Ac), "worlds")
print("worlds strict", len(As), "default", len(Ad))
nz = [k for k, r in As.items() if r["brk"][1]] + [("warm", s) for s, w in Ws.items() if w["brk_warm"][1]]
print("P4a breakups > 0 under strict:", len(nz), nz[:5])
bad = []
for s in sorted(Ws):
    a, b = Ws[s]["h_occupied"], Wd[s]["h_occupied"]; d = a / b - 1
    print(f"  warm seed {s:2d}: h_occupied strict {a:.5f} default {b:.5f}  {100*d:+.1f}%"); bad += [s] if abs(d) > .2 else []
print("P4b seeds outside 20%:", bad)
def L50s(A):
    by = defaultdict(list)
    for (s, m, L), r in A.items(): by[m].append((L, outcome(r), r))
    out = {}
    for m in ("local", "host", "updates"):
        iv, note = l50([(L, o) for L, o, _ in by[m]]); out[m] = (iv, note, boot(by[m]))
    return out
for name, A in (("default", Ad), ("strict", As)):
    o = L50s(A)
    for m, (iv, note, bs) in o.items(): print(f"{name:8s} {m:8s} L50 {iv} ({note}) boot {bs}")
    pt = lambda m: sum(o[m][0]) / 2
    print(f"{name:8s} shift host-local {pt('host') - pt('local'):.2f}; host boot lo vs local point+3 = {o['host'][2][0]:.2f} vs {pt('local') + 3:.2f}, hi {o['host'][2][1]:.2f}")
