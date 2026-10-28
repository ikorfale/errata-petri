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
    t0 = time.time(); u0 = w.update; samples = []; events = []
    while w.update - u0 < a.updates and time.time() - t0 < a.max_min * 60:
        w.run_update()
        if w.update % SAMPLE == 0:
            c = census(w); samples.append({k: v for k, v in c.items() if k != "top"})
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
    if st.get("engine") and st["engine"] != engine:
        rec["events"].insert(0, f"engine changed since the last day ({st['engine']} -> {engine})")
    json.dump(rec, open(os.path.join(D, "day-%03d.json" % day), "w"), indent=1)
    with open(os.path.join(D, "series.jsonl"), "a") as f:
        for s in samples: f.write(json.dumps(s) + "\n")
    tn = lambda c: ", ".join(f"{k} {n}" for k, n in c["tasks_now"].items() if n) or "none"
    post = [f"Petri daily, day {day}: updates {u0:,} to {w.update:,} of one world that never restarts.", ""]
    post += [f"- {e}" for e in events] if events else ["- No events today: no new task, none lost, no new dominant genotype."]
    post += ["", f"End of day: {after['pop']} organisms, {after['genotypes']} genotypes, median genome {after['median_len']} "
             f"instructions. Tasks performed now (organisms): {tn(after)}.",
             f"Tasks ever performed, with first update: {', '.join(f'{k} {u:,}' for k, u in ever.items()) or 'none yet'}.",
             f"Dominant genome ({after['top_len']}): {after['top']}", "",
             f"Continuity: state digest {digest[:16]} (previous {(st['digest'] or 'fresh world')[:16]}), engine {engine}. "
             "Rules: tagged inputs, no parasites. Code: https://github.com/ikorfale/errata-petri (daily.py)"]
    open(os.path.join(D, "post-%03d.md" % day), "w").write("\n".join(post) + "\n")
    st.update(day=day, digest=digest, ever=ever, prev=after, engine=engine)
    json.dump(st, open(sp, "w"), indent=1)
    print("\n".join(post))

if __name__ == "__main__":
    main()
