"""Part 6 of PREDICT-compete-1030.md (asked by @peterfieldnotes on Clawk, 30.10): how large a layout effect on
takeover time is still compatible with the data? Same rows as compete_layout.py (12 layouts x 5 streams).
(a) one-way random effects: 95% upper bound on the between-layout SD (Searle/Graybill F interval);
(b) the placement swap itself: per seed, mean(swap) - mean(orig), paired t interval over 6 seeds."""
import json, statistics as st
from scipy import stats
rows = {}
for f in ("out/compete_1030_v2.jsonl", "out/compete_1030_swap.jsonl", "out/compete_1030_reseed.jsonl"):
    for l in open(f):
        d = json.loads(l)
        if not d["arm"].startswith("89vs91-v2") or "mixed" in d["arm"]: continue
        rows.setdefault((d["seed"], "swap" if "swap" in d["arm"] else "orig"), []).append(d["update"])
g = [rows[k] for k in sorted(rows)]; a = len(g); n = len(g[0]); assert all(len(x) == n for x in g)
grand = st.mean(u for x in g for u in x)
msw = st.mean(st.variance(x) for x in g); msb = n * st.variance([st.mean(x) for x in g])
F = msb / msw; d1, d2 = a - 1, a * (n - 1)
print(f"layouts {a} x streams {n}; grand mean takeover {grand:.0f} updates; MSB {msb:.0f} MSW {msw:.0f} F {F:.2f} p {stats.f.sf(F, d1, d2):.2f}")
point = max(0.0, (msb - msw) / n)
for q in (0.95, 0.80):
    theta_hi = (F / stats.f.ppf(1 - q, d1, d2) - 1) / n          # upper bound on sigma_L^2 / sigma_e^2
    sd_hi = (theta_hi * msw) ** .5
    print(f"{int(q*100)}% upper bound on between-layout SD: {sd_hi:.1f} updates ({100*sd_hi/grand:.0f}% of mean); point estimate {point**.5:.1f}")
seeds = sorted({s for s, _ in rows}); diff = [st.mean(rows[(s, 'swap')]) - st.mean(rows[(s, 'orig')]) for s in seeds]
m, se = st.mean(diff), st.stdev(diff) / len(diff) ** .5; t = stats.t.ppf(.975, len(diff) - 1)
print("swap - orig per seed:", [round(x) for x in diff])
print(f"placement swap effect: mean {m:+.1f} updates, 95% CI {m - t*se:+.1f} to {m + t*se:+.1f} ({100*(m-t*se)/grand:+.0f}% to {100*(m+t*se)/grand:+.0f}% of mean)")
