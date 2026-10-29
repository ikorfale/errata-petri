"""glitchfox 107595: are the merit2 baseline births clustered above the parent? Per class (neutral >=0.95, worse <0.95 >0,
sterile 0; same assay as merit_survival.py), distinct parent and grandparent individuals and genotypes, the largest
grandparent groups, and the second-census split with one random birth per grandparent individual (50 draws).
Needs the rerun with grandparent ids (replay_origins.py, 29.10). Written 29.10 12:05 UTC (date -u).
Usage: python3 merit2_grandparents.py out/origin_genomes_day2_gp.json"""
import json, sys, random
from collections import Counter
from scipy.stats import fisher_exact
src = open('merit_survival.py').read().split('d = json.load(open(sys.argv[1]))')[0]; exec(src)
d = json.load(open(sys.argv[1])); cls = {'neutral': [], 'worse': [], 'sterile': []}
for x in d['baseline_census_reaching']:
    p = rate(x['parent_genome']); c = rate(x['genome'])
    if not p: continue
    k = 'neutral' if c / p >= .95 else ('sterile' if c == 0 else 'worse')
    cls[k].append((x['parent'], x['grandparent'], tuple(x['grandparent_genome'] or ()), x['born'] + x['life'] >= x['next_census'] + daily.SAMPLE))
for k, v in cls.items():
    gi = Counter(r[1] for r in v); gg = Counter(r[2] for r in v)
    print(f"{k}: births {len(v)}, reach 2nd census {sum(r[3] for r in v)}; distinct parents {len({r[0] for r in v})}, "
          f"grandparent individuals {len(gi)} (largest {[n for _, n in gi.most_common(3)]}), genotypes {len(gg)} (largest {[n for _, n in gg.most_common(3)]})")
allr = [(k, r) for k, v in cls.items() for r in v]; gi = Counter(r[1] for _, r in allr)
print(f"all classes: {len(allr)} births, {len(gi)} grandparent individuals; shared across classes: "
      f"{sum(1 for g in gi if len({k for k, r in allr if r[1] == g}) > 1)}")
grp = {}
for k, r in allr:
    if k != 'sterile': grp.setdefault(r[1], []).append((k, r))
rng = random.Random(1029); ps = []
for i in range(50):
    pick = [rng.choice(m) for m in grp.values()]
    t = [[sum(r[3] for k, r in pick if k == c), sum(not r[3] for k, r in pick if k == c)] for c in ('neutral', 'worse')]
    ps.append(fisher_exact(t)[1])
    if i == 0: print(f"one birth per grandparent ({len(grp)} groups), draw 1: neutral {t[0][0]}/{sum(t[0])}, worse {t[1][0]}/{sum(t[1])}")
print(f"Fisher p over 50 draws: median {sorted(ps)[25]:.2g}, max {max(ps):.2g}")
