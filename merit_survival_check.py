"""Check on merit_survival.py (0/520 worse lines at second census looked too clean, 29.10 11:50): ratio histogram of the
worse class, and how far past their next census each class's lineage lived (born + life - next_census)."""
import json, sys
src = open('merit_survival.py').read().split('d = json.load(open(sys.argv[1]))')[0]; exec(src)
import daily
from statistics import median
d = json.load(open(sys.argv[1])); rows = []
for x in d['baseline_census_reaching']:
    p = rate(x['parent_genome']); c = rate(x['genome'])
    if not p: continue
    rows.append((c / p, x['born'] + x['life'] - x['next_census']))
for lo, hi in ((0, 1e-9), (1e-9, .5), (.5, .51), (.51, .8), (.8, .95), (.95, 1.05), (1.05, 99)):
    s = [m for r, m in rows if lo <= r < hi]
    if s: print(f"ratio [{lo:.2f},{hi:.2f}): n {len(s)}, margin past next census median {median(s)}, max {max(s)}, >= {daily.SAMPLE}: {sum(m >= daily.SAMPLE for m in s)}")
