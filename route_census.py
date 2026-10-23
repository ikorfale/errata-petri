# For the top genotype of every census snapshot in a run: how was each task's first credited output built?
# Taint tracking along the trace: a register value carries the set of non-nand op kinds that fed it
# ('A' add/sub, 'K' inc/dec/shift: constants and offsets). Inputs are clean; nand unions its operands; swap,
# push and pop move the sets. A task whose credited value has an empty set was computed by nand alone.
# Usage: python3 route_census.py out/tagged_s1.json [--every 10]
import json, sys
from collections import Counter, defaultdict
sys.path.insert(0, __import__("os").path.dirname(__file__))
from petri import World, OPS, parse, COMP, NOP

def routes(genome, seed=7, cap=20000):
    w = World(side=5, seed=seed, copy_mut=0.0)
    w.inject(genome, "t", cell=0)
    o = w.cells[0]
    t = [frozenset()] * 3; st = []; out = {}; n = 0
    while w.births == 0 and n < cap:
        L = len(o.mem); ip = o.heads[0] % L; op = OPS[o.mem[ip]]
        nxt = o.mem[(ip + 1) % L]; r = nxt if nxt in NOP else 1
        tasks0 = set(o.tasks); reg0 = list(o.reg); t0 = list(t)
        w.step(o, 0); n += 1; o = w.cells[0]
        if op == "IO":
            for k in o.tasks - tasks0:
                out[k] = "".join(sorted(t0[r])) or "nand"
            t[r] = frozenset()
        elif op == "nand":
            t[r] = t0[1] | t0[2]
        elif op in ("add", "sub"):
            t[r] = t0[1] | t0[2] | {"A"}
        elif op in ("inc", "dec", "shift-l", "shift-r"):
            t[r] = t0[r] | {"K"}
        elif op == "swap":
            t[r], t[COMP[r]] = t0[COMP[r]], t0[r]
        elif op == "push" and len(st) < 10 and len(o.stk) > len(st):
            st.append(t0[r])
        elif op == "pop":
            t[r] = st.pop() if st else frozenset()
        else:
            for i in range(3):
                if o.reg[i] != reg0[i]:
                    t[i] = frozenset({"K"})      # heads, search results, alloc sizes: not input-derived
        if len(st) > len(o.stk):
            st = st[-len(o.stk):] if o.stk else []
    return out

rows = json.load(open(sys.argv[1]))
every = int(sys.argv[sys.argv.index("--every") + 1]) if "--every" in sys.argv else 10
tally = defaultdict(Counter)
for row in rows[every - 1::every]:
    rt = routes(parse(row["top"]))
    for k, v in rt.items():
        tally[k][v] += 1
    print(row["update"], " ".join(f"{k}:{v}" for k, v in sorted(rt.items())))
print("totals:", {k: dict(c) for k, c in sorted(tally.items())})
