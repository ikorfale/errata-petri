"""Part 5 of PREDICT-compete-1030.md: layout or chance? Reads out/compete_1030_reseed.jsonl (+ v2 and swap runs as reseed 0).
Per (seed, orientation): update to 90% for the original stream and reseeds 1-4. Prints a one-way variance split."""
import json, statistics as st
rows = {}
for f, tag in (("out/compete_1030_v2.jsonl", None), ("out/compete_1030_swap.jsonl", None), ("out/compete_1030_reseed.jsonl", None)):
    for l in open(f):
        d = json.loads(l)
        if not d["arm"].startswith("89vs91-v2") or "mixed" in d["arm"]: continue
        key = (d["seed"], "swap" if "swap" in d["arm"] else "orig")
        rows.setdefault(key, []).append((d.get("reseed", 0), d["update"], d["winner"]))
groups = []
for k in sorted(rows):
    v = sorted(rows[k]); ups = [u for _, u, _ in v]; groups.append(ups)
    print(k[0], k[1].ljust(4), "updates", ups, "mean %.0f" % st.mean(ups), "winners", "".join(w for *_, w in v))
allu = [u for g in groups for u in g]
within = st.mean(st.variance(g) for g in groups)
between = st.variance([st.mean(g) for g in groups])
n = st.mean(len(g) for g in groups)
print(f"layouts {len(groups)}, runs {len(allu)}, B wins {sum(w=='B' for k in rows for *_, w in rows[k])}")
print(f"within-layout SD {within**.5:.1f}; SD of layout means {between**.5:.1f}; expected from chance alone {(within/n)**.5:.1f}")
print(f"F = n*var(means)/mean(within var) = {n*between/within:.2f} (about 1 if layout adds nothing)")
