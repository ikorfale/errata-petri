# zenith 99171: list every one-step mutant (substitution, insertion, deletion) of the s2 dominant genotype that
# computes AND in one gestation, and which tasks it keeps. Same tracer as genome_trace (mutation off, seed 7).
import json, string, collections
from genome_trace import trace
from petri import parse

d = json.load(open("out/s2_dump.json"))
top = max(d["genotypes"], key=lambda g: g["n"])["genome"]
AL = sorted(set(string.ascii_lowercase))


def tasks(gen):
    try:
        log, _ = trace(parse(gen), 7, 1)
    except Exception as e:
        return ("ERR",)
    return tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()  # tasks reset at division: union over the gestation


base = tasks(top)
print("dominant tasks", base, "len", len(top))
muts = []
for i in range(len(top)):
    muts.append((f"del {i}", top[:i] + top[i + 1:]))
    for c in AL:
        if c != top[i]:
            muts.append((f"sub {i} {top[i]}>{c}", top[:i] + c + top[i + 1:]))
for i in range(len(top) + 1):
    for c in AL:
        muts.append((f"ins {i} {c}", top[:i] + c + top[i:]))
cnt = collections.Counter()
hits = []
for name, g in muts:
    t = tasks(g)
    cnt[t] += 1
    if "AND" in t:
        hits.append((name, t, g))
print(f"{len(muts)} one-step mutants; task sets: {cnt.most_common(8)}")
print(f"computing AND: {len(hits)}; of them also ANDN: {sum('ANDN' in t for _, t, _ in hits)}")
for name, t, g in hits:
    print(" ", name, t)
json.dump([{"edit": n, "tasks": t, "genome": g} for n, t, g in hits], open("out/and_mutants_s2.json", "w"), indent=0)
