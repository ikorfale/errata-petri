"""#484 full filter: every dividing AND+ANDN second-step hit in out/two_step.json, deduplicated by genome.
For each: does the first child equal the parent (copy_mut 0, indel 0)? For those that do: solo growth (seeds 1-5, 150 updates).
Writes out/two_step_filter.json and prints a summary."""
import sys, json, time
sys.path.insert(0, "."); sys.path.insert(0, "out")
from two_step_check import edit, child, solo, top, blk
d = json.load(open("out/two_step.json"))
seen = {}
for s in d:
    g1 = edit(top[:s["p"]] + blk + top[s["p"] + 12:], s["first"])
    for e2, n, L in s["hits"]:
        g = edit(g1, e2)
        seen.setdefault(g, []).append((s["p"], s["first"], e2, n))
print("hits", sum(len(s["hits"]) for s in d), "distinct genomes", len(seen), flush=True)
rows = []; t0 = time.time()
for i, (g, routes) in enumerate(seen.items()):
    c = child(g)
    ok = c == g
    rows.append({"genome": g, "len": len(g), "steps": routes[0][3], "routes": routes, "faithful": ok,
                 "child_len": len(c) if c else None, "solo": solo(g) if ok else None})
    if i % 100 == 0: print(i, round(time.time() - t0), flush=True)
json.dump(rows, open("out/two_step_filter.json", "w"))
f = [r for r in rows if r["faithful"]]
print("faithful", len(f), "of", len(rows))
for r in sorted(f, key=lambda r: r["steps"]):
    print(r["len"], r["steps"], "solo", r["solo"], r["routes"][:3])
