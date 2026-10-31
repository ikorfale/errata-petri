"""Exploratory reads for PREDICT-lockin-1031-A1 item 3 (written 31.10 06:10 UTC, after lockin-1031 finished).
(a) modal-length share of live cells at update 44,000 vs end median, Spearman over all 14 seeds (6 seen + 8 new);
(b) is a lock absorbing? For each seed, after its first lock: share of later snapshots with one length >= 50%,
and the modal lengths seen while locked. Reads out/shrink_carrier_<seed>.json only."""
import json
seeds = [14, 28, 11, 21, 23, 26, 12, 15, 17, 29, 13, 19, 20, 18]
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r
def spearman(x, y):
    rx, ry = rank(x), rank(y); n = len(x); mx = sum(rx) / n; my = sum(ry) / n
    c = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return c / (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
sh, end = [], []
print("seed share44k mode44k end | lock_at lockL held_after modal_lengths_while_held")
for s in seeds:
    rows = json.load(open(f"out/shrink_carrier_{s}.json"))["rows"]
    r = next(r for r in rows if r["update"] == 44000); L, n = max(r["len_hist"], key=lambda x: x[1])
    sh.append(n / r["pop"]); end.append(rows[-1]["glen_med"])
    m = [(r["update"],) + tuple(max(r["len_hist"], key=lambda x: x[1])) + (r["pop"],) for r in rows]
    li = next((i for i, (u, l, c, p) in enumerate(m) if c / p >= 0.5), None)
    if li is None: print(s, f"{sh[-1]:.2f}", L, end[-1], "| never"); continue
    after = m[li:]; held = [x for x in after if x[2] / x[3] >= 0.5]
    print(s, f"{sh[-1]:.2f}", L, end[-1], "|", after[0][0], after[0][1], f"{len(held)}/{len(after)}", sorted({x[1] for x in held}))
print(f"Spearman(share at 44k, end median) over {len(seeds)} seeds: {spearman(sh, end):.2f}")
