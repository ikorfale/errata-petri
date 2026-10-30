"""Day-3 sweep, step 3: does the length-91 genotype win a head-to-head against the length-89 one it replaced?
Prereg: PREDICT-compete-1030.md. A 30x30 world (daily settings) is filled at random, half with the top 89 genotype at
82,000 and half with the top 91 at 82,500 (replay-day-003-swaps.json); copy_mut = indel = 0, so no new genotypes.
Runs until one side holds >= 90% of the living or MAXU updates pass. Control arm: the same 89 genotype under two labels
(neutral by construction: who wins is drift).
v1 (default) starts every organism at merit = its length; the first to divide jumps to task merit (~5.9M) and the
rest get almost no CPU, so v1 measures a start-up race, not fitness. v2 starts both at their census merit.
mixed: children placed uniformly at random (tests the kin-competition guess, PREDICT-compete-1030.md part 3).
Usage: python3 compete.py SEED [control] [v2] [mixed] [swap]  -> one JSON line"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from petri import World
MAXU = 1500

def genomes():
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily/replay-day-003-swaps.json")))
    c = {x["update"]: x for x in d["censuses"]}
    t89, t91 = c[82000]["top"]["89"][0], c[82500]["top"]["91"][0]
    return list(bytes.fromhex(t89["g"])), list(bytes.fromhex(t91["g"])), t89["merit"], t91["merit"]

def main(seed, control=False, census_merit=False, mixed=False, swap=False):
    g89, g91, m89, m91 = genomes()
    a, b = (g89, g89) if control else (g89, g91)
    ma, mb = (m89, m89 if control else m91)
    w = World(seed=seed, copy_mut=0.0, indel=0.0)
    if mixed:                               # well-mixed: a child goes to a uniformly random cell, not a neighbour
        w.neighbour = lambda c: w.rng.randrange(w.n)
    cells = list(range(w.n)); w.rng.shuffle(cells)
    for i, cell in enumerate(cells):
        if swap: i += 1                     # swap: same layout, genotypes exchanged between the two slot sets
        w.inject(a if i % 2 == 0 else b, "A" if i % 2 == 0 else "B", cell=cell)
        if census_merit:                    # v2: start at the merit the genotype had in the census, not its length
            w.cells[cell].merit = ma if i % 2 == 0 else mb
    t0, trace = time.time(), []
    for u in range(1, MAXU + 1):
        w.run_update()
        live = [o for o in w.cells if o is not None]
        nb = sum(1 for o in live if o.lineage == "B")
        if u % 25 == 0: trace.append((u, len(live), nb))
        if live and (nb >= 0.9 * len(live) or nb <= 0.1 * len(live)):
            break
    live = [o for o in w.cells if o is not None]
    nb = sum(1 for o in live if o.lineage == "B")
    win = "B" if nb >= 0.9 * len(live) else "A" if nb <= 0.1 * len(live) else "none"
    return {"seed": seed, "arm": ("control" if control else "89vs91") + ("-v2" if census_merit else "") + ("-mixed" if mixed else "") + ("-swap" if swap else ""), "winner": win, "update": u, "pop": len(live),
            "nB": nb, "sec": round(time.time() - t0), "trace": trace}

if __name__ == "__main__":
    print(json.dumps(main(int(sys.argv[1]), "control" in sys.argv[2:], "v2" in sys.argv[2:], "mixed" in sys.argv[2:], "swap" in sys.argv[2:])), flush=True)
