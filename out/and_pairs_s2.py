"""Fable 23.10: is the AND+ANDN genotype two steps from the s2 dominant? Every pair of insertions in the tail
(positions 66-91 of the parent, 26 letters each), one gestation traced (genome_trace, seed 7). Prints every
pair whose task set holds both AND and ANDN, and a count of task sets."""
import json, string, collections, sys
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
D = json.load(open("out/s2_dump.json"))
top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase
def tasks(g):
    try:
        log, _ = trace(parse(g), 7, 1)
    except Exception:
        return ("ERR",)
    return tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()
P = range(66, 92); cnt = collections.Counter(); hits = 0; n = 0
for i in P:
    for a in AL:
        g1 = top[:i] + a + top[i:]
        for j in range(i, 93):                  # second insertion at or after the first, in g1 coordinates
            for b in AL:
                g = g1[:j + 1] + b + g1[j + 1:]
                t = tasks(g); n += 1; cnt[t] += 1
                if "AND" in t and "ANDN" in t:
                    hits += 1; print("BOTH", i, a, j + 1, b, t, g, flush=True)
print(f"{n} double insertions; with AND and ANDN: {hits}; task sets: {cnt.most_common(10)}", flush=True)
