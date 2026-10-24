"""#491 truth runner: the real first division outcome of a genome, mutation and indels off, world seed given.
Runs until a birth or ncopy > 10*L (the predictor's horizon); a step cap of 400*L that binds first is 'unresolved'.
Classes: exact j | exact-offlap ncopy | rotated ncopy (child a true rotation of the parent) | other-birth len |
never (ncopy passed 10*L with no birth) | unresolved."""
import sys
sys.path.insert(0, ".")
from petri import World
def truth(g, seed=7, laps=10):
    g = list(g); L = len(g)
    w = World(side=5, seed=seed, copy_mut=0.0); w.indel = 0.0; w.inject(g, "t", cell=0); o = w.cells[0]
    for _ in range(400 * L):
        if o.ncopy > laps * L: return ("never", "no birth within 10 laps")
        b = w.births; nc = o.ncopy
        w.step(o, 0)
        if w.births > b:
            kid = [c for c in w.cells if c is not None and c is not o]
            ch = list(kid[0].mem[:kid[0].glen]) if kid else []
            if ch == g: return ("exact", nc // L) if nc % L == 0 else ("exact-offlap", nc)
            if len(ch) == L and any(ch == g[q:] + g[:q] for q in range(1, L)): return ("rotated", nc)
            return ("other-birth", len(ch))
        o = w.cells[0]
    return ("unresolved", "step cap")
