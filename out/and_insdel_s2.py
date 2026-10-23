"""#451 (Fable review 23.10, posted prediction in 99590): length-preserving two-edit class, one insertion plus one
deletion anywhere in the s2 dominant (95 letters). The mod-3 copy loop makes ins+ins, del+del and sub+indel pairs nulls
by construction; this class is not. Prediction written before the run: at least one ins+del genome credits AND and ANDN
and divides (solo pop@150 >= 130, 5 seeds, mutation off). Distinct genomes only (dedup), one gestation traced, seed 7."""
import collections, json, string, sys, statistics as st
sys.path.insert(0, ".")
from genome_trace import trace
from petri import World, parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase
def tasks(g):
    try: log, _ = trace(parse(g), 7, 1, cap=3000)
    except Exception: return ("ERR",)
    return tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()
def solo(g):
    out = []
    for s in range(1, 6):
        w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
        w.inject(parse(g), "x", cell=0)
        for u in range(150): w.run_update()
        out.append(sum(o is not None for o in w.cells))
    return st.mean(out)
seen = set(); n = hits = viable = 0; cnt = collections.Counter()
for i in range(len(top) + 1):
    for a in AL:
        g1 = top[:i] + a + top[i:]
        for j in range(len(g1)):
            g = g1[:j] + g1[j + 1:]
            if g == top or g in seen: continue
            seen.add(g); n += 1
            t = tasks(g); cnt[len(t)] += 1
            if "AND" in t and "ANDN" in t:
                hits += 1; p = solo(g); viable += p >= 130
                print("BOTH", "ins", i, a, "del", j, t, f"solo {p:.1f}", g, flush=True)
    print(f"# done i={i}: {n} distinct, {hits} AND+ANDN, {viable} dividing", flush=True)
print(f"{n} distinct ins+del genomes; AND+ANDN {hits}; dividing (solo pop@150 >= 130) {viable}; task-count histogram {dict(cnt)}", flush=True)
