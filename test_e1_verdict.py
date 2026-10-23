"""Synthetic checks of e1_verdict.py (run: python3 test_e1_verdict.py; prints how many checks ran)."""
import json, math, random, tempfile, os
from e1_verdict import load, verdict

LS = [16, 20, 24, 28, 32, 36, 40, 44, 48]


def world(seed, L, outcome):
    if outcome == "extinct":
        census = [{"u": 2000 + 250 * k, "inf": 3} for k in range(1, 4)] + [{"u": 3000, "inf": 0}]
    else:
        inf = 300 if outcome == "established" else 20
        census = [{"u": 2000 + 250 * k, "inf": inf} for k in range(1, 13)]
    return {"seed": seed, "L": L, "upd": 3000, "end_genomes": [["x" * L, 5]] if outcome != "extinct" else [],
            "injections": 1, "secondary": 0, "cpu_s": 1, "census": census}


def run(rule):
    fd, path = tempfile.mkstemp(suffix=".jsonl"); os.close(fd)
    with open(path, "w") as f:
        for s in range(1, 15):
            f.write(json.dumps({"warm": {"seed": s, "h_occupied": 0.05, "merit_median_over_mean": 0.5}}) + "\n")
            for L in LS:
                f.write(json.dumps(world(s, L, rule(s, L))) + "\n")
    out = verdict(*load([path])); os.unlink(path); return out


checks = []
def check(name, cond, out):
    checks.append(name)
    assert cond, name + "\n" + out

rng = random.Random(1)
o = run(lambda s, L: "established" if rng.random() < 1 / (1 + math.exp(0.4 * (L - 30))) else "extinct")
l50 = float(o.split("L50 = ")[1].split()[0]); check("logistic recovers L50~30", 27 < l50 < 33, o)
o = run(lambda s, L: "established" if L <= 32 else "extinct")
check("separation interval (32,36] is inside B", "L50 in (32, 36]" in o and "band containing L50: B" in o, o)
check("A killed by established at 32", "A falsified: 14 established at L=32" in o, o)
o = run(lambda s, L: "established" if L <= 28 else "extinct")
check("gap (28,32] supports none", "L50 in (28, 32]" in o and "supports none" in o, o)
o = run(lambda s, L: "established" if L <= 36 else "extinct")
check("B band from separation (36,40]", "band containing L50: B" in o, o)
o = run(lambda s, L: "established" if L < 24 else "extinct")
check("separation (20,24] intersects A and C -> ambiguous", "L50 in (20, 24]" in o and "ambiguous (A, C)" in o, o)
o = run(lambda s, L: "established" if rng.random() < 0.5 else "extinct")
check("flat null fires and blocks the band", "NULL (flat)" in o and "none given, a null fired" in o, o)
o = run(lambda s, L: "extinct" if L <= 28 else "established")
check("reversed separation", "reversed separation" in o and "B falsified: all 14 extinct at L=16" in o, o)
o = run(lambda s, L: "unresolved" if s == 1 else ("established" if L <= 24 else "extinct"))
check("unresolved excluded and listed", "1:20@5000" in o and " 13    0      1" in o.replace("16    13", " 13"), o)
o = run(lambda s, L: "extinct" if (L == 16 and s <= 2) else ("established" if L <= 24 else "extinct"))
check("A killed by 2 extinct at 16", "A falsified: 2 extinct at L=16" in o, o)
o = run(lambda s, L: "established" if L <= 28 or (L == 32 and s <= 2) else "extinct")
check("quasi-separation: 2/14 at 32 is not B (second model's case)", "band containing L50: B" not in o and "quasi-separation" in o, o)
o = run(lambda s, L: "established" if L <= 32 or (L == 36 and s <= 12) else "extinct")
check("quasi-separation: 12/14 at 36 is B", "band containing L50: B" in o, o)
from petri import ANCESTOR, CODE, show
check("show() is one character per instruction", len(show(ANCESTOR)) == len(ANCESTOR), "")
print(len(checks), "checks passed")
