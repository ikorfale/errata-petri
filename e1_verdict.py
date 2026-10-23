"""E1 verdict, mechanical (PREREG-E1.md, commit 9625b47). Written before either lab job finished.
usage: python3 e1_verdict.py out/e1_a.jsonl out/e1_b.jsonl  [--expect-seeds 14]

Per world at +3000: established = infected >= 45, extinct = 0 infected (the sweep stops early at 0),
otherwise unresolved (reported, excluded from the fit).
L50: maximum-likelihood logistic fit of established (1) vs extinct (0) on L.
Not in the preregistration, decided here before seeing data: under complete or quasi-complete separation
the MLE does not exist; then L50 is reported as the interval between the largest L with any established world
and the smallest L above it with no established world, and a band "contains" L50 only if it contains that whole interval.
Null "flat": likelihood-ratio test of the slope, p > 0.05. Null "non-monotone": more than one inversion
(established share rising from one arm to the next larger L) among arms with at least one resolved world.
"""
import json, math, sys
from collections import defaultdict

UPD, EST, CELLS = 3000, 45, 900
BANDS = {"A": (21, 28), "B": (32, 40), "C": (-math.inf, 22)}


def load(paths):
    warm, worlds = {}, []
    for p in paths:
        for line in open(p):
            r = json.loads(line)
            if "warm" in r:
                warm[r["warm"]["seed"]] = r["warm"]; continue
            last = r["census"][-1] if r["census"] else None
            inf = last["inf"] if last else None
            if inf == 0:
                out = "extinct"
            elif last and last["u"] - r["census"][0]["u"] + 250 == UPD and inf >= EST:
                out = "established"
            else:
                out = "unresolved"
            lens = sorted({len(g) for g, _ in r["end_genomes"]})
            worlds.append({"seed": r["seed"], "L": r["L"], "inf": inf, "u_last": last["u"] if last else None,
                           "outcome": out, "end_lens": lens, "injections": r["injections"]})
    return warm, worlds


def loglik(a, b, xs, ys):
    s = 0.0
    for x, y in zip(xs, ys):
        z = a + b * x
        s += -math.log1p(math.exp(-z)) if y else -math.log1p(math.exp(z)) if z < 30 else -z
    return s


def fit(xs, ys, iters=100):
    """Newton-Raphson on (a, b); returns None if it does not converge (separation)."""
    a, b = 0.0, 0.0
    for _ in range(iters):
        g0 = g1 = h00 = h01 = h11 = 0.0
        for x, y in zip(xs, ys):
            p = 1 / (1 + math.exp(-(a + b * x)))
            g0 += y - p; g1 += (y - p) * x
            w = p * (1 - p); h00 += w; h01 += w * x; h11 += w * x * x
        det = h00 * h11 - h01 * h01
        if det < 1e-12:
            return None
        da = (h11 * g0 - h01 * g1) / det; db = (h00 * g1 - h01 * g0) / det
        a += da; b += db
        if abs(da) < 1e-10 and abs(db) < 1e-10:
            return (a, b) if abs(b) < 50 else None
    return None


def separated(xs, ys):
    est = [x for x, y in zip(xs, ys) if y]; ext = [x for x, y in zip(xs, ys) if not y]
    return not est or not ext or max(est) <= min(ext) or min(est) >= max(ext)


