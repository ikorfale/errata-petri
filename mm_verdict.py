"""Merit method 1 vs 4 verdict over paired seeds (PREDICT-merit-method-1030b.md, D1-D3).
U = mean unexec_mean over rows 76k-80k; G = glen_mean at 80k. Usage: python3 mm_verdict.py 11 12 13 14 15 16"""
import json, sys, math
from scipy import stats
seeds = [int(s) for s in sys.argv[1:]]
def UG(m, s):
    r = json.load(open(f"out/mm_{m}_{s}.json"))["rows"]
    last = [x for x in r if 76000 <= x["update"] <= 80000]
    assert len(last) == 5 and last[-1]["update"] == 80000, (m, s, [x["update"] for x in last])
    return sum(x["unexec_mean"] for x in last) / 5, last[-1]["glen_mean"]
dU, dG, dE, dX = [], [], [], []
print("| seed | U m1 | U m4 | dU | G m1 | G m4 | dG |\n|---|---|---|---|---|---|---|")
for s in seeds:
    (u1, g1), (u4, g4) = UG(1, s), UG(4, s)
    dU.append(u1 - u4); dG.append(g1 - g4)
    dE.append(g4 * (1 - u4) - g1 * (1 - u1)); dX.append(g4 * u4 - g1 * u1)   # m4 - m1 (glitchfox 108519)
    print(f"| {s} | {u1:.3f} | {u4:.3f} | {u1-u4:+.3f} | {g1:.1f} | {g4:.1f} | {g1-g4:+.1f} |")
n = len(seeds)
k = sum(d > 0 for d in dU)
p_sign = sum(math.comb(n, j) for j in range(k, n + 1)) / 2 ** n
print(f"D1 sign: dU>0 in {k}/{n}, one-sided p = {p_sign:.4f}")
for name, d in (("dU", dU), ("dG", dG)):
    m = sum(d) / n; sd = (sum((x - m) ** 2 for x in d) / (n - 1)) ** 0.5; t = stats.t.ppf(0.975, n - 1)
    print(f"D2 {name}: mean {m:+.4f}, sd {sd:.4f}, 95% t interval [{m - t*sd/n**0.5:+.4f}, {m + t*sd/n**0.5:+.4f}]")
r = stats.ttest_1samp(dU, 0, alternative="greater")
print(f"D3 one-sided paired t on dU: t = {r.statistic:.3f}, df {n-1}, p = {r.pvalue:.4f}")
for name, d, want in (("E1 executed units m4-m1", dE, 1), ("E2 unexecuted units m4-m1", dX, -1)):
    k = sum(x * want > 0 for x in d)
    print(f"{name}: {' '.join(f'{x:+.1f}' for x in d)}; in predicted direction {k}/{n}, one-sided p = {sum(math.comb(n, j) for j in range(k, n + 1)) / 2 ** n:.4f}")
k = sum(d < 0 for d in dG)
print(f"G1 sign: dG<0 in {k}/{n}, one-sided p = {sum(math.comb(n, j) for j in range(k, n + 1)) / 2 ** n:.4f} (rule: {n}/{n})")
r = stats.ttest_1samp(dG, 0, alternative="less")
print(f"G2 one-sided paired t on dG (H1 mean < 0): t = {r.statistic:.3f}, df {n-1}, p = {r.pvalue:.4f}")
