"""#451 remainder (23.10, after 99592): substitution pairs with the first position in 0-59 (second anywhere after it). Fable 23.10 / zenith 99171: is a dividing AND+ANDN genotype two substitutions from the s2 dominant?
Double insertions in the tail gave AND+ANDN task sets but none divides (out/both_check.txt): length changes stall
division in this genome. Substitutions keep the length. Every pair of substitutions at positions 60-95, one
gestation traced (seed 7); each AND+ANDN hit then gets a solo viability check (20x20, seeds 1-5, pop at 150)."""
import json, string, collections, sys, statistics as st
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, parse
D = json.load(open("out/s2_dump.json"))
top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase
def tasks(g):
    try:
        log, _ = trace(parse(g), 7, 1, cap=3000)
    except Exception:
        return ("ERR",)
    return tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()
def solo(g):
    out = []
    for s in range(1, 6):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(150): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
P = range(0, 60); n = 0; hits = 0; viable = 0; cnt = collections.Counter()
for i in P:
    for a in AL:
        if a == top[i]: continue
        g1 = top[:i] + a + top[i + 1:]
        for j in range(i + 1, len(top)):
            for b in AL:
                if b == top[j]: continue
                g = g1[:j] + b + g1[j + 1:]
                t = tasks(g); n += 1; cnt[len(t)] += 1
                if "AND" in t and "ANDN" in t:
                    hits += 1; p = solo(g); viable += p >= 130
                    print("BOTH", i, a, j, b, t, f"solo {p:.1f}", g, flush=True)
    print(f"# done i={i}: {n} pairs, {hits} AND+ANDN, {viable} of them dividing", flush=True)
print(f"{n} double substitutions; with AND and ANDN: {hits}; dividing (solo pop@150 >= 130): {viable}", flush=True)
