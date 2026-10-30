"""Score PREDICT-swaps-1030.md on daily/replay-day-002-swaps.json (replay_swaps.py, day 2, digest-checked).
A modal swap: consecutive censuses where the mode changes between 89 and 90 (either way). For each swap: the dominant
genotype of the new mode vs the dominant genotype of the old mode one census before (Levenshtein distance, aligned
diffs), each run alone in a 5x5 world (sweep_iso.run, seeds 1-3): steps to first division, child merit, tasks.
Also the same for every census where the dominant genotype of the 89 or 90 class changes identity."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import OPS
src = open("sweep_iso.py").read().split("def profile")[0]   # sweep_iso runs its sweeps at import; take run() only
ns = {"__file__": os.path.abspath("sweep_iso.py")}; exec(compile(src, "sweep_iso.py", "exec"), ns); run = ns["run"]

def lev(a, b):
    d = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(b) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[-1]

def iso(g):
    r = [run(g, s) for s in (1, 2, 3)]
    r = [x for x in r if x]
    return (r[0][0], r[0][1], "+".join(r[0][2])) if r else ("sterile", None, "")

C = json.load(open("daily/replay-day-002-swaps.json"))["censuses"]
def dom(c, L):
    t = c["top"].get(str(L))
    return (bytes.fromhex(t[0]["g"]), t[0]["n"]) if t else (None, 0)
swaps = []
for a, b in zip(C, C[1:]):
    if {a["mode"], b["mode"]} == {89, 90}:
        old, new = a["mode"], b["mode"]
        go, no = dom(a, old); gn, nn = dom(b, new)
        dist = lev(go, gn)
        io, inew = iso(go), iso(gn)
        swaps.append(dist)
        print(f"swap {a['update']:>6}->{b['update']:>6}: {old}->{new}  dominant {old}: {no} copies {io} | dominant {new}: {nn} copies {inew} | lev {dist}")
print(f"S3: swaps with lev >= 2: {sum(d >= 2 for d in swaps)} of {len(swaps)}")
