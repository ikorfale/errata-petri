"""zenith 105387 falsifier: can a genome compute AND and keep ANDN? No one-step mutant does (0 of 38, and_mutants_s2.txt).
Two-step construction: duplicate a block top[a:b] that holds the AND edit (sub 70 u>b) and insert it before or after the
original block, so one copy runs ANDN and the other AND. Reports which (a, b, place) give both tasks, and their genomes."""
import json
from and_mutants import tasks, top
mut = top[:70] + "b" + top[71:]
hits = []
for a in range(40, 71):
    for b in range(71, 96):
        for place, g in (("after", top[:b] + mut[a:b] + top[b:]), ("before", top[:a] + mut[a:b] + top[a:])):
            t = tasks(g)
            if "AND" in t and "ANDN" in t: hits.append({"a": a, "b": b, "place": place, "len": len(g), "tasks": t, "genome": g})
print(len(hits), "constructions compute AND and ANDN")
for h in sorted(hits, key=lambda h: h["len"])[:8]: print(h["a"], h["b"], h["place"], h["len"], h["tasks"])
json.dump(hits, open("out/and_andn_dup.json", "w"), indent=0)