def verdict(warm, worlds, expect_seeds=14):
    by = defaultdict(list)
    for w in worlds:
        by[w["L"]].append(w)
    lines, Ls = [], sorted(by)
    lines.append(f"worlds: {len(worlds)} (expected {expect_seeds * 9}); seeds with warm-up rows: {len(warm)}")
    for s in sorted(warm):
        h = warm[s]
        lines.append(f"  warm seed {s}: h_occupied {h['h_occupied']}  merit median/mean {h['merit_median_over_mean']}")
    lines.append("L   est  ext  unres  share_est  (unresolved: seed:infected@update)")
    shares = []
    for L in Ls:
        c = {k: sum(w["outcome"] == k for w in by[L]) for k in ("established", "extinct", "unresolved")}
        res = c["established"] + c["extinct"]
        sh = c["established"] / res if res else None
        shares.append((L, sh))
        un = " ".join(f"{w['seed']}:{w['inf']}@{w['u_last']}" for w in by[L] if w["outcome"] == "unresolved")
        lines.append(f"{L:<3} {c['established']:>4} {c['extinct']:>4} {c['unresolved']:>6}  "
                     f"{'-' if sh is None else f'{sh:.3f}':>9}  {un}")
    bad = [(w["seed"], w["L"], w["end_lens"]) for w in worlds if w["end_lens"] and set(w["end_lens"]) != {w["L"]}]
    lines.append(f"parasite genome length changed in {len(bad)} worlds (top-5 end genomes checked)"
                 + (f": {bad[:10]}" if bad else ""))

    xs = [w["L"] for w in worlds if w["outcome"] != "unresolved"]
    ys = [1 if w["outcome"] == "established" else 0 for w in worlds if w["outcome"] != "unresolved"]
    est_L = [x for x, y in zip(xs, ys) if y]
    if not est_L or all(ys):
        lines.append("L50: no established worlds" if not est_L else "L50: no extinct worlds")
        interval = None
    elif separated(xs, ys) and min(est_L) >= max(x for x, y in zip(xs, ys) if not y) and max(est_L) > min(est_L + xs):
        interval = None
        lines.append("L50: reversed separation (established only at the longer L): no L50, contradicts every model")
    elif separated(xs, ys):
        lo = max(est_L); above = [L for L in Ls if L > lo]
        interval = (lo, above[0] if above else math.inf)
        lines.append(f"L50: complete separation, no MLE; L50 in ({interval[0]}, {interval[1]}]")
    else:
        ab = fit(xs, ys)
        if ab is None:
            lo = max(est_L); interval = (lo, min([L for L in Ls if L > lo] or [math.inf]))
            lines.append(f"L50: fit did not converge (quasi-separation); L50 in ({interval[0]}, {interval[1]}]")
        else:
            a, b = ab; l50 = -a / b; interval = (l50, l50)
            p1 = sum(ys) / len(ys)
            ll0 = sum(math.log(p1) if y else math.log(1 - p1) for y in ys)
            lr = 2 * (loglik(a, b, xs, ys) - ll0)
            p = math.erfc(math.sqrt(max(lr, 0) / 2))          # chi-square, 1 df
            lines.append(f"L50 = {l50:.2f} (logistic a={a:.3f} b={b:.4f}; LR slope test chi2={lr:.2f}, p={p:.2g})")
            if p > 0.05:
                lines.append("NULL (flat): slope not distinguishable from 0 at p>0.05")

    inv = sum(1 for (_, s1), (_, s2) in zip([s for s in shares if s[1] is not None], [s for s in shares if s[1] is not None][1:]) if s2 > s1)
    lines.append(f"inversions (share rising with L): {inv}" + ("  -> NULL (non-monotone)" if inv > 1 else ""))

    if interval:
        lo, hi = interval
        hits = [k for k, (a, b) in BANDS.items() if a <= lo and hi <= b]
        lines.append("band containing L50: " + (", ".join(hits) if hits else
                     "none (28-32, above 40, or an interval spanning bands): supports none of A, B, C"))

    def n(L, k):
        return sum(w["outcome"] == k for w in by.get(L, []))
    kills = []
    for L in Ls:
        if L <= 28 and len(by[L]) == expect_seeds and n(L, "extinct") == expect_seeds:
            kills.append(f"B falsified: all {expect_seeds} extinct at L={L}")
        if L >= 44 and n(L, "established"):
            kills.append(f"B falsified: {n(L, 'established')} established at L={L}")
        if L >= 32 and n(L, "established"):
            kills.append(f"A falsified: {n(L, 'established')} established at L={L}")
    if n(16, "extinct") >= 2:
        kills.append(f"A falsified: {n(16, 'extinct')} extinct at L=16")
    lines += kills or ["no falsification rule fired"]
    return "\n".join(lines)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    exp = int(sys.argv[sys.argv.index("--expect-seeds") + 1]) if "--expect-seeds" in sys.argv else 14
    args = [a for a in args if a != str(exp)] if "--expect-seeds" in sys.argv else args
    print(verdict(*load(args), expect_seeds=exp))
