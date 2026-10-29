"""glitchfox 107528 (design effect): how clustered are the merit2 baseline births? Single-linkage clusters of parent
genomes at Levenshtein distance <= K; then the neutral-vs-worse second-census split with one random birth per cluster
(50 draws). Run with ~/venv/bin/python (rapidfuzz). Written 29.10 by date -u 11:18 UTC."""
import json, sys, random, numpy as np
from rapidfuzz.process import cdist
from rapidfuzz.distance import Levenshtein
from scipy.stats import fisher_exact
src = open('merit_survival.py').read().split('d = json.load(open(sys.argv[1]))')[0]; exec(src)
d = json.load(open(sys.argv[1])); rows = []
for x in d['baseline_census_reaching']:
    p = rate(x['parent_genome']); c = rate(x['genome'])
    if not p: continue
    rows.append((c / p >= .95, x['born'] + x['life'] >= x['next_census'] + daily.SAMPLE, ''.join(chr(65 + v) for v in x['parent_genome'])))
S = [r[2] for r in rows]; D = cdist(S, S, scorer=Levenshtein.distance, workers=1)
print(f"births {len(rows)}; parent genome length median {int(np.median([len(s) for s in S]))}")
for K in (0, 2, 5, 10, 20):
    lab = list(range(len(S)))
    def f(i):
        while lab[i] != i: lab[i] = lab[lab[i]]; i = lab[i]
        return i
    for i, j in zip(*np.nonzero(np.triu(D <= K, 1))): lab[f(i)] = f(j)
    cl = {}
    for i in range(len(S)): cl.setdefault(f(i), []).append(i)
    rng = random.Random(K); ps, tabs = [], []
    for _ in range(50):
        pick = [rows[rng.choice(m)] for m in cl.values()]
        t = [[sum(r[1] for r in pick if r[0]), sum(not r[1] for r in pick if r[0])], [sum(r[1] for r in pick if not r[0]), sum(not r[1] for r in pick if not r[0])]]
        tabs.append(t); ps.append(fisher_exact(t)[1])
    t = tabs[0]; sz = sorted((len(m) for m in cl.values()), reverse=True)
    print(f"K={K}: clusters {len(cl)} (largest {sz[:5]}); one birth per cluster, draw 1: neutral {t[0][0]}/{t[0][0]+t[0][1]}, worse {t[1][0]}/{t[1][0]+t[1][1]}; "
          f"Fisher p median over 50 draws {np.median(ps):.2g}, max {max(ps):.2g}")
