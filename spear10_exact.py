"""Exact two-sided null of Spearman rho at n = 10 (no ties), all 10! orders, in integers: rho = 1 - 6*d2/990.
Prints the smallest cutoff |rho| = k/165 whose two-sided tail is <= 0.05. Run: python3 spear10_exact.py"""
from itertools import permutations
from collections import Counter
from fractions import Fraction
n = 10; c = Counter()
for p in permutations(range(n)):
    c[sum((i - x) ** 2 for i, x in enumerate(p))] += 1
tot = sum(c.values())
rho = {d: 1 - Fraction(6 * d, n * (n * n - 1)) for d in c}
for r in sorted({abs(v) for v in rho.values()}, reverse=True):
    tail = sum(k for d, k in c.items() if abs(rho[d]) >= r)
    if Fraction(tail, tot) > Fraction(1, 20): break
    best = (r, tail)
print(f'n=10 two-sided 0.05: reject iff |rho| >= {best[0]} = {float(best[0]):.4f}; tail {best[1]}/{tot} = {best[1]/tot:.4f}')
