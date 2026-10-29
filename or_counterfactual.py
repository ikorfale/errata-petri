"""rhea0987 (board 107241): did OR's reward drive the 63,000 sweep under competition? Start from the saved day-2 world
at 62,500 (the OR clade opened there: 38 members), tag every live organism that performs OR (current or last gestation)
as clade "C", all others "X" (the tag rides on Org.lineage, which the dynamics never read). Two arms from the same
world with the world RNG reseeded to the same seed: OR worth 2^3 as in the run ("real") or 2^0 ("neutral"); no other
task value changes. Census every 500 updates to 65,000: OR performers, NOT/NAND performers, share of live organisms
descended from C. Seed "orig" = no reseed, real arm only: must reproduce series.jsonl (OR 472 at 63,000).
Usage: python3 or_counterfactual.py [start_pkl] > out/or_counterfactual.txt"""
import json, os, pickle, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri, daily
START = sys.argv[1] if len(sys.argv) > 1 else "out/sweeps/w62500.pkl"
END, SEEDS = 65000, ["orig"] + list(range(1, 9))
REAL = list(petri.TASKS)
NEUT_B = int(os.environ.get("OR_NEUTRAL_EXP", "0"))   # 0 = no reward; 2 = break-even with NOT+NAND (added 29.10)
NEUT = [(n, f, NEUT_B if n == "OR" else b) for n, f, b in REAL]
def does(o, t): return t in o.tasks or t in (getattr(o, "ptasks", None) or ())
def run(arm, seed):
    petri.TASKS[:] = REAL if arm == "real" else NEUT
    w = pickle.load(open(START, "rb"))
    live = [o for o in w.cells if o is not None]
    for o in live: o.lineage = "C" if does(o, "OR") else "X"
    if seed != "orig": w.rng = random.Random(seed)
    rows = []
    while w.update < END:
        w.run_update()
        if w.update % 500 == 0:
            live = [o for o in w.cells if o is not None]
            t = daily.census(w)["tasks_now"]
            rows.append({"u": w.update, "n": len(live), "OR": t.get("OR", 0), "NOT": t.get("NOT", 0), "NAND": t.get("NAND", 0),
                         "C": round(sum(o.lineage == "C" for o in live) / max(1, len(live)), 3)})
    petri.TASKS[:] = REAL
    return rows
c0 = sum(1 for o in pickle.load(open(START, "rb")).cells if o is not None and does(o, "OR"))
print(json.dumps({"start": START, "clade_C_at_start": c0, "neutral_or_exp": NEUT_B}), flush=True)
for seed in SEEDS:
    if seed == "orig" and NEUT_B: continue
    for arm in (["real"] if seed == "orig" else ["real", "neutral"] if not NEUT_B else ["neutral"]):
        print(json.dumps({"arm": arm, "seed": seed, "rows": run(arm, seed)}), flush=True)
