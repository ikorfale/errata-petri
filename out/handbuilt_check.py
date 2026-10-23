"""Plan #451 (zenith 99386/99401): hand-built AND+ANDN genotype from the s2 dominant.
Block 'ycuopcuyq' inserted before h-search (pos 84): IO into C, nand, push, pop into C, nand (= AND of the
last two inputs), IO, plus one no-op so the length stays 2 mod 3 (the 3-copy loop checks the end label only
every third copy; 8 inserted instructions made it copy the genome three times over).
Solo: 20x20, mutation off, seeds 1-10, pop at update 150. H2H vs parent: seeds 1-20 x 2 placements, 300 updates.
Arms: hb9 (AND exponent 2, x512 vs x128), hb9 with AND worth nothing (cost-only control, x128 vs x128),
top+3 no-ops (length-only control). Usage: python3 out/handbuilt_check.py ARM"""
import json, sys, statistics as st
sys.path.insert(0, ".")
import petri
from petri import World, parse
D = json.load(open("out/s2_dump.json"))
TOP = max(D["genotypes"], key=lambda g: g["n"])["genome"]
ARMS = {"hb9": TOP[:84] + "ycuopcuyq" + TOP[84:], "hb9_and0": TOP[:84] + "ycuopcuyq" + TOP[84:],
        "top3q": TOP[:84] + "qqq" + TOP[84:]}
arm = sys.argv[1]; g = ARMS[arm]
if arm == "hb9_and0":
    petri.TASKS[:] = [(n, f, 0 if n == "AND" else b) for n, f, b in petri.TASKS]
def world(s):
    w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0; return w
solo = []
for s in range(1, 11):
    w = world(s); w.inject(parse(g), "x", cell=0)
    for u in range(150): w.run_update()
    solo.append(sum(o is not None for o in w.cells))
print(arm, len(g), "solo pop@150 mean", st.mean(solo), solo, flush=True)
sh = []
for s in range(1, 21):
    for a, b in ((0, 210), (210, 0)):
        w = world(s); w.inject(parse(TOP), "par", cell=a); w.inject(parse(g), "mut", cell=b)
        for u in range(300): w.run_update()
        live = [o.lineage for o in w.cells if o is not None]
        sh.append(live.count("mut") / max(1, len(live)))
print(arm, "h2h share mean %.3f, %d/40 >= 0.5, min %.3f max %.3f" % (st.mean(sh), sum(x >= 0.5 for x in sh), min(sh), max(sh)), flush=True)
