"""#451: is the copy loop's phase the barrier? The s2 copy loop does 3 h-copy per if-label check and stops when the
last copied pair is the label complement 'ab' (genome end), so a length change that is not a multiple of 3 should
overshoot. Insert k harmless swap-stk ('q', a no-op) at 84 for k = 0..6; solo pop at 150 (20x20, seeds 1-5),
and gestation steps in one traced gestation."""
import sys, json, statistics as st
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
def solo(g, n=150):
    out = []
    for s in range(1, 6):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(n): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
for k in range(7):
    g = top[:84] + "q" * k + top[84:]
    _, n = trace(parse(g), 7, 1, cap=20000)
    print(f"k={k} len {len(g)} len mod 3 {len(g) % 3} gestation steps {n} solo pop@150 {solo(g):.1f}", flush=True)
