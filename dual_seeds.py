"""PREDICT-dualbirths-1029.md, check: are the 11 in-world AND+ANDN dividers in seed 101 dual by genotype, or did they hit
AND+ANDN on one draw of inputs? Trace each logged genome over 100 input seeds (one gestation, cap 20000) and count the
gestations that end with both AND and ANDN. Usage: python3 dual_seeds.py > out/dual_seeds_s101.txt"""
import json, gzip, sys
sys.path[:0] = [".", "out"]
from genome_trace import trace
from petri import parse
D = json.load(gzip.open("out/dual_births_s101.json.gz", "rt"))
for d in D["duals"]:
    both = div = 0; seen = set()
    for s in range(100):
        log, n = trace(parse(d["genome"]), s, 1, cap=20000)
        tk = set().union(*[set(r[7]) for r in log]) if log else set()
        div += n < 20000; both += {"AND", "ANDN"} <= tk; seen |= tk
    print(f"update {d['update']} len {len(d['genome'])} world tasks {','.join(d['tasks'])}: "
          f"AND+ANDN in {both}/100 seeds, divided in {div}/100, tasks ever {','.join(sorted(seen))}", flush=True)
