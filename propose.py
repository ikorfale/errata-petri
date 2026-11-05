#!/usr/bin/env python3
"""Agent-proposed experiments for Petri (PROPOSE.md): check a proposal, smoke-run it, run it, give the verdict.

  python3 propose.py check prop.json           validate; print the canonical sha256 to post BEFORE any run
  python3 propose.py smoke prop.json           2 paired seeds, side 12, 300 updates: does it execute (no verdict)
  python3 propose.py run prop.json --out DIR   the full run (a lab job when long); writes DIR/rows.jsonl + DIR/verdict.txt

A proposal changes only switches that already exist in petri.World, compares two arms on paired world seeds
(same seed in both arms), reads one census number at the last update, and is judged by a sign count fixed in advance.
"""
import hashlib, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri

# switch -> (type, allowed values or (min, max)); everything else in World stays at its default
SWITCHES = {
    "copy_mut": (float, (0.0, 0.05)),
    "indel": (float, (0.0, 0.5)),
    "slice_": (int, (5, 120)),
    "parasites": (bool, (False, True)),
    "para_global": (bool, (False, True)),
    "age_limit": (bool, (False, True)),
    "age_mode": (str, ("instr", "host", "updates")),
}
CTOR = {"copy_mut", "indel", "slice_", "parasites"}           # passed to World(); the rest are set after it
METRICS = {"pop", "genotypes", "mean_len", "infected", "injections", "secondary", "births"}
TASKS = {"NOT", "NAND", "AND", "ORN", "OR", "ANDN", "NOR", "XOR", "EQU"}
FIELDS = {"title", "author", "question", "control", "treatment", "metric", "direction", "seeds", "updates", "side",
          "held_if", "why_this_could_be_wrong"}
LIMITS = {"seeds": (3, 12), "updates": (100, 3000), "side": (10, 30)}


def metric_names():
    return sorted(METRICS) + [f"task_births.{t}" for t in sorted(TASKS)] + [f"tasks_now.{t}" for t in sorted(TASKS)]


def load(path):
    p = json.load(open(path))
    errs = []
    missing, extra = FIELDS - set(p), set(p) - FIELDS
    if missing:
        errs.append(f"missing fields: {sorted(missing)}")
    if extra:
        errs.append(f"unknown fields (not read, so not allowed): {sorted(extra)}")
    for arm in ("control", "treatment"):
        for k, v in (p.get(arm) or {}).items():
            if k not in SWITCHES:
                errs.append(f"{arm}.{k}: not a switch; allowed {sorted(SWITCHES)}")
                continue
            typ, rng = SWITCHES[k]
            if type(v) is not typ:
                errs.append(f"{arm}.{k}: expected {typ.__name__}, got {type(v).__name__}")
            elif typ in (int, float) and not rng[0] <= v <= rng[1]:
                errs.append(f"{arm}.{k}={v} outside {rng}")
            elif typ in (str, bool) and v not in rng:
                errs.append(f"{arm}.{k}={v!r} not in {rng}")
    if p.get("control") == p.get("treatment"):
        errs.append("control and treatment are the same world")
    if p.get("metric") not in metric_names():
        errs.append(f"metric {p.get('metric')!r} unknown; one of {metric_names()}")
    if p.get("direction") not in ("treatment>control", "treatment<control"):
        errs.append("direction must be 'treatment>control' or 'treatment<control'")
    for k, (lo, hi) in LIMITS.items():
        if not isinstance(p.get(k), int) or not lo <= p[k] <= hi:
            errs.append(f"{k} must be an integer in [{lo}, {hi}]")
    h = p.get("held_if")
    if not isinstance(h, int) or not isinstance(p.get("seeds"), int) or not p["seeds"] // 2 < h <= p["seeds"]:
        errs.append("held_if: number of paired seeds where the direction holds (strict), more than half of seeds")
    if errs:
        sys.exit("proposal rejected:\n- " + "\n- ".join(errs))
    canon = json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    return p, hashlib.sha256(canon).hexdigest()


def world(arm, seed, side):
    w = petri.World(side=side, seed=seed, **{k: v for k, v in arm.items() if k in CTOR})
    for k, v in arm.items():
        if k not in CTOR:
            setattr(w, k, v)
    w.inject(petri.ANCESTOR, "ancestor")
    return w


def read(census, metric):
    if "." in metric:
        part, task = metric.split(".")
        return census[part].get(task, 0)
    return census[metric]


def run(p, seeds, side, updates, out=None):
    rows = []
    for s in seeds:
        r = {"seed": s}
        for arm in ("control", "treatment"):
            t0, w = time.time(), world(p[arm], s, side)
            for _ in range(updates):
                w.run_update()
            r[arm] = read(w.census(), p["metric"])
            r[arm + "_sec"] = round(time.time() - t0, 1)
        r["holds"] = r["treatment"] > r["control"] if p["direction"] == "treatment>control" else r["treatment"] < r["control"]
        rows.append(r)
        print(json.dumps(r), flush=True)
        if out:
            open(os.path.join(out, "rows.jsonl"), "a").write(json.dumps(r) + "\n")
    return rows


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("check", "smoke", "run"):
        sys.exit(__doc__)
    cmd, path = sys.argv[1], sys.argv[2]
    p, sha = load(path)
    print(f"proposal OK: {p['title']} by {p['author']}\nsha256 {sha}")
    if cmd == "check":
        print("post this hash before the run; any later edit changes it")
        return
    if cmd == "smoke":
        run(p, [1, 2], 12, 300)
        print("smoke only: executes, no verdict")
        return
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else sys.exit("run needs --out DIR")
    os.makedirs(out, exist_ok=True)
    if os.path.exists(os.path.join(out, "rows.jsonl")):
        sys.exit(f"{out}/rows.jsonl exists: one run per proposal, never a rerun into the same record")
    seeds = [20261100 + i for i in range(p["seeds"])]          # fixed for every proposal, not chosen per run
    rows = run(p, seeds, p["side"], p["updates"], out)
    k = sum(r["holds"] for r in rows)
    ties = sum(r["treatment"] == r["control"] for r in rows)
    verdict = (f"{'HELD' if k >= p['held_if'] else 'NOT HELD'}: {p['direction']} on {p['metric']} at update "
               f"{p['updates']} in {k} of {len(rows)} paired seeds (needed {p['held_if']}; ties {ties} count as not holding); "
               f"proposal sha256 {sha}")
    open(os.path.join(out, "verdict.txt"), "w").write(verdict + "\n")
    print(verdict)


if __name__ == "__main__":
    main()
