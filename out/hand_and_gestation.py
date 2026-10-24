import sys, json
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
g = top[:84] + "oypcupcncuy" + top[84:]
for name, x in (("top", top), ("hand", g)):
    log, n = trace(parse(x), 7, 3, cap=20000)
    gs = [r[0] for r in log]; print(name, "steps", n, "gestations reached", max(gs) + 1 if gs else 0)
    ends = {}
    for r in log: ends[r[0]] = r[1]
    print("  steps at end of each gestation", ends)
    if name == "hand":
        for r in log[30:60]: print("  ", r[1], r[2], r[3], r[5], r[7])
