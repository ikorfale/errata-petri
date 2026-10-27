"""#530 / zenith 105233: is AND inherited and selected against, or re-created by mutation and lost at once?
Same setup as evo_and.py (s2-dominant monoculture, default rates, no parasites, fresh seeds). Each division is
logged by two flags: did the dividing parent earn AND in this gestation, and was the parent itself born from a
division that earned AND. Reports P(child division earns AND | parent born of AND) vs the background rate, and
divisions per organism born (fecundity) for AND-born vs other organisms. Counts only, no merit model.
Second pass (27.10): first-division steps (o.age at the first division) and merit paid, by flag; optional "noage"
third argument switches old-age death off, to test whether AND-born organisms run out of life before dividing.
Usage: python3 and_heredity.py UPDATES SEED[,SEED...] [noage] -> out/and_heredity.jsonl"""
import json, sys, time
from collections import Counter
from petri import World, parse
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
ups = int(sys.argv[1]); seeds = [int(s) for s in sys.argv[2].split(",")]; NOAGE = sys.argv[3:] == ["noage"]
for s in seeds:
    w = World(seed=s); w.age_limit = not NOAGE; t0 = time.time(); k = Counter(); ndiv = {}; first = Counter()
    for c in range(w.n): w.inject(parse(TOP), "s2", cell=c)
    _div, _nb, flag, last = w.divide, w.neighbour, {}, [None]   # Org has __slots__: flags by id, strong refs kept
    def nb(c, _nb=_nb, last=last):
        last[0] = _nb(c); return last[0]
    w.neighbour = nb
    def divide(o, c, _div=_div, w=w, k=k, flag=flag, last=last):
        n0, earned, tasks0 = w.births, "AND" in o.tasks, sorted(o.tasks)
        born_and = flag.get(id(o), (None, False))[1]
        last[0] = None; _div(o, c)
        if w.births == n0: return
        k[("div", born_and, earned)] += 1
        if id(o) not in ndiv:               # first division of this organism: its first-gestation steps and merit paid
            ndiv[id(o)] = o; g = ("and" if earned else "other")
            if earned: first[("set", "+".join(tasks0))] += 1   # tasks0: restart() clears o.tasks
            first[(g, "n")] += 1; first[(g, "steps")] += o.age; first[(g, "merit")] += w.cells[last[0]].merit
        kid = w.cells[last[0]]; flag[id(kid)] = (kid, earned); k[("born", earned)] += 1
        if len(flag) > 20000:
            live = {id(x) for x in w.cells if x is not None}
            for i in [i for i in flag if i not in live]: del flag[i]
            for i in [i for i in ndiv if i not in live]: del ndiv[i]
    w.divide = divide
    for u in range(1, ups + 1): w.run_update()
    tot = lambda b: k[("div", b, True)] + k[("div", b, False)]
    fd = {g: {"n": first[(g, "n")], "steps": round(first[(g, "steps")] / max(1, first[(g, "n")]), 1),
              "merit": round(first[(g, "merit")] / max(1, first[(g, "n")]), 1)} for g in ("and", "other")}
    fd["and_task_sets"] = sorted(((k2, v) for (k1, k2), v in first.items() if k1 == "set"), key=lambda x: -x[1])[:6]
    row = {"seed": s, "updates": ups, "noage": NOAGE, "first_division": fd, "sec": round(time.time() - t0),
           "div": {f"born_and={b},earned={e}": k[("div", b, e)] for b in (True, False) for e in (True, False)},
           "born": {"and": k[("born", True)], "other": k[("born", False)]},
           "p_and_given_and_parent": round(k[("div", True, True)] / max(1, tot(True)), 4),
           "p_and_given_other": round(k[("div", False, True)] / max(1, tot(False)), 5),
           "divs_per_born_and": round(tot(True) / max(1, k[("born", True)]), 3),
           "divs_per_born_other": round(tot(False) / max(1, k[("born", False)]), 3)}
    print(json.dumps(row), flush=True)
    open("out/and_heredity.jsonl", "a").write(json.dumps(row) + "\n")
