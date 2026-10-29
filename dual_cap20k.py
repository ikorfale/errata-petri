"""zenith-claude 107851: do any of the 42 dual genotypes that did not divide within 2000 isolation steps divide by 20,000?
Same trace as dual_births_trace.py (genome_trace, seed 7, 1 gestation), cap 20000. Also prints each genotype's
world old-age limit, 20 x max(len,10) instructions (petri.py age_limit). Written 29.10 16:11 UTC (date -u)."""
import json, sys
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
H = json.load(open("out/dual_births_trace_other.json"))["hits"]
rows = []
for h in H:
    if h["steps"] < 2000: continue
    try: log, n = trace(parse(h["genome"]), 7, 1, cap=20000); ok = bool(log)
    except Exception as e: n, ok = None, False
    rows.append({"genome": h["genome"], "len": len(h["genome"]), "steps20k": n, "divided": ok and n < 20000,
                 "age_limit": 20 * max(len(h["genome"]), 10)})
json.dump(rows, open("out/dual_cap20k.json", "w"))
d = [r for r in rows if r["divided"]]
print("genotypes over 2000:", len(rows), "divide by 20000:", len(d))
for r in d: print("  len", r["len"], "steps", r["steps20k"], "age limit", r["age_limit"])
print("age limits of the 42:", sorted(set(r["age_limit"] for r in rows)))
