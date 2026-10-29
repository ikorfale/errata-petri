"""Thread 107757, zenith 107759: of the 58 dual genotypes among the 1,610,525 distinct mutated children of non-AND parents
(seed 101, dual_births_trace_other.json), how many are dual by genotype and divide as duals? Same check as dual_seeds.py:
each genome alone over 100 input seeds (one gestation, cap 20000); counts gestations ending with AND and ANDN, and
gestations that divide. Usage: python3 dual_seeds_other.py > out/dual_seeds_other_s101.txt"""
import json, sys
sys.path[:0] = [".", "out"]
from genome_trace import trace
from petri import parse
D = json.load(open("out/dual_births_trace_other.json"))
for i, h in enumerate(D["hits"]):
    both = div = bothdiv = 0
    for s in range(100):
        log, n = trace(parse(h["genome"]), s, 1, cap=20000)
        tk = set().union(*[set(r[7]) for r in log]) if log else set()
        d = n < 20000; div += d; both += {"AND", "ANDN"} <= tk; bothdiv += d and {"AND", "ANDN"} <= tk
    print(f"{i} births {h['births']} len {len(h['genome'])} mod3 {h['len_mod3']}: AND+ANDN {both}/100, divided {div}/100, "
          f"both and divided {bothdiv}/100", flush=True)
