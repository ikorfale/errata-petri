"""E2 verdict, mechanical (PREREG-E2.md). Written before any E2 job ran.
usage: python3 e2_verdict.py out/e2_a.jsonl out/e2_b.jsonl out/e1_a.jsonl out/e1_b.jsonl
Outcomes as in E1 (established = infected >= 45 at +3000, extinct = 0, else unresolved). L50 per mode with E1's rules
(logistic MLE; complete separation -> interval (largest L with an established world, next arm]; quasi-separation ->
interpolated share-0.5 crossing). E1 reference L50 = 26.88. A shift counts as >= 3 only if the whole L50 interval is >= 29.88.
Local arms reproduce E1 world for world (same seeds, same RNG); any mismatch is a bug: exit 1 before any L50.
Second-model review (Fable 23.10) before any data: E1 files required; shift judged on a seed-cluster bootstrap interval
(2000 resamples; each resample's L50 interval, separation included; CI = 2.5% of lows to 97.5% of highs); complete
separation upper bound = smallest extinct L; 'crowding' named only if occupied-host failures are >= 50% of failed
injections in local mode and < 10% in global, otherwise a supported shift is reported as 'spatial structure'."""
import json, random, sys
from collections import defaultdict
from e1_verdict import fit, EST, load as load_e1

REF = 26.88


def outcome(r):
    last = r["census"][-1] if r["census"] else None
    if last and last["inf"] == 0: return "extinct"
    if last and last["u"] - r["census"][0]["u"] + 250 == r["upd"] and last["inf"] >= EST: return "established"
    return "unresolved"


def l50(ws):
    """ws: [(L, outcome)] -> (lo, hi) interval or None, plus a note."""
    xy = [(L, 1 if o == "established" else 0) for L, o in ws if o != "unresolved"]
    est = [L for L, y in xy if y]; ext = [L for L, y in xy if not y]; Ls = sorted({L for L, _ in ws})
    if not est or not ext: return None, "no established" if not est else "no extinct (L50 above the largest arm)"
    if min(est) >= max(ext) and not (min(est) == max(ext)): return None, "reversed separation"
    if max(est) < min(ext):
        return (max(est), min(ext)), "complete separation"
    if max(est) == min(ext) and sum(1 for L in Ls if L == max(est)) == 1 and all(
            (y == 1) if L < max(est) else (y == 0) if L > max(est) else True for L, y in xy):
        sh = []
        for L in Ls:
            ys = [y for x, y in xy if x == L]
            if ys: sh.append((L, sum(ys) / len(ys)))
        c = next((L1 + (L2 - L1) * (s1 - .5) / (s1 - s2) for (L1, s1), (L2, s2) in zip(sh, sh[1:]) if s1 >= .5 > s2), None)
        return ((c, c) if c is not None else None), "quasi-separation, interpolated"
    ab = fit([x for x, _ in xy], [y for _, y in xy])
    if ab is None or ab[1] == 0: return None, "fit failed"
    v = -ab[0] / ab[1]; return (v, v), f"logistic a={ab[0]:.3f} b={ab[1]:.4f}"


def boot(ws, n=2000):
    seeds = sorted({r["seed"] for _, _, r in ws}); rng = random.Random(20261023); lo, hi = [], []
    for _ in range(n):
        pick = [rng.choice(seeds) for _ in seeds]
        iv, _ = l50([(L, o) for s in pick for L, o, r in ws if r["seed"] == s])
        if iv is None: return None                   # a resample with no L50 at all: interval undetermined
        lo.append(iv[0]); hi.append(iv[1])
    lo.sort(); hi.sort(); return (lo[int(.025 * n)], hi[int(.975 * n) - 1])


def main(a):
    rows = [json.loads(l) for p in a[:2] for l in open(p)]
    worlds = [r for r in rows if "warm" not in r]
    by = defaultdict(list); fails = defaultdict(lambda: defaultdict(int)); lost = defaultdict(lambda: defaultdict(int)); h = defaultdict(list)
    for r in worlds:
        by[r["mode"]].append((r["L"], outcome(r), r))
        for k, v in r["inj_fail"].items(): fails[r["mode"]][k] += v
        for k, v in r["para_lost"].items(): lost[r["mode"]][k] += v
        h[r["mode"]].append(r["h_arm"])
    print(f"worlds: {len(worlds)} (expected {14 * 17})")
    if len(a) != 4: sys.exit("need the two E2 and the two E1 files")
    if True:
        _, e1 = load_e1(a[2:4]); ref = {(w["seed"], w["L"]): (w["outcome"], w["inf"]) for w in e1}
        mm = [(r["seed"], L) for L, o, r in by["local"] if ref.get((r["seed"], L)) != (o, r["census"][-1]["inf"] if r["census"] else None)]
        print(f"local arms matching E1 world for world: {len(by['local']) - len(mm)}/{len(by['local'])}")
        if mm or not by["local"]: print(f"MISMATCH {mm[:10]}: verdict void"); sys.exit(1)
    res = {}
    for m in ("local", "global", "noage"):
        ws = by[m]; print(f"\nmode {m}: mean h_arm {sum(h[m]) / max(len(h[m]), 1):.4f}")
        print("  L   est ext unres")
        for L in sorted({L for L, _, _ in ws}):
            c = [o for x, o, _ in ws if x == L]
            print(f"  {L:<3} {c.count('established'):>3} {c.count('extinct'):>3} {c.count('unresolved'):>5}")
        iv, note = l50([(L, o) for L, o, _ in ws])
        bs = boot(ws); res[m] = bs
        tf = sum(fails[m].values()); tl = sum(lost[m].values())
        print(f"  L50 {iv if iv is None else tuple(round(x, 2) for x in iv)} ({note}); bootstrap interval {bs if bs is None else tuple(round(x, 2) for x in bs)}")
        print(f"  failed injections {tf}: " + ", ".join(f"{k} {v / tf:.1%}" for k, v in sorted(fails[m].items())) if tf else "  failed injections 0")
        print(f"  parasites lost with host {tl}: " + ", ".join(f"{k} {v / tl:.1%}" for k, v in sorted(lost[m].items())) if tl else "  parasites lost 0")
    def shift(iv):
        if iv is None: return "undetermined"
        return ">=3" if iv[0] >= REF + 3 else "<3" if iv[1] < REF + 3 else "straddles 3"
    g, n = shift(res["global"]), shift(res["noage"])
    occ = {m: fails[m].get("occupied", 0) / max(sum(fails[m].values()), 1) for m in ("local", "global")}
    print(f"occupied-host share of failed injections: local {occ['local']:.1%}, global {occ['global']:.1%}")
    name = "crowding by occupied neighbours" if occ["local"] >= .5 and occ["global"] < .1 else "spatial structure"
    print(f"\nshift vs E1 L50 {REF}: global {g}, noage {n}")
    print(f"crowding (second model): {'supported, as ' + name if g == '>=3' else 'falsified as the main cause' if g == '<3' else 'undecided'}")
    print("old age (mine, post hoc):", "supported" if n == ">=3" else "not material" if n == "<3" else "undecided")
    if res["global"] and g == ">=3":
        inB = 32 <= res["global"][0] and res["global"][1] <= 40
        print(f"global L50 inside E1 band B [32,40] (measured-h mean field): {inB}")


if __name__ == "__main__":
    main(sys.argv[1:])
