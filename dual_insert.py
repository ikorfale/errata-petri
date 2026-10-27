"""zenith 105387 falsifier (#530): drop one AND+ANDN genome (or the dominant, as control) into an s2 monoculture and
watch whether its lineage sweeps. Prediction fixed first in PREDICT-dual-1027.md.
Usage: python3 dual_insert.py dual|control SEED[,SEED] [UPDATES] -> out/dual_insert.jsonl"""
import json, os, sys, time
from collections import Counter
from petri import World, parse
D = json.load(open("out/s2_dump.json")); TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
DUAL = sorted(json.load(open("out/and_andn_dup.json")), key=lambda h: (h["len"], h["a"], h["place"]))[0]["genome"]
arm = sys.argv[1]; seeds = [int(s) for s in sys.argv[2].split(",")]; ups = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
PATCH = sys.argv[4:] == ["patch"]   # third arm (PREDICT amendment 3): fill a 5x6 block of 30 cells
OUT = "out/dual_patch.jsonl" if PATCH else "out/dual_insert.jsonl"
QPOS = os.environ.get("DUALQ")   # 27.10 phase amendment: insert one no-op 'q' at QPOS -> 113 letters (2 mod 3, fast copy loop)
if QPOS is not None: OUT = OUT.replace(".jsonl", f"_q{QPOS}.jsonl")
for s in seeds:
    w = World(seed=s); t0 = time.time()
    for c in range(w.n): w.inject(parse(TOP), "s2", cell=c)
    cell = w.rng.randrange(w.n)
    for _ in range(50): w.run_update()   # warm-up: residents divide and carry real merit (~10k) before the seed goes in
    r0, c0 = divmod(cell, w.side)
    cells = [((r0 + i) % w.side) * w.side + (c0 + j) % w.side for i in range(5) for j in range(6)] if PATCH else [cell]
    live = [o for o in w.cells if o is not None]; m = sum(o.merit for o in live) / len(live)   # see PREDICT amendment
    G = parse(DUAL if arm == "dual" else TOP)
    if arm == "dual" and QPOS is not None: G = G[:int(QPOS)] + parse("q") + G[int(QPOS):]
    for x in cells: w.inject(list(G), "seed", cell=x); w.cells[x].merit = m
    tb = Counter(); _div = w.divide
    def divide(o, c, _div=_div, w=w, tb=tb):
        n0, lin, t = w.births, o.lineage, set(o.tasks); _div(o, c)
        if w.births > n0 and lin == "seed":
            tb["births"] += 1; tb["AND+ANDN"] += ("AND" in t and "ANDN" in t)
    w.divide = divide
    row = {"arm": arm, "seed": s, "cell": cell, "patch": PATCH, "len": len(G), "qpos": QPOS, "checks": []}
    for u in range(1, ups + 1):
        w.run_update()
        if u in (100, 250, 500, 1000, 1500, 2000) or u == ups:
            mine = sum(1 for o in w.cells if o is not None and o.lineage == "seed")
            row["checks"].append({"after": u, "cells": mine, "of": w.n, "births": tb["births"], "births_and_andn": tb["AND+ANDN"]})
            if not mine: row["extinct_by"] = u; break
    row["sec"] = round(time.time() - t0); print(json.dumps(row), flush=True)
    open(OUT, "a").write(json.dumps(row) + "\n")
