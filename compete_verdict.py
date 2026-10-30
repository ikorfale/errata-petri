"""Verdict for PREDICT-compete-1030.md: winners, update to 90%, and the logit slope of B's share (per update) from the
25-update trace of each v2 seed. Usage: python3 compete_verdict.py > out/compete_verdict.txt"""
import json, math
from statistics import median
for f in ("out/compete_1030.jsonl", "out/compete_1030_v2.jsonl"):
    rows = [json.loads(l) for l in open(f)]
    for r in rows:
        pts = [(u, nb / n) for u, n, nb in r["trace"] if 0 < nb < n]
        slope = ""
        if len(pts) >= 2 and not r["arm"].startswith("control"):
            xs = [u for u, _ in pts]; ys = [math.log(p / (1 - p)) for _, p in pts]
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
            slope = f"logit slope {b:.4f}/update"
        print(r["arm"], r["seed"], r["winner"], r["update"], f"B {r['nB']}/{r['pop']}", slope)
    test = [r for r in rows if not r["arm"].startswith("control")]
    print(f"{f}: B wins {sum(r['winner']=='B' for r in test)}/{len(test)}, median update {median(r['update'] for r in test)}\n")
