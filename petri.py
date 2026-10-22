"""Petri: a small Avida-style artificial-life world.

Each organism is a program in a 26-instruction "heads" language. It copies
itself instruction by instruction (copies can mutate), divides, and its child
takes a neighbouring cell on a toroidal grid. Organisms that compute logic
functions of their inputs (NOT, NAND, AND, ...) through IO get more CPU time.
Nobody tells them how: if a function appears, evolution found it.
"""
import json, random, sys, time
from collections import Counter

OPS = ["nop-A", "nop-B", "nop-C", "if-n-equ", "if-less", "if-label", "mov-head",
       "jmp-head", "get-head", "set-flow", "shift-r", "shift-l", "inc", "dec",
       "push", "pop", "swap-stk", "swap", "add", "sub", "nand", "h-copy",
       "h-alloc", "h-divide", "IO", "h-search"]
CODE = {n: i for i, n in enumerate(OPS)}
CH = "abcdefghijklmnopqrstuvwxyz"          # one letter per op, a/b/c = nops
NOP = (0, 1, 2)
COMP = {0: 1, 1: 2, 2: 0}                  # nop-A -> B -> C -> A
M32 = 0xFFFFFFFF
IP, RH, WH, FH = 0, 1, 2, 3
TASKS = [("NOT", lambda a, b: [~a & M32, ~b & M32], 1),
         ("NAND", lambda a, b: [~(a & b) & M32], 1),
         ("AND", lambda a, b: [a & b], 2),
         ("ORN", lambda a, b: [(a | ~b) & M32, (b | ~a) & M32], 2),
         ("OR", lambda a, b: [a | b], 3),
         ("ANDN", lambda a, b: [a & ~b & M32, b & ~a & M32], 3),
         ("NOR", lambda a, b: [~(a | b) & M32], 4),
         ("XOR", lambda a, b: [a ^ b], 4),
         ("EQU", lambda a, b: [~(a ^ b) & M32], 5)]


def parse(text):
    """Genome from letters ("rzcag...") or op names separated by spaces/newlines."""
    t = text.strip()
    if t and all(ch in CH for ch in t):
        return [CH.index(ch) for ch in t]
    return [CODE[w] for w in t.replace(",", " ").split() if not w.startswith("#")]


def show(g):
    return "".join(CH[i] for i in g)


ANCESTOR = (["h-alloc", "h-search", "nop-C", "nop-A", "mov-head", "nop-C"]
            + ["nop-C"] * 85 +
            ["h-search", "h-copy", "if-label", "nop-C", "nop-A", "h-divide",
             "mov-head", "nop-A", "nop-B"])
ANCESTOR = [CODE[n] for n in ANCESTOR]


class Org:
    __slots__ = ("mem", "glen", "heads", "reg", "stk", "copied", "ncopy", "inputs",
                 "inbuf", "tasks", "merit", "age", "credit", "lineage", "born")

    def __init__(self, genome, lineage, merit=1.0, born=0):
        self.mem = bytearray(genome)
        self.glen = len(genome)
        self.heads = [0, 0, 0, 0]
        self.reg = [0, 0, 0]
        self.stk = []
        self.copied = bytearray()           # recent h-copy values (tail kept short)
        self.ncopy = 0                      # h-copy executions this gestation
        self.inputs = []
        self.inbuf = []
        self.tasks = set()
        self.merit = merit
        self.age = 0                        # instructions executed
        self.credit = 0.0                   # fractional CPU carried between updates
        self.lineage = lineage
        self.born = born


