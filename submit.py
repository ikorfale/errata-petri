"""Seeding Petri: a strict parser, a viability check and a per-epoch registry.

  python3 submit.py check FILE [--preview]           parse + viability (+ head-to-head share vs the ancestor)
  python3 submit.py add FILE --agent NAME --epoch N  check, then record in submissions/epoch-N.jsonl

A genome is either one word of op letters (see LETTERS in SUBMIT.md) or op names separated by
spaces, commas or newlines. Lines starting with # are comments. Nothing else is accepted: an
unknown name or letter is an error with its position, never skipped.
"""
import hashlib, json, os, sys
from petri import CH, CODE, OPS, World, show

MIN_LEN, MAX_LEN = 10, 256
INJECT = CODE["inject"]


class Reject(ValueError):
    pass


def parse_strict(text, parasites=False):
    lines = [l.split("#", 1)[0] for l in text.splitlines()]
    words = " ".join(lines).replace(",", " ").split()
    if not words:
        raise Reject("empty genome")
    if len(words) == 1 and words[0] not in CODE:
        w = words[0]
        bad = [(i, ch) for i, ch in enumerate(w) if ch not in CH]
        if bad:
            raise Reject(f"unknown letter {bad[0][1]!r} at position {bad[0][0] + 1}")
        g = [CH.index(ch) for ch in w]
    else:
        bad = [(i, w) for i, w in enumerate(words) if w not in CODE]
        if bad:
            raise Reject(f"unknown op {bad[0][1]!r} at word {bad[0][0] + 1}")
        g = [CODE[w] for w in words]
    if not MIN_LEN <= len(g) <= MAX_LEN:
        raise Reject(f"length {len(g)}: a genome must have {MIN_LEN} to {MAX_LEN} instructions")
    if INJECT in g and not parasites:
        raise Reject("'inject' (A) is only allowed in epochs with parasites on")
    return g


def viable(g, updates=400, births=3):
    """Alone in an empty 10x10 world without mutation: does it make `births` children in time,
    and is the first child an exact copy? Seeds that cannot reproduce are refused."""
    w = World(side=10, seed=0, copy_mut=0.0, parasites=INJECT in g)
    w.indel = 0.0
    c = w.inject(list(g), "check", cell=0)
    first = None
    for u in range(updates):
        w.run_update()
        if first is None and w.births:
            kid = next(o for i, o in enumerate(w.cells) if o is not None and i != c)
            first = {"update": u + 1, "exact": list(kid.mem) == list(g), "child_len": len(kid.mem)}
        if w.births >= births:
            break
    return {"viable": w.births >= births, "births": w.births, "first_child": first}


def preview(g, seeds=(1, 2), updates=300):
    """Not a gate: the seed against the ancestor on a 20x20 grid, mutation off. Share of cells
    held by the seed's lineage at the end, per world seed. Tells a player how their design
    fares head to head before the epoch, nothing more."""
    from petri import ANCESTOR
    out = []
    for s in seeds:
        w = World(side=20, seed=s, copy_mut=0.0, parasites=INJECT in g)
        w.indel = 0.0
        w.inject(list(ANCESTOR), "ancestor", cell=0)
        w.inject(list(g), "seed", cell=210)
        for _ in range(updates):
            w.run_update()
        live = [o.lineage for o in w.cells if o is not None]
        out.append(round(live.count("seed") / max(1, len(live)), 2))
    return out


def digest(g):
    return hashlib.sha256(show(g).encode()).hexdigest()


def check(text, parasites=False):
    try:
        g = parse_strict(text, parasites)
    except Reject as e:
        return {"ok": False, "reason": str(e)}
    v = viable(g)
    out = {"ok": v["viable"], "length": len(g), "letters": show(g), "sha256": digest(g), **v}
    if not v["viable"]:
        out["reason"] = f"made {v['births']} children in 400 updates alone (needs 3)"
    return out


def add(text, agent, epoch, parasites=False, root="submissions"):
    r = check(text, parasites)
    if not r["ok"]:
        return r
    os.makedirs(root, exist_ok=True)
    path = os.path.join(root, f"epoch-{epoch}.jsonl")
    rows = [json.loads(l) for l in open(path)] if os.path.exists(path) else []
    if any(x["agent"] == agent for x in rows):
        return {"ok": False, "reason": f"{agent} already seeded epoch {epoch} (one seed per agent per epoch)"}
    if any(x["sha256"] == r["sha256"] for x in rows):
        return {"ok": False, "reason": "the same genome is already seeded this epoch"}
    row = {"agent": agent, "epoch": epoch, "sha256": r["sha256"], "letters": r["letters"],
           "length": r["length"]}
    with open(path, "a") as f:
        f.write(json.dumps(row) + "\n")
    return {**r, "recorded": path}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "add"])
    ap.add_argument("file")
    ap.add_argument("--agent")
    ap.add_argument("--epoch", type=int)
    ap.add_argument("--parasites", action="store_true")
    ap.add_argument("--preview", action="store_true", help="also: share against the ancestor head to head")
    a = ap.parse_args()
    text = open(a.file).read()
    if a.cmd == "check":
        r = check(text, a.parasites)
        if a.preview and r["ok"]:
            r["share_vs_ancestor"] = preview(parse_strict(text, a.parasites))
    else:
        if not a.agent or a.epoch is None:
            sys.exit("add needs --agent and --epoch")
        r = add(text, a.agent, a.epoch, a.parasites)
    print(json.dumps(r, indent=1))
    sys.exit(0 if r["ok"] else 1)
