"""theone 107640 / glitchfox 107659 / zenith 107668: the "first 400" check over raw baseline index < 400 (not rows[:400]),
with every exclusion printed by raw index and reason (glitchfox's drop-in, same assay as merit_survival.py).
Pass condition stated before the run (zenith 107668): n 398, equal-or-better 176, both exclusions below raw index 400.
Also: does the grandparent rerun (_gp) carry the same baseline births, in the same order, as _r2?
Written 29.10 12:54 UTC (date -u). Usage: python3 raw400_check.py out/origin_genomes_day2_r2.json [out/origin_genomes_day2_gp.json]"""
import json, sys, hashlib
from statistics import median
src = open('merit_survival.py').read().split('d = json.load(open(sys.argv[1]))')[0]; exec(src)
for f in sys.argv[1:]:
    print(f"== {f} sha256 {hashlib.sha256(open(f, 'rb').read()).hexdigest()}")
B = json.load(open(sys.argv[1]))['baseline_census_reaching']
rows, raw400, excl = [], [], []
for i, x in enumerate(B):
    if x['parent_genome'] is None:
        excl.append((i, 'parent None')); continue
    p = rate(x['parent_genome']); c = rate(x['genome'])
    if not p:
        excl.append((i, 'parent rate 0')); continue
    r = (c / p, x['born'] + x['life'] >= x['next_census'] + daily.SAMPLE)
    rows.append(r)
    if i < 400: raw400.append(r[0])
print('raw baseline births:', len(B), '| exclusions (raw index, reason):', excl)
q = sorted(raw400)
print(f"raw-index<400 check: n {len(q)}, median {median(q):.3f}, equal-or-better {sum(v >= .95 for v in q)}, sterile {sum(v == 0 for v in q)}")
if len(sys.argv) > 2:
    G = json.load(open(sys.argv[2]))['baseline_census_reaching']
    key = lambda x: (x['born'], x['genome'], x['parent_genome'], x['life'])
    same = sum(key(a) == key(b) for a, b in zip(B, G))
    print(f"r2 vs gp baseline: {len(B)} vs {len(G)} births, identical (born, genome, parent genome, life) at same index: {same}")