class World:
    def __init__(self, side=30, seed=1, copy_mut=0.0075, indel=0.05, slice_=30):
        self.side, self.n = side, side * side
        self.rng = random.Random(seed)
        self.cells = [None] * self.n
        self.copy_mut, self.indel, self.slice = copy_mut, indel, slice_
        self.update = 0
        self.births = 0
        self.task_births = Counter()

    def inject(self, genome, lineage, cell=None):
        if not 10 <= len(genome) <= 256:
            raise ValueError("a seeded genome must have 10 to 256 instructions")
        cell = self.rng.randrange(self.n) if cell is None else cell
        self.cells[cell] = Org(genome, lineage, merit=float(len(genome)), born=self.update)
        return cell

    def neighbour(self, c):
        x, y = c % self.side, c // self.side
        dx, dy = self.rng.choice([(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0),
                                  (-1, 1), (0, 1), (1, 1)])
        return (x + dx) % self.side + ((y + dy) % self.side) * self.side

    # --- one instruction -------------------------------------------------
    def step(self, o, c):
        mem, h = o.mem, o.heads
        L = len(mem)
        ip = h[IP] % L
        op = mem[ip]
        nxt = mem[(ip + 1) % L]
        mod = nxt if nxt in NOP else None   # a following nop modifies the op
        adv = 1 + (mod is not None and op not in NOP and op not in (3, 4))
        r = (mod if mod is not None else 1) if op not in NOP else 1
        reg = o.reg
        if op <= 2:
            adv = 1
        elif op == 21:                      # h-copy
            v = mem[h[RH] % L]
            if self.rng.random() < self.copy_mut:
                v = self.rng.randrange(len(OPS))
            mem[h[WH] % L] = v
            o.copied.append(v)
            if len(o.copied) > 40:
                del o.copied[:-10]
            o.ncopy += 1
            h[RH] = (h[RH] + 1) % L
            h[WH] = (h[WH] + 1) % L
            adv = 1
        elif op == 5:                       # if-label: last copied == complement of label
            lab = self.label(mem, ip + 1)
            adv = 1 + len(lab)
            want = [COMP[x] for x in lab]
            if not (lab and o.copied[-len(lab):] == bytes(want)):
                adv += 1
        elif op == 6:                       # mov-head ?IP? -> flow head
            hd = mod if mod is not None else IP
            h[hd] = h[FH]
            if hd == IP:
                return
        elif op == 3 or op == 4:            # if-n-equ / if-less
            rr = mod if mod is not None else 1
            a, b = reg[rr], reg[COMP[rr]]
            ok = (a != b) if op == 3 else (a < b)
            adv = (1 if mod is None else 2)
            if not ok:
                adv += 1
        elif op == 7:                       # jmp-head ?IP? by CX
            hd = mod if mod is not None else IP
            h[hd] = (h[hd] + reg[2]) % L
            if hd == IP:
                h[IP] = (h[IP] + 1) % L
                return
        elif op == 8:                       # get-head: CX = ?IP?
            reg[2] = h[mod if mod is not None else IP]
        elif op == 9:                       # set-flow: FH = ?CX?
            h[FH] = reg[mod if mod is not None else 2] % L
        elif op == 10:
            reg[r] >>= 1
        elif op == 11:
            reg[r] = (reg[r] << 1) & M32
        elif op == 12:
            reg[r] = (reg[r] + 1) & M32
        elif op == 13:
            reg[r] = (reg[r] - 1) & M32
        elif op == 14:
            if len(o.stk) < 10:
                o.stk.append(reg[r])
        elif op == 15:
            reg[r] = o.stk.pop() if o.stk else 0
        elif op == 16:
            pass                            # single stack: swap-stk is a no-op
        elif op == 17:
            reg[r], reg[COMP[r]] = reg[COMP[r]], reg[r]
        elif op in (18, 19, 20):
            a, b = reg[1], reg[2]
            reg[r] = ((a + b) if op == 18 else (a - b) if op == 19 else ~(a & b)) & M32
        elif op == 22:                      # h-alloc: double memory
            if L == o.glen and L < 400:
                mem.extend([0] * L)
                reg[0] = L
            adv = 1
        elif op == 23:                      # h-divide
            self.divide(o, c)
            return
        elif op == 24:                      # IO: output ?BX?, input into ?BX?
            self.output(o, reg[r])
            if not o.inbuf:
                o.inbuf = [self.rng.getrandbits(32) for _ in range(3)]
            v = o.inbuf.pop()
            o.inputs.append(v)
            reg[r] = v
        elif op == 25:                      # h-search for complement template
            lab = self.label(mem, ip + 1)
            want = [COMP[x] for x in lab]
            adv = 1 + len(lab)
            if not lab:
                reg[1] = reg[2] = 0
                h[FH] = (ip + 1) % L
            else:
                k = len(want)
                p = (mem * 3).find(bytes(want), ip + 1 + k, ip + L - 1 + k)
                pos = None if p < 0 else p % L
                if pos is None:
                    reg[1] = reg[2] = 0
                    h[FH] = (ip + 1) % L
                else:
                    reg[1] = (pos - ip) % L
                    reg[2] = k
                    h[FH] = (pos + k) % L
        h[IP] = (ip + adv) % L

    @staticmethod
    def label(mem, start):
        L = len(mem)
        out = []
        while len(out) < 10 and mem[(start + len(out)) % L] in NOP:
            out.append(mem[(start + len(out)) % L])
        return out

    def output(self, o, v):
        ins = o.inputs[-2:]
        if len(ins) < 2 or ins[0] == ins[1]:
            return                          # tasks need two distinct inputs; with a == b
                                            # outputting 0 would pass XOR and ANDN
        a, b = ins[-1], ins[-2]
        for name, f, _ in TASKS:
            if name not in o.tasks and v in f(a, b) and v not in (a, b):
                o.tasks.add(name)

    def divide(self, o, c):
        mem, h = o.mem, o.heads
        rh, wh = h[RH], h[WH]
        if wh == 0:
            wh = len(mem)                   # write head wrapped at the end of memory
        if rh == 0:
            rh = len(mem)
        child = mem[rh:wh] if wh > rh else []
        parent = mem[:rh]
        h[IP] = (h[IP] + 1) % len(mem)
        if (len(child) < 10 or len(parent) < 10 or not (0.5 <= len(child) / len(parent) <= 2)
                or o.ncopy < 0.5 * len(child)):
            return                          # failed division: keep running (Avida also
                                            # requires at least half the child to be copied)
        if self.rng.random() < self.indel:
            i = self.rng.randrange(len(child) + 1)
            if self.rng.random() < 0.5:
                child.insert(i, self.rng.randrange(len(OPS)))
            elif len(child) > 10:
                child.pop(min(i, len(child) - 1))
        bonus = float(min(o.ncopy, len(child)))   # merit = copied size, not padded length
        for name, _, b in TASKS:
            if name in o.tasks:
                bonus *= 2 ** b
        for name in o.tasks:
            self.task_births[name] += 1
        kid = Org(child, o.lineage, merit=bonus, born=self.update)
        self.cells[self.neighbour(c)] = kid
        self.births += 1
        # parent restarts as a fresh copy of itself, keeping its merit
        o.mem, o.glen = parent, len(parent)
        o.heads = [0, 0, 0, 0]
        o.reg = [0, 0, 0]
        o.stk, o.copied, o.inputs, o.inbuf = [], bytearray(), [], []
        o.ncopy = 0
        o.merit = bonus
        o.tasks = set()

    def run_update(self):
        live = [(c, o) for c, o in enumerate(self.cells) if o is not None]
        if not live:
            return
        mean = sum(o.merit for _, o in live) / len(live)
        self.rng.shuffle(live)
        for c, o in live:
            if self.cells[c] is not o:
                continue                    # replaced by a neighbour's child
            o.credit += self.slice * o.merit / mean
            n = int(o.credit)
            o.credit -= n
            step = self.step
            for _ in range(n):
                step(o, c)
            o.age += n
            if o.age > 20 * max(o.glen, 10):
                self.cells[c] = None        # old age: 20 x genome length in instructions (Avida)
        self.update += 1

    def census(self):
        live = [o for o in self.cells if o is not None]
        g = Counter(show(o.mem[:o.glen]) for o in live)
        t = Counter(name for o in live for name in o.tasks)
        lin = Counter(o.lineage for o in live)
        return {"update": self.update, "pop": len(live), "births": self.births,
                "genotypes": len(g),
                "mean_len": round(sum(o.glen for o in live) / max(1, len(live)), 1),
                "top": g.most_common(1)[0][0] if g else "",
                "tasks_now": dict(t), "lineages": dict(lin),
                "task_births": dict(self.task_births)}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--updates", type=int, default=200)
    ap.add_argument("--side", type=int, default=30)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--mut", type=float, default=0.0075)
    ap.add_argument("--every", type=int, default=50)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    w = World(side=a.side, seed=a.seed, copy_mut=a.mut)
    w.inject(ANCESTOR, "ancestor")
    rows = []
    t0 = time.time()
    for u in range(a.updates):
        w.run_update()
        if (u + 1) % a.every == 0:
            row = w.census()
            row["sec"] = round(time.time() - t0, 1)
            rows.append(row)
            print(json.dumps({k: row[k] for k in ("update", "pop", "births", "genotypes",
                                                  "mean_len", "tasks_now", "sec")}), flush=True)
    if a.out:
        json.dump(rows, open(a.out, "w"))
