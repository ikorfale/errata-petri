"""Replay a day of the long Petri world from its saved base and record the genome-length mix at every census
(PREDICT-shrink-1029.md). Same loop and lineage censuses as daily.py / replay_origins.py, adds no state and draws no
random numbers, and must end on the day's digest or its output is discarded.
Usage: python3 replay_lengths.py BASE_DIR UPDATES DIGEST_PREFIX > out.json"""
import json, os, pickle, sys, time, hashlib
from collections import Counter
import petri, daily
from world_digest import canon_s
base, U, want = sys.argv[1], int(sys.argv[2]), sys.argv[3]
w = pickle.load(open(os.path.join(base, "world.pkl"), "rb")); st = json.load(open(os.path.join(base, "state.json")))
assert hashlib.sha256(canon_s(w).encode()).hexdigest() == st["digest"], "base world does not match its state digest"
if "lin_prev" in st:
    lin_prev = {k: {int(c): set(v) for c, v in m.items()} for k, m in st["lin_prev"].items()}
    lin_prev["_gen"] = [(u, {int(c): x for c, x in m.items()}) for u, m in st.get("lin_gen", [])]
    lin_prev["_deepf"] = st.get("lin_deepf", {})
else: _, lin_prev = daily.lineage_census(w, {})
def row(w):
    live = [o for o in w.cells if o is not None]; L = Counter(o.glen for o in live)
    mer = {}
    for o in live: mer.setdefault(o.glen, []).append(o.merit)
    return {"update": w.update, "pop": len(live), "lens": dict(sorted(L.items())),
            "mode": L.most_common(1)[0][0], "share2": sum(n for l, n in L.items() if l % 3 == 2) / max(1, len(live)),
            "merit_by_len": {l: sorted(v)[len(v) // 2] for l, v in mer.items() if L[l] >= 5}}
out = [row(w)]; u0, t0 = w.update, time.time()
while w.update - u0 < U:
    w.run_update()
    if w.update % daily.SAMPLE == 0:
        _, lin_prev = daily.lineage_census(w, lin_prev); out.append(row(w))
dig = hashlib.sha256(canon_s(w).encode()).hexdigest()
if not dig.startswith(want): sys.exit(f"replay ended on digest {dig[:16]}, expected {want}: results discarded")
sys.stderr.write(f"replayed {w.update - u0} updates in {time.time() - t0:.0f}s, digest ok\n")
json.dump({"base": base, "digest": dig, "censuses": out}, sys.stdout)
