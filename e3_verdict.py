"""E3 verdict, mechanical (PREREG-E3.md). Written 27.10 before any E3 world ran.
usage: python3 e3_verdict.py out/e3_a.jsonl out/e3_b.jsonl out/e2_a.jsonl out/e2_b.jsonl
Anchor: E3 local arms must equal E2 local arms world for world (outcome and final infected count), else exit 1.
Outcomes, L50 and the seed-cluster bootstrap interval are e2_verdict.py's. REF = 26.88 (E1), NOAGE = 31.52 (E2)."""
import json, sys
from collections import defaultdict
from e2_verdict import outcome, l50, boot

REF, NOAGE = 26.88, 31.52


def main(a):
    if len(a) != 4: sys.exit("need the two E3 and the two E2 files")
    rows = lambda ps: [r for p in ps for l in open(p) for r in [json.loads(l)] if "warm" not in r]
    e3, e2 = rows(a[:2]), rows(a[2:])
    ref = {(r["seed"], r["L"]): (outcome(r), r["census"][-1]["inf"] if r["census"] else None) for r in e2 if r["mode"] == "local"}
    by = defaultdict(list); lost = defaultdict(lambda: defaultdict(int))
    for r in e3:
        by[r["mode"]].append((r["L"], outcome(r), r))
        for k, v in r["para_lost"].items(): lost[r["mode"]][k] += v
    print(f"worlds: {len(e3)} (expected {14 * 14})")
    mm = [(r["seed"], L) for L, o, r in by["local"] if ref.get((r["seed"], L)) != (o, r["census"][-1]["inf"] if r["census"] else None)]
    print(f"local arms matching E2 world for world: {len(by['local']) - len(mm)}/{len(by['local'])}")
    if mm or not by["local"]: print(f"MISMATCH {mm[:10]}: verdict void"); sys.exit(1)
    res = {}
    for m in ("local", "host", "updates"):
        ws = by[m]; print(f"\nmode {m}\n  L   est ext unres")
        for L in sorted({L for L, _, _ in ws}):
            c = [o for x, o, _ in ws if x == L]
            print(f"  {L:<3} {c.count('established'):>3} {c.count('extinct'):>3} {c.count('unresolved'):>5}")
        iv, note = l50([(L, o) for L, o, _ in ws]); res[m] = (iv, boot(ws))
        tl = sum(lost[m].values())
        print(f"  L50 {iv if iv is None else tuple(round(x, 2) for x in iv)} ({note}); bootstrap {res[m][1] if res[m][1] is None else tuple(round(x, 2) for x in res[m][1])}")
        print(f"  parasites lost with host {tl}: " + ", ".join(f"{k} {v / tl:.1%}" for k, v in sorted(lost[m].items())) if tl else "  parasites lost 0")
    def shift(iv):
        if iv is None: return "undetermined"
        return ">=3" if iv[0] >= REF + 3 else "<3" if iv[1] < REF + 3 else "straddles 3"
    hs, us = shift(res["host"][1]), shift(res["updates"][1])
    print(f"\nshift vs E1 L50 {REF}: host {hs}, updates {us}")
    print("H1 (parasite steps age the host):", "supported" if hs == ">=3" else "falsified as the main cause" if hs == "<3" else "undecided")
    print("H2 (updates-age equals instruction-age for this question):", "holds" if us == "<3" else "fails" if us == ">=3" else "undecided")
    if res["host"][0]:
        p = sum(res["host"][0]) / 2; print(f"descriptive: share of the noage shift reproduced by host mode = {(p - REF) / (NOAGE - REF):.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
