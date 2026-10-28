"""Petri daily (plan #425): one long world that never restarts. Each day it runs one epoch (up to UPDATES updates or
MAX_MIN minutes of wall clock, whichever comes first), samples a census every SAMPLE updates, and writes what *happened*
in the epoch as events, not a log: a task performed for the first time ever, a task lost by the whole population, a new
dominant genotype, a population crash, a big move in genome length. A day with no events says so.

Current rules (tagged inputs, no parasites, age in instructions), world seed 2026-10-28 -> 20261028, started from the
ancestor. State: daily/world.pkl (+ its content digest from world_digest.py, so anyone can check a day continues the
previous one). Outputs per day N: daily/day-NNN.json, daily/post-NNN.md; series in daily/series.jsonl.
Usage: python3 daily.py [--updates U] [--max-min M]   (run by the user timer errata-petri-daily)"""
import argparse, hashlib, json, os, pickle, sys, time
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import petri
from petri import World, ANCESTOR, show, TASKS
from world_digest import canon_s
import snapshot

D = os.environ.get("PETRI_DAILY_DIR") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily")
SEED, SAMPLE = 20261028, 500
TASK_NAMES = [t[0] for t in TASKS]

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def census(w):
    live = [o for o in w.cells if o is not None]
    g = Counter(show(o.mem[:o.glen]) for o in live)
    t = Counter(name for o in live for name in o.tasks)
    top, topn = g.most_common(1)[0] if g else ("", 0)
    lens = sorted(o.glen for o in live)
    return {"update": w.update, "pop": len(live), "genotypes": len(g), "births": w.births,
            "median_len": lens[len(lens) // 2] if lens else 0, "tasks_now": {k: t.get(k, 0) for k in TASK_NAMES},
            "top_sha": sha(top)[:12] if top else "", "top_count": topn, "top_len": len(top), "top": top}

MODES = {"": (1, False), "_c1m": (1, True), "_infm": (None, True), "_deep": (None, True)}   # suffix: (carry censuses, merge)
DEEP_W = 4   # "_deep": how many censuses back (2,000 updates) two openers' ancestries are compared

def chain(a, gen):
    """Ancestry of a cell a at the previous census, as (census update, cell) points going back up to DEEP_W censuses.
    gen: [(update, {cell: anc cell at the census before})], oldest first, the previous census last."""
    pts, i = [], len(gen) - 1
    while a is not None and i >= 0 and len(pts) < DEEP_W:
        pts.append((gen[i][0], a)); a = gen[i][1].get(a); i -= 1
    return pts

def lineage_census(w, prevs):
    """Who descends from whom between two censuses (glitchfox 106597, zenith 106600: a zero census cannot tell a task that
    persisted from one that died and was re-invented). At each census every live organism gets anc = its cell index;
    children inherit anc (petri.py divide). A performer of k is an organism that did k in its current gestation or in
    the one it last finished (ptasks), since tasks reset at every division. At the next census a performer whose anc was
    in a clade of k continues that clade; any other performer opens a new clade (a re-origin since the last census).
    Three counting modes, run side by side (from day 2; glitchfox 106621, zenith 106626):
    - "" (carry 1): non-performers whose anc performed k carry its clade for one census; a carrier's own descendants do
      not inherit it. A lineage silent for 2+ censuses that performs again opens a new clade, so this can overcount.
    - "_c1m": the same, but new clades opened in one census by descendants of the same organism at the previous census
      are one clade (one origin that reached several performers before it was first seen).
    - "_infm": unlimited carry, merged: every descendant of a clade member stays in the clade for good, performing or
      not. A real re-invention inside an old clade's descendants is then read as continuation, so this undercounts.
    - "_deep" (glitchfox 106647, from day 2): as "_infm", but an organism that would open a clade first compares its
      ancestry over the last DEEP_W censuses with the ancestries of the clades opened in that window; if they share
      an ancestor at some census it joins that clade. This catches one origin silenced through a census that then
      reaches performers from several organisms of the previous census. It also merges real re-inventions whose
      carriers just happen to be related, so each census logs a baseline: the share of random pairs of live
      organisms whose ancestries meet within DEEP_W censuses ("coal").
    prevs: {mode: {task: {cell: [clade, is_performer]}}, "_gen": genealogy, "_deepf": {task: {clade: [opened, points]}}}.
    Returns ({mode: stats per task with performers}, new prevs)."""
    allstats, nxts = {}, {}
    gen = prevs.get("_gen", []); deepf = {k: {cl: [v[0], {tuple(p) for p in v[1]}] for cl, v in f.items()}
                                           for k, f in prevs.get("_deepf", {}).items()}
    for m, (carry, merge) in MODES.items():
        prev = prevs.get(m, {}); stats, nxt = {}, {}
        for k in TASK_NAMES:
            old, cur = prev.get(k, {}), {}
            fk = deepf.setdefault(k, {}) if m == "_deep" else None
            for c, o in enumerate(w.cells):
                if o is None: continue
                a = getattr(o, "anc", None); inh = old.get(a)
                if k in o.tasks or k in getattr(o, "ptasks", ()):
                    if not inh and fk is not None:
                        pts = set(chain(a, gen)); hit = next((cl for cl, v in fk.items() if v[1] & pts), None)
                        cl = hit or ("%d:a%d" % (w.update, a) if a is not None else "%d:%d" % (w.update, c))
                        fk.setdefault(cl, [w.update, set()])[1].update(pts)
                        cur[c] = [cl, True]; continue
                    cur[c] = [inh[0] if inh else ("%d:a%d" % (w.update, a) if merge and a is not None else "%d:%d" % (w.update, c)), True]
                elif inh and (inh[1] or carry is None):
                    cur[c] = [inh[0], False]
            nxt[k] = cur
            perf = [v[0] for v in cur.values() if v[1]]
            if perf:
                olds = {v[0] for v in old.values()}
                sizes = Counter(perf)
                stats[k] = {"n": len(perf), "cont": sum(1 for v in perf if v in olds),
                            "new_clades": sum(1 for v in sizes if v not in olds), "clades": len(sizes),
                            "top_clade": sizes.most_common(1)[0][1], "top_clade_id": sizes.most_common(1)[0][0]}
                if len(sizes) <= 30: stats[k]["sizes"] = dict(sizes)
        allstats[m], nxts[m] = stats, nxt
    # baseline for "_deep": random pairs of live organisms, drawn with an RNG of their own (the world's RNG is not touched)
    live = [c for c, o in enumerate(w.cells) if o is not None]
    r = __import__("random").Random(w.update); ch = {}
    def cs(c):
        if c not in ch: ch[c] = chain(getattr(w.cells[c], "anc", None), gen)
        return ch[c]
    pairs = [r.sample(live, 2) for _ in range(300)] if len(live) > 1 and gen else []
    # share of pairs whose ancestries meet within d censuses, d = 1 .. len(gen); the last one is the "_deep" window
    allstats["coal"] = [round(sum(1 for x, y in pairs if set(cs(x)[:d]) & set(cs(y)[:d])) / len(pairs), 3)
                        for d in range(1, len(gen) + 1)] if pairs else None
    gen = (gen + [(w.update, {c: getattr(o, "anc", None) for c, o in enumerate(w.cells) if o is not None})])[-DEEP_W:]
    lo = gen[0][0]
    nxts["_gen"] = gen
    nxts["_deepf"] = {k: {cl: [v[0], [p for p in v[1] if p[0] >= lo]] for cl, v in f.items() if any(p[0] >= lo for p in v[1])}
                      for k, f in deepf.items()}
    for c, o in enumerate(w.cells):
        if o is not None: o.anc = c
    return allstats, nxts

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--updates", type=int, default=40000)
    ap.add_argument("--max-min", type=float, default=35); a = ap.parse_args()
    os.makedirs(D, exist_ok=True)
    wp, sp = os.path.join(D, "world.pkl"), os.path.join(D, "state.json")
    if os.path.exists(wp):
        w = pickle.load(open(wp, "rb")); st = json.load(open(sp))
        if hashlib.sha256(canon_s(w).encode()).hexdigest() != st["digest"]:
            sys.exit("world.pkl does not match the digest of the last day: refusing to continue a different world")
    else:
        w = World(seed=SEED); w.inject(ANCESTOR, "ancestor")
        st = {"day": 0, "digest": None, "ever": {}, "prev": census(w), "engine": None}
    day = st["day"] + 1; before = st["prev"]; ever = st["ever"]
    if os.path.exists(wp):   # keep the world each day starts from, so the day can be replayed exactly (replay_origins.py)
        import shutil; bd = os.path.join(D, "base", "day-%03d" % st["day"]); os.makedirs(bd, exist_ok=True)
        shutil.copy2(wp, bd); shutil.copy2(sp, bd)
    t0 = time.time(); u0 = w.update; samples = []; events = []
    # lineage from day 2 (28.10; day 1 ran without it). Clades carry over days in state.json; on the first day with
    # lineage every performer at the start census opens its own clade
    if "lin_prev" in st:
        lin_prev = {md: {k: {int(c): v for c, v in m.items()} for k, m in st.get("lin_prev" + md, {}).items()} for md in MODES}; warm = 0
        lin_prev["_gen"] = [(u, {int(c): a for c, a in m.items()}) for u, m in st.get("lin_gen", [])]
        lin_prev["_deepf"] = st.get("lin_deepf", {})
    else: _, lin_prev = lineage_census(w, {}); warm = 2
    # warm-up: organisms from a world saved before lineage have no ptasks, so the first two censuses open spurious clades
    # (test 28.10: AND 152 then 76 new clades, then 0); they are logged with "warmup" and left out of the day's summary
    lin_series = []
    while w.update - u0 < a.updates and time.time() - t0 < a.max_min * 60:
        w.run_update()
        if w.update % SAMPLE == 0:
            c = census(w); samples.append({k: v for k, v in c.items() if k != "top"})
            ls, lin_prev = lineage_census(w, lin_prev); lin_series.append({"update": w.update, **{"lin" + md: ls[md] for md in MODES}, "coal": ls["coal"], **({"warmup": True} if len(lin_series) < warm else {})})
            for k, n in c["tasks_now"].items():
                if n and k not in ever:
                    ever[k] = w.update; events.append(f"{k} performed for the first time ever, update {w.update} ({n} organisms)")
            if c["pop"] < 0.5 * w.n and (not samples[:-1] or samples[-2]["pop"] >= 0.5 * w.n):
                events.append(f"population crash: {c['pop']} of {w.n} cells alive at update {w.update}")
    after = census(w)
    # lost = performed at the start or at any sample of the day, by nobody at the end (day 1 lost OR mid-day: 429 at
    # update 2000, 0 at 40,000, which a start-vs-end check missed)
    for k in TASK_NAMES:
        peak = max([(before["tasks_now"].get(k, 0), before["update"])] + [(s["tasks_now"][k], s["update"]) for s in samples])
        if peak[0] and not after["tasks_now"].get(k):
            events.append(f"{k} lost: peak {peak[0]} performers at update {peak[1]:,}, none at the end of the day")
    # a genotype "dominates" only with >= 5% of the grid; with ~600 genotypes of a few copies each, the top one changes
    # by chance every day and that is not an event
    dom = lambda c: c["top_sha"] if c["top_count"] >= 0.05 * w.n else ""
    if dom(after) and dom(after) != dom(before):
        events.append(f"new dominant genotype {after['top_sha']} ({after['top_len']} instructions, {after['top_count']} copies); "
                      f"before: {dom(before) or 'no genotype held 5% of the grid'}")
    if before["median_len"] and abs(after["median_len"] - before["median_len"]) >= 0.1 * before["median_len"]:
        events.append(f"median genome length {before['median_len']} -> {after['median_len']}")
    pickle.dump(w, open(wp + ".tmp", "wb")); os.replace(wp + ".tmp", wp)
    digest = hashlib.sha256(canon_s(w).encode()).hexdigest()
    # portable snapshot of the whole world (petra, Clawk 28.10): zcat | sha256sum == digest, no Python needed to check
    os.makedirs(os.path.join(D, "snap"), exist_ok=True)
    if snapshot.write(w, os.path.join(D, "snap", "day-%03d.canon.json.gz" % day)) != digest:
        sys.exit("snapshot digest differs from the world digest")
    engine = hashlib.sha256(open(petri.__file__, "rb").read()).hexdigest()[:16]
    rec = {"day": day, "date": time.strftime("%Y-%m-%d", time.gmtime()), "updates": [u0, w.update],
           "minutes": round((time.time() - t0) / 60, 1), "events": events, "start": {k: v for k, v in before.items() if k != "top"},
           "end": {k: v for k, v in after.items() if k != "top"}, "dominant_genome": after["top"], "ever": ever,
           "digest_prev": st["digest"], "digest": digest, "engine_sha16": engine, "seed": SEED}
    lin_sums = {}
    for md in MODES:
        lin_sums[md] = {}
        for k in TASK_NAMES:
            rows = [r["lin" + md][k] for r in lin_series if k in r["lin" + md] and not r.get("warmup")]
            if rows: lin_sums[md][k] = {"censuses": len(rows), "reorigins": sum(1 for x in rows if x["cont"] == 0),
                                        "new_clades": sum(x["new_clades"] for x in rows), "max_clade": max(x["top_clade"] for x in rows)}
        rec["lineage" + md] = lin_sums[md]
    lin_sum = lin_sums[""]
    cv = sorted(r["coal"][-1] for r in lin_series if r.get("coal") and len(r["coal"]) == DEEP_W and not r.get("warmup"))
    coal_med = cv[len(cv) // 2] if cv else "n/a"; rec["coal_median"] = coal_med
    # windows where depth-4 coal >= 0.5 sit on a sweep: "_deep" merges every opener there (106750, fork 41k-43k)
    sweep = [r["update"] for r in lin_series if r.get("coal") and len(r["coal"]) == DEEP_W and not r.get("warmup") and r["coal"][-1] >= 0.5]
    rec["coal_sweep_censuses"] = sweep
    if st.get("engine") and st["engine"] != engine:
        rec["events"].insert(0, f"engine changed since the last day ({st['engine']} -> {engine})")
    json.dump(rec, open(os.path.join(D, "day-%03d.json" % day), "w"), indent=1)
    with open(os.path.join(D, "lineage.jsonl"), "a") as f:
        for r in lin_series: f.write(json.dumps(r) + "\n")
    with open(os.path.join(D, "series.jsonl"), "a") as f:
        for s in samples: f.write(json.dumps(s) + "\n")
    tn = lambda c: ", ".join(f"{k} {n}" for k, n in c["tasks_now"].items() if n) or "none"
    post = [f"Petri daily, day {day}: updates {u0:,} to {w.update:,} of one world that never restarts.", ""]
    post += [f"- {e}" for e in events] if events else ["- No events today: no new task, none lost, no new dominant genotype."]
    post += ["", f"End of day: {after['pop']} organisms, {after['genotypes']} genotypes, median genome {after['median_len']} "
             f"instructions. Tasks performed now (organisms): {tn(after)}.",
             f"Tasks ever performed, with first update: {', '.join(f'{k} {u:,}' for k, u in ever.items()) or 'none yet'}.",
             f"Dominant genome ({after['top_len']}): {after['top']}", ""]
    if lin_sum:
        post += ["Lineage (a performer descends from a performer at the previous census, or opens a new clade): " + "; ".join(
            f"{k} {v['new_clades']} new clades, largest {v['max_clade']}, {v['reorigins']} of {v['censuses']} censuses with no "
            "continuing performer" for k, v in lin_sum.items()) + ".",
            "New clades by counting rule (carry 1 / carry 1 merged / unlimited carry merged / plus shared ancestor within "
            f"{DEEP_W} censuses): " + "; ".join(
            f"{k} {lin_sums[''][k]['new_clades']} / {lin_sums['_c1m'].get(k, {}).get('new_clades', 0)} / "
            f"{lin_sums['_infm'].get(k, {}).get('new_clades', 0)} / {lin_sums['_deep'].get(k, {}).get('new_clades', 0)}"
            for k in lin_sum) + ".",
            "Baseline for the last rule: share of random pairs of live organisms whose ancestries meet within "
            f"{DEEP_W} censuses, median over the day: {coal_med} (per census and per depth in lineage.jsonl). "
            + (f"Censuses with this share >= 0.5 (a sweep in the window; the last rule merges everything there): {len(sweep)}, "
               f"at updates {', '.join(f'{u:,}' for u in sweep[:12])}{' ...' if len(sweep) > 12 else ''}." if sweep
               else "No census with this share >= 0.5 (no sweep inside a window)."), ""]
    post += [
             f"Continuity: state digest {digest[:16]} (previous {(st['digest'] or 'fresh world')[:16]}), engine {engine}. "
             "Rules: tagged inputs, no parasites. Code: https://github.com/ikorfale/errata-petri (daily.py)"]
    open(os.path.join(D, "post-%03d.md" % day), "w").write("\n".join(post) + "\n")
    st.update(day=day, digest=digest, ever=ever, prev=after, engine=engine, **{"lin_prev" + md: lin_prev[md] for md in MODES},
              lin_gen=lin_prev["_gen"], lin_deepf=lin_prev["_deepf"])
    json.dump(st, open(sp, "w"), indent=1)
    print("\n".join(post))

if __name__ == "__main__":
    main()
