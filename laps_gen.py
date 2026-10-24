"""#491 out-of-sample lap test, step 1: the fresh mutant list and both predictions, written BEFORE any division run.
Parents: the ancestor plus the first census exact copiers (out/two_step_filter.json order) that static_lap does not
abstain on, two per check period p in (1, 3) and up to two more with any other p. Per parent, with random.Random(491):
100 single substitutions, 50 single indels, 50 double substitutions, letters drawn from the 26 non-parasite ops as
petri.py draws them. Genomes already in two_step_filter.json, duplicates and parents are dropped.
Writes out/laps_mutants.json (genome strings) and out/laps_predictions.json; prints both sha256."""
import sys, json, random, hashlib, collections
sys.path.insert(0, ".")
from petri import parse, ANCESTOR, OPS
from static_lap import predict, arith
LET = "abcdefghijklmnopqrstuvwxyz"
show = lambda g: "".join(LET[x] for x in g)
census = json.load(open("out/two_step_filter.json"))
known = {r["genome"] for r in census}
parents = [show(ANCESTOR)]; byp = collections.Counter()
for r in census:
    g = parse(r["genome"]); pr = predict(g); a = arith(g)
    if pr[0] != "exact" or a is None: continue
    p = a[2] if a[0] == "exact" else a[1]
    slot = p if p in (1, 3) else "other"
    if byp[slot] < 2: parents.append(r["genome"]); byp[slot] += 1
rng = random.Random(491); nops = len(OPS) - 1; out = []
for P in parents:
    g = list(parse(P)); L = len(g)
    for _ in range(100):
        h = g[:]; i = rng.randrange(L); h[i] = rng.randrange(nops); out.append(h)
    for _ in range(50):
        h = g[:]; i = rng.randrange(L + 1)
        if rng.random() < 0.5: h.insert(i, rng.randrange(nops))
        elif L > 10: del h[min(i, L - 1)]
        out.append(h)
    for _ in range(50):
        h = g[:]
        for i in rng.sample(range(L), 2): h[i] = rng.randrange(nops)
        out.append(h)
seen = set(parents) | known; M = []
for h in out:
    s = show(h)
    if s not in seen: seen.add(s); M.append(s)
preds = [{"genome": s, "static": list(predict(parse(s))), "arith": (lambda a: list(a) if a else None)(arith(parse(s)))} for s in M]
blob = json.dumps(M, indent=0).encode(); open("out/laps_mutants.json", "wb").write(blob)
pb = json.dumps(preds, indent=0).encode(); open("out/laps_predictions.json", "wb").write(pb)
print("parents", len(parents), dict(byp)); print("mutants", len(M))
print("mutants sha256", hashlib.sha256(blob).hexdigest()); print("predictions sha256", hashlib.sha256(pb).hexdigest())
print("static", collections.Counter(p["static"][0] if p["static"][0] != "exact" else f"exact j={p['static'][1]}" for p in preds).most_common())
print("arith", collections.Counter("none" if p["arith"] is None else f"{p['arith'][0]} j={p['arith'][1]}" if p["arith"][0] == "exact" else "never" for p in preds).most_common())
