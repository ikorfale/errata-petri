"""#491 blocker 4 (power on the lap arithmetic): a targeted stratum, written BEFORE any division run.
The random mutants of laps_gen.py are nearly all j=1, so they cannot tell the two predictors apart. Here: the full
single-edit neighbourhood (every single insertion and substitution of the 26 non-parasite ops at every position) of
the same parents, each variant classified by its predicted cell (check period p, arith prediction, static prediction).
From every cell, up to CAP variants are drawn with random.Random(4912), so rare cells (j=3, j=5, p=2 and p=4, and every
cell where arith and static disagree) are in the test with their own counts. Cells where static abstains are skipped,
as in laps_gen.py. Genomes in two_step_filter.json, the parents and the laps_gen.py mutants are excluded.
Writes out/laps_targeted.json; prints the cell table and sha256."""
import sys, json, random, hashlib, collections
sys.path.insert(0, ".")
from petri import parse, ANCESTOR, OPS
from static_lap import predict, arith
CAP = 25
LET = "abcdefghijklmnopqrstuvwxyz"
show = lambda g: "".join(LET[x] for x in g)
census = json.load(open("out/two_step_filter.json"))
known = {r["genome"] for r in census}
parents = [show(ANCESTOR)]; byp = collections.Counter()
for r in census:                                  # the same parent rule as laps_gen.py
    g = parse(r["genome"]); pr = predict(g); a = arith(g)
    if pr[0] != "exact" or a is None: continue
    p = a[2] if a[0] == "exact" else a[1]
    slot = p if p in (1, 3) else "other"
    if byp[slot] < 2: parents.append(r["genome"]); byp[slot] += 1
known |= set(parents) | set(json.load(open("out/laps_mutants.json")))
nops = len(OPS) - 1; cells = collections.defaultdict(list); seen = set()
for P in parents:
    g = list(parse(P)); L = len(g)
    for i in range(L + 1):
        for op in range(nops):
            for h in (g[:i] + [op] + g[i:], g[:i] + [op] + g[i + 1:] if i < L else None):
                if h is None: continue
                s = show(h)
                if s in known or s in seen: continue
                seen.add(s); pr = predict(h); a = arith(h)
                if pr[0] not in ("exact", "never"): continue
                if a is None: key = ("p=?", "arith:none", f"static:{pr[0]}")
                else:
                    p = a[2] if a[0] == "exact" else a[1]
                    key = (f"p={p}", f"arith:j={a[1]}" if a[0] == "exact" else "arith:never",
                           f"static:{pr[0]}" + (f" j={pr[1]}" if pr[0] == "exact" else ""))
                cells[key].append(s)
rng = random.Random(4912); pick = []
print("cell (p, arith, static): variants -> drawn")
for key in sorted(cells, key=str):
    v = sorted(cells[key]); d = v if len(v) <= CAP else rng.sample(v, CAP)
    agree = "agree" if key[1].replace("arith:", "") == key[2].replace("static:exact ", "").replace("static:", "") else "DISAGREE"
    print(f"  {key}: {len(v)} -> {len(d)}  [{agree}]")
    pick += [{"genome": s, "cell": list(key), "static": list(predict(parse(s))),
              "arith": (lambda a: list(a) if a else None)(arith(parse(s)))} for s in d]
blob = json.dumps(pick, indent=0).encode(); open("out/laps_targeted.json", "wb").write(blob)
print("variants", len(seen), "drawn", len(pick)); print("targeted sha256", hashlib.sha256(blob).hexdigest())
