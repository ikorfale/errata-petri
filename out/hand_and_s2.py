"""#451: hand-built AND+ANDN genome from the s2 dominant. After the NOT output (IO at 83) C holds all ones; insert
push B / IO / pop C / nand / pop C (empty -> 0) / dec C / nand / IO, i.e. AND = nand(nand(u1, u2), ones), before h-search.
Then the same checks as and_subpairs_low_s2.py: one traced gestation (seed 7) and solo viability (20x20, seeds 1-5, pop@150)."""
import json, sys, statistics as st
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, parse
D = json.load(open("out/s2_dump.json"))
top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
def tasks(g):
    log, _ = trace(parse(g), 7, 1, cap=3000)
    return tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()
def solo(g, n=150):
    out = []
    for s in range(1, 6):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(n): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
print("top", len(top), top[80:86], "tasks", tasks(top), "solo", solo(top))
INS = sys.argv[1] if len(sys.argv) > 1 else "oypcupcncuy"
for pos in (84,):
    g = top[:pos] + INS + top[pos:]
    print("ins", pos, INS, "len", len(g), "tasks", tasks(g), "solo", solo(g), g)
