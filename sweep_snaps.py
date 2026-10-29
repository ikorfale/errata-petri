"""Day-2 sweeps (coal >= 0.5 at 57.5k, 63k, 66.5k, 75.5k): did each come from copy speed or from a task? (promise in
board 106752: check whether each flagged sweep shortens gestation in isolation). Step 1: replay day 2 from the day-1
world (deterministic; lineage fields are never read by the dynamics, readwatch day-002) and pickle the world at the
censuses around each sweep. Checked against series.jsonl task counts at every saved census.
Usage: python3 sweep_snaps.py > out/sweep_snaps.txt"""
import json, os, pickle, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daily
w = pickle.load(open("daily/base/day-001/world.pkl", "rb"))
SAVE = {55500, 56500, 57500, 61500, 62500, 63000, 65500, 66500, 74500, 75500}
ser = {}
for l in open("daily/series.jsonl"):
    r = json.loads(l); ser[r["update"]] = r["tasks_now"]
os.makedirs("out/sweeps", exist_ok=True)
while w.update < max(SAVE):
    w.run_update()
    if w.update in SAVE:
        t = daily.census(w)["tasks_now"]; ok = all(t.get(k, 0) == v for k, v in ser.get(w.update, {}).items())
        print(w.update, "match series" if ok else "MISMATCH", t, flush=True)
        pickle.dump(w, open(f"out/sweeps/w{w.update}.pkl", "wb"))
