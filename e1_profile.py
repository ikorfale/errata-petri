"""E1 L50 profile-likelihood 95% CI (Fable review 23.10 of zenith 100298): logit p = b (L - L50), b profiled out on a
grid of L50; CI = {L50 : 2 (llmax - llprof) <= 3.841}. Ignores seed clustering (the bootstrap covers that). Also checks
seed frailty: are the seeds extinct at L=24 also extinct at L=28?"""
import math, sys
from e1_verdict import load
warm, worlds = load(sys.argv[1:3])
xy = [(w['L'], 1 if w['outcome'] == 'established' else 0) for w in worlds if w['outcome'] != 'unresolved']
def ll(b, m):
    s = 0.0
    for x, y in xy:
        z = b * (x - m); s += -math.log1p(math.exp(-z)) if y else (-math.log1p(math.exp(z)) if z < 30 else -z)
    return s
def prof(m):  # maximise over slope b < 0 by golden section on [-20, -1e-4]
    lo, hi = -20.0, -1e-4; g = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        c, d = hi - g * (hi - lo), lo + g * (hi - lo)
        if ll(c, m) > ll(d, m): hi = d
        else: lo = c
    return ll((lo + hi) / 2, m)
grid = [20 + i / 100 for i in range(1501)]
pl = [prof(m) for m in grid]; mx = max(pl); m_hat = grid[pl.index(mx)]
inside = [m for m, v in zip(grid, pl) if 2 * (mx - v) <= 3.841]
print(f'profile max at L50 = {m_hat:.2f}; 95% profile CI {min(inside):.2f} - {max(inside):.2f}')
by = {}
for w in worlds: by.setdefault(w['seed'], {})[w['L']] = w['outcome']
ext24 = [s for s in sorted(by) if by[s].get(24) == 'extinct']
print('seeds extinct at L24:', ext24, '-> their L28:', [by[s].get(28) for s in ext24])
print('seeds established at L28:', [s for s in sorted(by) if by[s].get(28) == 'established'])
