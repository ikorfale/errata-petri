"""E1 L50 interval (Fable 23.10: the fit gives only a point). Seed-cluster bootstrap: resample the 14 seeds with
replacement, keep each seed's 9 arms together, refit. Post-hoc, descriptive; the verdict stays e1_verdict.py's."""
import random, sys
from e1_verdict import load, fit, EST
warm, worlds = load(sys.argv[1:3])
by = {}
for w in worlds:
    y = {'established': 1, 'extinct': 0}.get(w['outcome'])
    if y is not None: by.setdefault(w['seed'], []).append((w['L'], y))
seeds = sorted(by); rng = random.Random(20261023); out = []
for _ in range(2000):
    xs, ys = [], []
    for s in (rng.choice(seeds) for _ in seeds):
        for L, y in by[s]: xs.append(L); ys.append(y)
    r = fit(xs, ys)
    if r: out.append(-r[0] / r[1])
out.sort(); n = len(out)
print(f"bootstrap fits {n}/2000 (rest separated); L50 2.5% {out[int(.025*n)]:.2f}  median {out[n//2]:.2f}  97.5% {out[int(.975*n)]:.2f}")
