"""Summarise an or_counterfactual.py run: C share at the last census per seed, mean with a bootstrap 95% CI over seeds
(10,000 resamples, fixed seed), seeds at 0, against the start share (added 29.10 for the OR_TAG=D arm).
Usage: python3 or_cf_summary.py out/or_cf_D32.txt"""
import json, random, sys
L = [json.loads(l) for l in open(sys.argv[1])]
h, runs = L[0], L[1:]
p0 = h["clade_C_at_start"] / h.get("n_start", 877)
end = [r["rows"][-1]["C"] for r in runs]
r = random.Random(1); n = len(end)
bs = sorted(sum(r.choice(end) for _ in range(n)) / n for _ in range(10000))
print(json.dumps({"seeds": n, "start_share": round(p0, 4), "end_u": runs[0]["rows"][-1]["u"], "mean_end": round(sum(end) / n, 4),
                  "ci95": [round(bs[249], 4), round(bs[9749], 4)], "zero": sum(e == 0 for e in end),
                  "above_0.5": sum(e > 0.5 for e in end), "max": max(end), "ends": end}))
