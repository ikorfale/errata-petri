"""#484 (zenith 100725): from each one-step dead-code activator that computes AND+ANDN but never divides (56, from
out/dead_region.py), try every further one-step mutant (sub/ins/del). Cap 2000 steps: the world's age limit is
20 x length (~1900), so slower genomes die before dividing anyway. Report mutants keeping AND+ANDN that divide, and fast (<300)."""
import sys, json, string
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
AL = string.ascii_lowercase; blk = "oypcupcncuyq"
def run(g, cap):
    try: log, n = trace(parse(g), 7, 1, cap=cap)
    except Exception: return (), cap
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n
def neigh(g):
    for i in range(len(g) + 1):
        for c in AL:
            yield f"ins {i} {c}", g[:i] + c + g[i:]
            if i < len(g) and c != g[i]: yield f"sub {i} {c}", g[:i] + c + g[i + 1:]
        if i < len(g): yield f"del {i}", g[:i] + g[i + 1:]
starts = []
for p in (31, 35, 39, 43, 47):
    g = top[:p] + blk + top[p + 12:]
    for name, x in neigh(g):
        t, n = run(x, 20000)
        if "AND" in t and "ANDN" in t: starts.append((p, name, x, n))
print("one-step AND+ANDN activators:", len(starts), "dividing:", sum(s[3] < 20000 for s in starts), flush=True)
out = []; tot = 0
for p, name, x, _ in starts:
    hits = []
    for n2, y in neigh(x):
        t, n = run(y, 2000); tot += 1
        if "AND" in t and "ANDN" in t and n < 2000: hits.append((n2, n, len(y)))
    fast = [h for h in hits if h[1] < 300]
    print(f"block {p} {name}: second steps dividing with AND+ANDN {len(hits)}, fast {len(fast)}", sorted(hits, key=lambda h: h[1])[:3], flush=True)
    out.append({"p": p, "first": name, "hits": hits})
print("second-step mutants traced:", tot, "| starts with any dividing AND+ANDN:", sum(bool(o["hits"]) for o in out),
      "| with any fast:", sum(any(h[1] < 300 for h in o["hits"]) for o in out))
json.dump(out, open("out/two_step.json", "w"))
