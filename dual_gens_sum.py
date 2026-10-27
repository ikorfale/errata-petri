"""Pool out/dual_gens.jsonl by arm and generation (weights = dead organisms). Usage: python3 dual_gens_sum.py"""
import json
from collections import defaultdict
P = defaultdict(lambda: defaultdict(float))
for l in open("out/dual_gens.jsonl"):
    r = json.loads(l); a = r["arm"] + ("-sweep" if r["arm"] == "dual" and r["seed"] == 11 else "")
    for g, v in r["gens"].items():
        n = v["dead"]; d = n * v["p_divided"]; S = P[(a, g)]
        S["n"] += n; S["cens"] += v["alive_censored"]; S["kids"] += n * v["mean_kids"]; S["div"] += d
        S["t"] += d * v["upd_to_first_div"]; S["ratio"] += n * v["merit_over_mean_at_birth"]
print("arm          gen       dead  alive  kids/ind  P(div)  upd->1st  merit/mean")
for (a, g), S in sorted(P.items()):
    n = max(1, S["n"])
    print(f"{a:12s} {g:9s} {int(S['n']):6d} {int(S['cens']):6d} {S['kids']/n:9.3f} {S['div']/n:7.3f} {S['t']/max(1,S['div']):9.2f} {S['ratio']/n:10.3f}")
