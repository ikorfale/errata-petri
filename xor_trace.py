# Are XOR and EQU credits real solvers or arithmetic coincidences?
# Inputs are random 32-bit words. a+b equals a^b whenever a&b == 0, and a+~b equals
# ~(a^b) whenever a&~b == 0: each with probability (3/4)^32 ~ 1.0e-4 per output.
# Part 1: rerun a world and, at each first XOR/EQU/AND credit of a gestation, record
# which arithmetic expression of the two inputs the output also equals, and the genome.
# Part 2: each crediting genotype alone, mutation off, many gestations on fresh inputs:
# the share of gestations that earn the task again. A heritable solver should be near 1.
import json, random, sys
from collections import Counter
sys.path.insert(0, __import__("os").path.dirname(__file__))
import petri
from petri import World, Org, ANCESTOR, TASKS, M32, show, parse

WATCH = ("XOR", "EQU", "AND")

def forms(a, b, v):
    f = {"a+b": (a + b) & M32, "a-b": (a - b) & M32, "b-a": (b - a) & M32,
         "a+~b": (a + (~b & M32)) & M32, "b+~a": (b + (~a & M32)) & M32,
         "~(a+b)": ~(a + b) & M32, "~(a-b)": ~(a - b) & M32, "~(b-a)": ~(b - a) & M32}
    hit = [k for k, x in f.items() if x == v]
    # the same output may also be a cheaper logic task: XOR == NAND when a|b is all ones,
    # XOR == OR when a&b == 0, EQU == AND when a|b is all ones (each ~(3/4)^32)
    hit += ["also:" + name for name, fn, _ in TASKS if name not in ("XOR", "EQU") and v in fn(a, b)]
    if (a | b) == M32: hit.append("a|b=ones")
    if (a & b) == 0: hit.append("a&b=0")
    if (a & ~b & M32) == 0 or (b & ~a & M32) == 0: hit.append("subset")
    return hit or ["exact-only"]

class Traced(World):
    def __init__(self, *k, **kw):
        super().__init__(*k, **kw)
        self.log = Counter()
        self.genomes = {t: Counter() for t in WATCH}
    def output(self, o, v):
        before = set(o.tasks)
        super().output(o, v)
        for t in WATCH:
            if t in o.tasks and t not in before:
                a, b = o.inputs[-1], o.inputs[-2]
                for h in forms(a, b, v):
                    self.log[(t, h)] += 1
                ip = o.heads[petri.IP] % len(o.mem)
                self.log[(t, "ip-in-child" if ip >= o.glen else "ip-in-parent")] += 1
                self.genomes[t][show(o.mem[:o.glen])] += 1

def retest(genome_str, gestations=300, seed=7):
    """One organism alone, no mutation: share of its divisions credited with each task."""
    w = World(side=6, seed=seed, copy_mut=0.0, indel=0.0)
    g = parse(genome_str)
    c = w.inject(g, "test")
    o = w.cells[c]
    got, n, steps = Counter(), 0, 0
    orig = w.divide
    def div(o2, c2):
        nonlocal n
        held, b0 = set(o2.tasks), w.births
        orig(o2, c2)
        if o2 is o and w.births > b0:       # failed divides are not gestations
            n += 1
            for t in held:
                got[t] += 1
    w.divide = div
    while n < gestations and steps < 400000:
        w.step(o, c)
        steps += 1
        w.cells = [None] * w.n; w.cells[c] = o      # keep it alone; children are discarded
    return n, {t: got[t] for t in WATCH}, dict(got)

if __name__ == "__main__":
    updates = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    w = Traced(side=30, seed=seed)
    w.inject(ANCESTOR, "ancestor")
    for u in range(updates):
        w.run_update()
    print(json.dumps({"seed": seed, "updates": updates, "births": w.births,
                      "task_births": dict(w.task_births)}))
    for (t, h), k in sorted(w.log.items()):
        print("CREDIT", t, h, k)
    for t in WATCH:
        top = w.genomes[t].most_common(5)
        print("GENOTYPES", t, "distinct", len(w.genomes[t]))
        for gs, k in top:
            n, watched, allt = retest(gs)
            print("RETEST", t, "credits", k, "gestations", n, "watched", json.dumps(watched),
                  "all", json.dumps(allt), "genome", gs)
    sys.stdout.flush()
