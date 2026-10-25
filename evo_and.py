"""#481 proper: does AND arise and fix in a mutating world that starts as a monoculture of the s2 dominant?
s2 itself ran 100,000 updates without AND (README); the one-step scan found 0 fitter task-gainers in 1,254 neutral
fills. Here: fresh RNG seeds, default v0.3 rates (copy_mut 0.0075, indel 0.05), no parasites, 30x30 filled with the
s2 dominant. Every 250 updates log the carriers of AND, of AND with all four s2 tasks, mean length, genotypes.
Usage: python3 evo_and.py UPDATES SEED[,SEED...]  -> out/evo_and.jsonl (one line per checkpoint)"""
import json, sys, time, hashlib
from collections import Counter
from petri import World, parse, show
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
FOUR = {"ANDN", "NAND", "NOT", "ORN"}
ups = int(sys.argv[1]); seeds = [int(s) for s in sys.argv[2].split(",")]
with open("out/evo_and.jsonl", "a") as out:
    for s in seeds:
        w = World(seed=s); t0 = time.time(); pb = pa = 0
        out.write(json.dumps({"seed": s, "update": 0, "top": TOP, "copy_mut": w.copy_mut, "indel": w.indel,
                              "side": w.side, "slice": w.slice, "parasites": w.parasites,
                              "petri_sha256": hashlib.sha256(open("petri.py", "rb").read()).hexdigest()}) + "\n")
        for c in range(w.n): w.inject(parse(TOP), "s2", cell=c)
        for u in range(1, ups + 1):
            w.run_update()
            if u % 250 == 0 or u == ups:
                live = [o for o in w.cells if o is not None]
                andc = [o for o in live if "AND" in o.tasks]
                c = w.census()
                g = Counter(show(o.mem[:o.glen]) for o in live)
                b, a = c["births"], c["task_births"].get("AND", 0)
                row = {"seed": s, "update": u, "pop": len(live), "and": len(andc),
                       "and_share_births": round((a - pa) / max(1, b - pb), 4),   # AND births / births since last row
                       "top": g.most_common(1)[0], "still_top0": g.get(TOP, 0),
                       "and_all4": sum(FOUR <= set(o.tasks) for o in andc),
                       "and_births": c["task_births"].get("AND", 0), "births": c["births"],
                       "genotypes": c["genotypes"], "mean_len": c["mean_len"], "tasks_now": c["tasks_now"],
                       "sec": round(time.time() - t0)}
                pb, pa = b, a
                if andc:
                    row["and_top"] = Counter(show(o.mem[:o.glen]) for o in andc).most_common(1)[0]
                out.write(json.dumps(row) + "\n"); out.flush()
        json.dump(g.most_common(), open(f"out/evo_and_census_s{s}.json", "w"))
