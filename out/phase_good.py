"""Why do 46 faithful AND+ANDN genomes of length 96 divide fast, when the parent's phase rule (e = 2) says length 96
never divides? Insert k no-op 'q' at the parent's site 84 (85 when the edits insert a letter before it, else 84; Fable review 24.10) for k = 0..5 and trace gestation.
If gestation is fast at k = 0 and k = 3 and never/slow elsewhere, the edit shifted e to 0."""
import sys, json
sys.path.insert(0, "."); sys.path.insert(0, "out")
from genome_trace import trace
from petri import parse
from two_step_check import edit, top, blk
for p, e1, e2, site in [(39, "sub 21 h", "ins 31 z", 85), (39, "sub 21 h", "ins 10 n", 85), (47, "sub 28 c", "sub 45 f", 84)]:
    g = edit(edit(top[:p] + blk + top[p + 12:], e1), e2)
    for k in range(6):
        x = g[:site] + "q" * k + g[site:]
        _, n = trace(parse(x), 7, 1, cap=20000)
        print(p, e1, e2, "k", k, "len", len(x), "mod3", len(x) % 3, "steps", n, flush=True)
