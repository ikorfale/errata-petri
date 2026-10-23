"""E1 L50 with Firth-penalized logistic regression (exists under separation), point and seed-cluster bootstrap with
all 2000 resamples (same rng and draw order as e1_bootstrap.py). Post-hoc, descriptive (zenith 100298)."""
import math, random, sys
from e1_verdict import load

def firth(xs, ys, iters=200):
    a = b = 0.0
    for _ in range(iters):
        ps = [1 / (1 + math.exp(-(a + b * x))) for x in xs]
        ws = [p * (1 - p) for p in ps]
        h00 = sum(ws); h01 = sum(w * x for w, x in zip(ws, xs)); h11 = sum(w * x * x for w, x in zip(ws, xs))
        det = h00 * h11 - h01 * h01
        i00, i01, i11 = h11 / det, -h01 / det, h00 / det
        hs = [w * (i00 + 2 * i01 * x + i11 * x * x) for w, x in zip(ws, xs)]
        g0 = sum(y - p + h * (.5 - p) for y, p, h in zip(ys, ps, hs))
        g1 = sum((y - p + h * (.5 - p)) * x for y, p, h, x in zip(ys, ps, hs, xs))
        da = i00 * g0 + i01 * g1; db = i01 * g0 + i11 * g1
        s = 1.0
        while max(abs(s * da), abs(s * db)) > 5: s /= 2
        a += s * da; b += s * db
        if abs(da) < 1e-10 and abs(db) < 1e-10: return a, b
    raise RuntimeError('no convergence')

warm, worlds = load(sys.argv[1:3])
xy = [(w['L'], 1 if w['outcome'] == 'established' else 0) for w in worlds if w['outcome'] != 'unresolved']
a, b = firth([x for x, _ in xy], [y for _, y in xy]); print(f'full data Firth L50 = {-a/b:.2f} (a={a:.3f} b={b:.4f})')
by = {}
for w in worlds:
    if w['outcome'] != 'unresolved': by.setdefault(w['seed'], []).append((w['L'], 1 if w['outcome'] == 'established' else 0))
seeds = sorted(by); rng = random.Random(20261023); out = []
for _ in range(2000):
    pts = [p for s in [rng.choice(seeds) for _ in seeds] for p in by[s]]
    a, b = firth([x for x, _ in pts], [y for _, y in pts]); out.append(-a / b)
out.sort(); n = len(out)
print(f'Firth bootstrap n={n}: 2.5% {out[int(.025*n)]:.2f}  median {out[n//2]:.2f}  97.5% {out[int(.975*n)]:.2f}  share>28 {sum(v>28 for v in out)/n:.4f}')
