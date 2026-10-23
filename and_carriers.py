# Plan #449: the rare AND carriers in seed 2 at update 100k (out/s2_dump.json, job petri-s2dump).
# For each: the edit against the dominant genotype, and the named outputs of one gestation (genome_trace.trace).
# Usage: python3 and_carriers.py > out/and_carriers_s2.txt
import json, difflib, collections
from genome_trace import trace, fname, NAMES
from petri import parse

d = json.load(open("out/s2_dump.json"))
G = d["genotypes"]
top = max(G, key=lambda g: g["n"])["genome"]
has = lambda g, t: any(t in k.split(",") for k in g["tasks"])
andg = [g for g in G if has(g, "AND")]
n = sum(g["n"] for g in G)
nandn = sum(g["n"] for g in G if has(g, "ANDN"))
print(f"update {d['update']}, pop {n}; AND carriers {len(andg)} (organisms {sum(g['n'] for g in andg)}); "
      f"ANDN carriers in pop {nandn}/{n}; AND carriers with ANDN {sum(has(g, 'ANDN') for g in andg)}")
print(f"if AND and ANDN were independent: P(all {len(andg)} lack ANDN) = {(1 - nandn / n) ** len(andg):.4f}")


def outputs(genome):
    log, _ = trace(parse(genome), 7, 1)
    out = []
    for g, k, ip, op, bt, at, ins, tasks in log:
        if op == "IO" and len(ins) == 2:
            q, p = ins
            out.append((ip, fname(bt[1] if False else bt[1], p, q, NAMES.get(p >> 24, "?"), NAMES.get(q >> 24, "?")), tuple(tasks)))
    return out


print("\ndominant (n=%d) outputs:" % max(g["n"] for g in G), outputs(top))
for g in andg:
    sm = difflib.SequenceMatcher(None, top, g["genome"], autojunk=False)
    ed = [(t, i1, top[i1:i2], g["genome"][j1:j2]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal"]
    print(f"\nAND carrier n={g['n']} len {len(g['genome'])} tasks {g['tasks']}\n  edits vs dominant: {ed}")
    print("  outputs:", outputs(g["genome"]))
