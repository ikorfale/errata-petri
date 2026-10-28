"""#541 zenith 105858: strict-rule refusals per arm (seeds 1-7, out/e3strict_c.jsonl, the rerun with refusal counters).
Per mode, pooled over worlds: viable refusals per 1,000 host births, episodes per 1,000 births, share of episodes lost
before dividing, and the first-division gap with vs without a refusal (medians pooled as the median of world medians)."""
import json
from collections import defaultdict
from statistics import median
by = defaultdict(list)
for l in open("out/e3strict_c.jsonl"):
    r = json.loads(l)
    if "warm" not in r: by[r["mode"]].append(r)
print("mode     worlds  births    viable/1k  episodes/1k  lost%   pend%  first-gap clean | refused (median of world medians)")
for m in ("local", "host", "updates"):
    rs = by[m]; B = sum(r["brk"][0] for r in rs); f = lambda k: sum(r["ref"][k] for r in rs)
    ep = f("episodes")
    fc = median(r["ref"]["firstgap_clean_q10_50_90"][1] for r in rs if r["ref"]["firstgap_clean_n"])
    fr = [r["ref"]["firstgap_ref_q10_50_90"][1] for r in rs if r["ref"]["firstgap_ref_n"]]
    print(f"{m:8s} {len(rs):5d} {B:9d} {1000*f('viable_refusals')/B:10.1f} {1000*ep/B:11.2f} {100*f('lost')/ep:6.1f} {100*f('alive_pending')/ep:6.1f}  {fc:6.0f} | {median(fr):6.0f} (n worlds {len(fr)})")
