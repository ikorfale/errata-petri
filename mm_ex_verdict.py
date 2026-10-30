"""Verdict for PREDICT-merit-ex-1030.md: primary C = dE - dX (exact two-sided sign-flip), secondary Spearman dU vs dX
(exact cutoff 107/165 at n = 10), fixed sequence. Usage: python3 mm_ex_verdict.py 23 24 ... 32"""
import json, sys
from fractions import Fraction
from itertools import product
seeds = [int(s) for s in sys.argv[1:]]
assert len(seeds) == len(set(seeds)), "duplicate seed id"
def UG(m, s):
    r = json.load(open(f"out/mm_{m}_{s}.json"))["rows"]
    last = [x for x in r if 76000 <= x["update"] <= 80000]
    assert len(last) == 5 and last[-1]["update"] == 80000, (m, s, [x["update"] for x in last])
    return sum(x["unexec_mean"] for x in last) / 5, last[-1]["glen_mean"]
rows = []
for s in seeds:
    (u1, g1), (u4, g4) = UG(1, s), UG(4, s)
    dU, dG = u1 - u4, g1 - g4
    dE, dX = g4 * (1 - u4) - g1 * (1 - u1), g4 * u4 - g1 * u1
    assert abs(dE + dX + dG) < 1e-9, s
    rows.append((s, dU, dG, dE, dX, dE - dX))
print("| seed | dU | dG | dE | dX | C = dE-dX |\n|---|---|---|---|---|---|")
for s, dU, dG, dE, dX, C in rows: print(f"| {s} | {dU:+.3f} | {dG:+.1f} | {dE:+.1f} | {dX:+.1f} | {C:+.1f} |")
n = len(rows); C = [r[5] for r in rows]; obs = abs(sum(C))
ext = sum(abs(sum(c * f for c, f in zip(C, fl))) >= obs - 1e-12 for fl in product((1, -1), repeat=n))
p = Fraction(ext, 2 ** n); P = p <= Fraction(1, 20) and sum(C) > 0
print(f"P: mean C {sum(C)/n:+.2f}, positive in {sum(c > 0 for c in C)}/{n}, exact two-sided sign-flip p = {ext}/{2**n} = {float(p):.4f} -> {'PASS' if P else 'FAIL'}")
def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = Fraction(i + j + 2, 2)
        i = j + 1
    return r, len(set(v)) < len(v)
ra, ta = ranks([r[1] for r in rows]); rb, tb = ranks([r[4] for r in rows])
d2 = sum((a - b) ** 2 for a, b in zip(ra, rb)); rho = 1 - Fraction(6) * d2 / (n * (n * n - 1))
cut = Fraction(107, 165)
if not P: print("S: not read (primary failed; fixed sequence)")
else:
    print(f"S: Spearman dU vs dX rho = {rho} = {float(rho):+.4f}{' (ties: average ranks, cutoff approximate)' if ta or tb else ''}; "
          f"cutoff -{cut} -> {'PASS' if n == 10 and rho <= -cut else 'FAIL'}")
k = sum(r[1] > 0 for r in rows); dG = [r[2] for r in rows]; m = sum(dG) / n
sd = (sum((x - m) ** 2 for x in dG) / (n - 1)) ** 0.5
t = {5: 2.5706, 9: 2.2622}[n - 1]  # t 0.975 quantiles
print(f"side: dU > 0 in {k}/{n}; dG mean {m:+.2f}, 95% t [{m - t*sd/n**0.5:+.2f}, {m + t*sd/n**0.5:+.2f}]")
