"""zenith 100725 falsifier, restricted (Fable) to deletions in 59..83, where no jump landing or loop instruction moves.
Prediction from fast iff L = e (mod 3), e = 2: net -1 slow, net -2 never. Paired control for each edit: the same
deletion(s) with the length restored by no-op 'q' inserted at 84 (minus the deleted count before 84). If the control is
fast and the edit is not in its predicted class, the copy-loop story is falsified for that edit."""
import sys, json, itertools, collections
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
def steps(g):
    _, n = trace(parse(g), 7, 1, cap=20000); return n
def cls(n): return "never" if n >= 20000 else ("fast" if n < 300 else "slow")
def dele(g, idx): return "".join(c for k, c in enumerate(g) if k not in idx)
R = range(59, 84)
for k, pred in ((1, "slow"), (2, "never")):
    tab = collections.Counter(); bad = []
    for idx in itertools.combinations(R, k):
        g = dele(top, set(idx))
        ctrl = g[:84 - k] + "q" * k + g[84 - k:]
        e, c = cls(steps(g)), cls(steps(ctrl))
        tab[(c, e)] += 1
        if c == "fast" and e != pred: bad.append((idx, e))
    print(f"net -{k}: {sum(tab.values())} edits; (control class, edit class) counts {dict(tab)}")
    print(f"   control fast: {sum(v for (c, e), v in tab.items() if c == 'fast')}; of these edit in predicted class '{pred}': "
          f"{tab[('fast', pred)]}; counterexamples: {len(bad)} {bad[:10]}")
