"""Import-safe copy of mm_ex_verdict.py functions (generated 31.10 for shuffle_dx_null.py; scoring stays in mm_ex_verdict.py)."""
"""Verdict for PREDICT-merit-ex-1030.md: primary C = dE - dX (exact two-sided sign-flip), secondary Spearman dU vs dX
(exact cutoff 107/165 at n = 10), fixed sequence. Usage: python3 mm_ex_verdict.py 23 24 ... 32"""
import json, sys
from fractions import Fraction
from itertools import product
def UG(m, s):
    r = json.load(open(f"out/mm_{m}_{s}.json"))["rows"]
    last = [x for x in r if 76000 <= x["update"] <= 80000]
    assert len(last) == 5 and last[-1]["update"] == 80000, (m, s, [x["update"] for x in last])
    return sum(x["unexec_mean"] for x in last) / 5, last[-1]["glen_mean"]
def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = Fraction(i + j + 2, 2)
        i = j + 1
    return r, len(set(v)) < len(v)
def spearman(x, y):
    (ra, ta), (rb, tb) = ranks(x), ranks(y); n = len(x)
    return 1 - Fraction(6) * sum((a - b) ** 2 for a, b in zip(ra, rb)) / (n * (n * n - 1)), (ta, tb)
def signflip(C):
    obs = abs(sum(C))
    return Fraction(sum(abs(sum(c * f for c, f in zip(C, fl))) >= obs - 1e-12 for fl in product((1, -1), repeat=len(C))), 2 ** len(C))
# Observed-side fixtures through the same code that scores the data (glitchfox 108919, zenith 108915; amendment 30.10 16:36):
# table checks cannot see an orientation or shift bug in the cost, these can.
I = list(range(10))
assert spearman(I, I)[0] == 1                                   # identity: D = 0
assert spearman(I, I[::-1])[0] == -1                            # reversal: D = n(n^2-1)/3 = 330
assert spearman(I, [1, 0, 2, 3, 4, 5, 6, 7, 9, 8])[0] == Fraction(161, 165)   # two adjacent swaps: D = 4
assert spearman(I, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8])[0] == Fraction(163, 165)   # one swap: D = 2
assert spearman([5, 1, 9], [50, 10, 90])[0] == 1                # ranks, not values; order-preserving map
assert spearman([x * 1.0 for x in I], [-x for x in I])[0] == -1  # sign of dX enters as is
assert signflip([1.0] * 10) == Fraction(2, 1024) and signflip([1.0] * 9 + [-1.0]) == Fraction(22, 1024)
assert spearman(I, [2, 8, 9, 7, 6, 5, 4, 3, 1, 0])[0] == -Fraction(107, 165)  # D = 272: exactly on the bar, which passes (<=)
# Amendment 30.10 17:40 (zenith 108939, glitchfox 108936; 8/20 arms finished, none opened): signflip sums values, not
# signs, two-sided on |sum|; and S is scored on the integer D (rho <= -107/165 <=> D >= 272 at n = 10, no ties), so a
# float rho one ulp off the bar cannot flip the decision. rho stays for display.
assert signflip([2.0, 3, 4, 5, 6, 7, 8, 9, 10, -1]) == Fraction(4, 1024)   # sign test would give 22
assert signflip([1.0, 2, 3, 4, 5, 6, 7, 8, 9, -10]) == Fraction(86, 1024)  # sign test would give 22
def Dint(rho, n): return (1 - rho) * n * (n * n - 1) / 6
assert Dint(spearman(I, [2, 8, 9, 7, 6, 5, 4, 3, 1, 0])[0], 10) == 272 and Dint(Fraction(-1), 10) == 330
