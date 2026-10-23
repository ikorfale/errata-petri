# Which nand walk computes each task? Run one genome alone (mutation off) for one gestation and log every
# IO and nand with the truth table of each value. The three inputs carry top bytes 0x0F, 0x33, 0x55, which are the
# three columns of a 3-variable truth table, so the top byte of any value built from inputs by nand/swap/push/pop
# IS its truth table over the inputs. No symbolic execution needed. Shifts and add/sub break this; they are flagged.
# Usage: python3 genome_trace.py out/tagged_s1.json [--update 100000] [--seed 7] [--gest 3]
import json, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from petri import World, Org, OPS, TASKS, M32, parse, show

A, B, C = 0x55, 0x33, 0x0F          # top bytes of the 1st, 2nd and 3rd input popped (inbuf.pop() takes 0x55 first)
NAMES = {A: "x", B: "y", C: "z"}


def fname(v, p, q, pn, qn):
    """Name value v as a function of the two full input words p, q the task checker will use (exact, 32 bits).
    If only the top byte (the truth table) matches, the name gets '~' and the 32-bit offset: arithmetic on the way."""
    t, p, q = v & M32, p & M32, q & M32
    if t < 1 << 24:
        return str(t)                   # a counter or an offset, not a function of the inputs
    cand = {"NOT " + pn: ~p, "NOT " + qn: ~q, "NAND": ~(p & q), "AND": p & q, f"{pn}|~{qn}": p | ~q,
            f"{qn}|~{pn}": q | ~p, "OR": p | q, f"{pn}&~{qn}": p & ~q, f"{qn}&~{pn}": q & ~p, "NOR": ~(p | q),
            "XOR": p ^ q, "EQU": ~(p ^ q), pn: p, qn: q, "0": 0, "1": 0xFF}
    hit = [k for k, w in cand.items() if w & M32 == t]
    if hit:
        return hit[0]
    hit = [(k, (t - w) & M32) for k, w in cand.items() if (w >> 24) & 0xFF == t >> 24]
    if hit:
        d = hit[0][1]
        return f"{hit[0][0]}{d - (1 << 32) if d > 1 << 31 else d:+d}"
    return f"tt{t >> 24:02x}"


def trace(genome, seed=7, gestations=1, cap=20000):
    w = World(side=5, seed=seed, copy_mut=0.0)
    w.inject(genome, "t", cell=0)
    o = w.cells[0]
    log, g, n = [], 0, 0
    while g < gestations and n < cap:
        ip = o.heads[0] % len(o.mem)
        op = OPS[o.mem[ip]]
        before, ins0 = list(o.reg), o.inputs[-2:]
        births = w.births
        w.step(o, 0)
        n += 1
        o = w.cells[0]
        if op not in ("nop-A", "nop-B", "nop-C", "h-copy", "if-label") or "--all" in sys.argv:
            ins = ins0 if op == "IO" else o.inputs[-2:]   # an IO is scored on the inputs read before it
            log.append((g, n, ip, op, list(before), list(o.reg), list(ins), sorted(o.tasks)))
        if w.births > births:
            g += 1
    return log, n


def main():
    path = sys.argv[1]
    rows = json.load(open(path))
    upd = int(sys.argv[sys.argv.index("--update") + 1]) if "--update" in sys.argv else rows[-1]["update"]
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    gest = int(sys.argv[sys.argv.index("--gest") + 1]) if "--gest" in sys.argv else 1
    row = next(r for r in rows if r["update"] == upd)
    gen = parse(row["top"])
    print(f"{path} update {upd}: top genotype, length {len(gen)}, tasks in world now {row['tasks_now']}")
    print("genome:", row["top"])
    log, n = trace(gen, seed, gest)
    print(f"{n} instructions for {gest} gestation(s)")
    for g, k, ip, op, bt, at, ins, tasks in log:
        if len(ins) == 2:
            q, p = ins          # checker: a = inputs[-1], b = inputs[-2]
            pn, qn = NAMES.get(p >> 24, "?"), NAMES.get(q >> 24, "?")
            nm = lambda t: fname(t, p, q, pn, qn)
        else:
            nm = lambda t: f"tt{(t >> 24) & 0xFF:02x}" if t > 0xFFFFFF else str(t)
        desc = " ".join(f"{r}={nm(v)}" for r, v in zip("ABC", bt if op == "IO" else at))
        print(f"g{g} #{k:5d} ip{ip:3d} {op:7s} -> {desc:40s} last2={[NAMES.get(i >> 24, hex(i)) for i in ins]} tasks={tasks}")


if __name__ == "__main__":
    main()
