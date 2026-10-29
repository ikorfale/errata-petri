"""Offset-matched baseline (added after the readout, 29.10): origins are born close before their census, so compare
with baseline lines born at the same distance before a census. Not preregistered: a check of the G4 readout."""
import json, random
d = json.load(open("out/life_day2.json")); S = 500
nc = lambda b: (b // S + 1) * S
org = {int(k): v for k, v in d["origins"].items()}; f = max(org, key=lambda k: org[k]["life_any"])
rest = [v for k, v in org.items() if k != f]
offs = sorted(v["next_census"] - v["born"] for v in rest)
print("origin offsets before census: median", offs[len(offs)//2], "q90", offs[int(.9*len(offs))], "max", offs[-1])
b1 = [(b, l) for b, l in d["baseline_mutated_births"] if b + l >= nc(b)]
bo = [(nc(b) - b, b + l >= nc(b) + S) for b, l in b1]
print("baseline census-reaching offsets median", sorted(o for o, _ in bo)[len(bo)//2])
for W in (10, 25, 50):
    exp = 0; used = 0
    for o in offs:
        m = [s for oo, s in bo if abs(oo - o) <= W]
        if m: exp += sum(m) / len(m); used += 1
    print(f"window +-{W}: matched origins {used}, expected census2 survivors {exp:.1f}, observed 0, P(0)~{2.718281828**-exp:.2g}")
for lo, hi in ((0, 50), (50, 100), (100, 200), (200, 500)):
    m = [s for oo, s in bo if lo <= oo < hi]; print(f"baseline offset {lo}-{hi}: n {len(m)}, reach census2 {sum(m)/max(1,len(m)):.1%}")
