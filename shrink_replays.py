"""Exploratory (not preregistered), 31.10: is day 2's genome shrinkage (median 99 -> 89) a repeatable outcome of the
day-1 world? The method-1 arms of merit_method.py (seeds 11-32) are reseeded replays of day 2 under Petri's own rule.
Usage: python3 shrink_replays.py > out/shrink_replays.txt"""
import json
W = {json.loads(l)["update"]: json.loads(l)["median_len"] for l in open("daily/series.jsonl")}
print("wild median length at 44k/48k/60k/80k:", [W.get(u) for u in (44000, 48000, 60000, 80000)])
ends = []
for s in range(11, 33):
    r = json.load(open(f"out/mm_1_{s}.json"))["rows"]
    on = next((x["update"] for x in r if x["glen_med"] is not None and x["glen_med"] <= 94), None)
    ends.append(r[-1]["glen_med"]); print(f"seed {s}: median at 80k {r[-1]['glen_med']}, first <= 94 at {on}")
print(f"replays: {len(ends)}; median at 80k <= 90: {sum(e <= 90 for e in ends)}; <= 94: {sum(e <= 94 for e in ends)};"
      f" >= 99: {sum(e >= 99 for e in ends)}")
