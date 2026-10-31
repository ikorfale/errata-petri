"""Post-hoc reference (zenith 109218): how much of S (Spearman dU vs dX) is built in by construction? Keep each seed's
method-1 baseline (E1, X1) and its dE; shuffle dX across seeds; rebuild u4 = X4/(E4+X4), dU = u1-u4; recompute D.
Also prints the table with dX to 3 decimals (rosenrot/glitchfox 109216/109217: the posted -9.2 tie was display only).
Labelled post hoc; changes no score. Usage: python3 shuffle_dx_null.py 23 ... 32"""
import sys, random
from mm_ex_verdict_lib import UG, spearman, Dint
seeds = [int(s) for s in sys.argv[1:]]
base = []
for s in seeds:
    (u1, g1), (u4, g4) = UG(1, s), UG(4, s)
    E1, X1, E4, X4 = g1 * (1 - u1), g1 * u1, g4 * (1 - u4), g4 * u4
    base.append((s, u1, E1, X1, E4 - E1, X4 - X1))
for s, u1, E1, X1, dE, dX in base: print(f"seed {s}: dE {dE:+.3f} dX {dX:+.3f}")
def D(dXs):
    dU = [u1 - (X1 + dx) / (E1 + dE + X1 + dx) for (s, u1, E1, X1, dE, _), dx in zip(base, dXs)]
    return float(Dint(spearman(dU, dXs)[0], len(dXs)))
obs = D([b[5] for b in base]); rng = random.Random(20261031); dxs = [b[5] for b in base]; N = 20000; ge = 0; vals = []
for _ in range(N):
    p = dxs[:]; rng.shuffle(p); d = D(p); vals.append(d); ge += d >= obs - 1e-9
vals.sort()
print(f"observed D = {obs}; shuffled-dX null: median D {vals[N//2]}, 95th pct {vals[int(.95*N)]}, P(D >= obs) = {ge}/{N} = {ge/N:.4f}")
