"""Order-statistic check (theone, board 100496): upper index int(.975n) vs int(.975n)-1 as in e2_verdict.py. E1 bootstrap without silent exclusions (zenith, board 100298). Same 2000 seed-cluster resamples as e1_bootstrap.py
(rng 20261023, same draw order). Three readings, all post-hoc and descriptive; the E1 verdict stays e1_verdict.py's:
  fit-only   : resamples where the MLE exists (the published 25.4-28.0, separated ones dropped)
  midpoint   : separated resamples get the midpoint of their gap (largest established L, smallest extinct L);
               quasi-separated ones get the interpolated share-0.5 crossing (e2_verdict.l50 rules); all 2000 kept
  E2 rule    : each resample's L50 interval, 2.5% of lows to 97.5% of highs (the rule PREREG-E2 applies to E2)"""
import random, sys
from collections import Counter
from e1_verdict import load, fit
from e2_verdict import l50
warm, worlds = load(sys.argv[1:3])
by = {}
for w in worlds:
    by.setdefault(w['seed'], []).append((w['L'], w['outcome']))
seeds = sorted(by); rng = random.Random(20261023)
fitonly, mid, lo, hi, kinds = [], [], [], [], Counter()
for _ in range(2000):
    pick = [rng.choice(seeds) for _ in seeds]
    ws = [x for s in pick for x in by[s]]
    xy = [(L, 1 if o == 'established' else 0) for L, o in ws if o != 'unresolved']
    r = fit([x for x, _ in xy], [y for _, y in xy])
    if r: fitonly.append(-r[0] / r[1])
    iv, note = l50(ws)
    kinds[note.split(' a=')[0]] += 1
    if iv is None: print('resample with no L50:', note); continue
    mid.append((iv[0] + iv[1]) / 2); lo.append(iv[0]); hi.append(iv[1])
def q(v, p, off=0): v = sorted(v); return v[min(len(v) - 1, int(p * len(v)) + off)]
print('resample kinds:', dict(kinds))
print(f'fit-only  n={len(fitonly)}  2.5% {q(fitonly,.025):.2f}  median {q(fitonly,.5):.2f}  97.5% {q(fitonly,.975):.2f}')
print(f'midpoint  n={len(mid)}  2.5% {q(mid,.025):.2f}  median {q(mid,.5):.2f}  97.5% {q(mid,.975):.2f}')
print(f'E2 rule   n={len(lo)}  lows 2.5% {q(lo,.025):.2f}  highs 97.5% {q(hi,.975):.2f}')
sepmid = [(a + b) / 2 for a, b in zip(lo, hi) if a != b]
print('separated-resample midpoints:', dict(sorted(Counter(sepmid).items())))
print('upper order statistics, index 1950 (this script) vs 1949 (e2_verdict):')
print(f'  fit-only n={len(fitonly)} idx {int(.975*len(fitonly))}: {q(fitonly,.975):.4f}  idx-1: {q(fitonly,.975,-1):.4f}')
print(f'  midpoint   idx 1950: {q(mid,.975):.4f}  1949: {q(mid,.975,-1):.4f}')
print(f'  E2 highs   idx 1950: {q(hi,.975):.4f}  1949: {q(hi,.975,-1):.4f}')
print(f'  lows 2.5%  idx 50: {q(lo,.025):.4f}  49: {q(lo,.025,-1):.4f}')
