"""#530 / zenith 105387: where does the residual of AND-born fecundity go (0.37-0.38 observed vs ~0.43 from merit/steps)?
Same setup as and_heredity.py. Two counts by birth flag (born from a division that earned AND, or not):
(1) overwrites: was the victim overwritten before its first division, or after; (2) updates from birth to first
division. If AND-born organisms are overwritten before dividing more often than others, that is the residual.
Usage: python3 and_deaths.py UPDATES SEED[,SEED...] -> out/and_deaths.jsonl"""
import json, sys, time
from collections import Counter
from petri import World, parse
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
ups = int(sys.argv[1]); seeds = [int(s) for s in sys.argv[2].split(",")]
for s in seeds:
    w = World(seed=s); t0 = time.time(); k = Counter(); info = {}   # id -> [org, born_and, divided]
    for c in range(w.n): w.inject(parse(TOP), "s2", cell=c)
    _div, _nb, last = w.divide, w.neighbour, [None]
    def nb(c, _nb=_nb, w=w, k=k, info=info, last=last):
        t = _nb(c); last[0] = t; v = w.cells[t]
        if v is not None and id(v) in info and info[id(v)][0] is v:
            _, ba, dv = info[id(v)]; last.append((ba, dv))
        return t
    w.neighbour = nb
    def divide(o, c, _div=_div, w=w, k=k, info=info, last=last):
        n0, earned = w.births, "AND" in o.tasks
        del last[1:]; last[0] = None; _div(o, c)
        if w.births == n0: return
        if len(last) > 1: ba, dv = last[1]; k[("overwritten", ba, dv)] += 1
        rec = info.get(id(o))
        if rec is not None and rec[0] is o and not rec[2]:
            rec[2] = True; k[("first", rec[1], "n")] += 1; k[("first", rec[1], "upd")] += w.update - o.born
        kid = w.cells[last[0]]; info[id(kid)] = [kid, earned, False]; k[("born", earned)] += 1
        if len(info) > 40000:
            live = {id(x) for x in w.cells if x is not None}
            for i in [i for i in info if i not in live]: del info[i]
    w.divide = divide
    for u in range(1, ups + 1): w.run_update()
    row = {"seed": s, "updates": ups, "sec": round(time.time() - t0)}
    for b, name in ((True, "and"), (False, "other")):
        nb_ = k[("born", b)]; ob, oa = k[("overwritten", b, False)], k[("overwritten", b, True)]
        row[name] = {"born": nb_, "overwritten_before_first_div": ob, "overwritten_after": oa,
                     "p_overwritten_before_div": round(ob / max(1, nb_), 4),
                     "p_ever_divided": round(k[("first", b, "n")] / max(1, nb_), 4),
                     "updates_to_first_div": round(k[("first", b, "upd")] / max(1, k[("first", b, "n")]), 2)}
    print(json.dumps(row), flush=True)
    open("out/and_deaths.jsonl", "a").write(json.dumps(row) + "\n")
