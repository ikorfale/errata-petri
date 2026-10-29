"""List origins with merit ratio > 1.05 alone (glitchfox 107528: real or a rounding band?) and the parent-sterile drops."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], sys.argv[1]]
import importlib.util
src = open('origin_merit.py').read().split('d = json.load(open(sys.argv[1]))')[0]
exec(src)
d = json.load(open(sys.argv[1]))
for k, v in d['origins'].items():
    if v['born'] == 62369: continue
    c, ct = rate(v['genome']); p, pt = rate(v['parent_genome'])
    if not p: print(f"parent sterile alone: origin {k} born {v['born']}, child rate {c:.4f}"); continue
    if c / p > 1.05: print(f"better: origin {k} born {v['born']} ratio {c/p:.3f} child {c:.4f} parent {p:.4f} tasks child {ct} parent {pt}")
