"""Read out/evo_and.jsonl exactly as PREREG-evo-and.md says (written before the run; this reader written 25.10 during it).
Per seed: AND share of births over the last 1,000 updates (cumulative counters, not the snapshot), class
fixed >= 0.5 / established 0.1-0.5 / background < 0.1, first 250-update checkpoint with share >= 0.5.
A seed restarted after a kill has a second update-0 header: only rows after its LAST header count.
Run: python3 read_evoand.py [UPDATES=40000]"""
import json, sys
UPS = int(sys.argv[1]) if len(sys.argv) > 1 else 40000
runs = {}
for line in open("out/evo_and.jsonl"):
    r = json.loads(line)
    if r["update"] == 0: runs[r["seed"]] = []          # header: start (or restart) of this seed
    else: runs[r["seed"]].append(r)
fixed = done = 0
print(f"seeds seen {len(runs)}: {sorted(runs)}")
for s in sorted(runs):
    rows = runs[s]
    last = rows[-1] if rows else None
    if not last or last["update"] < UPS:
        print(f"seed {s}: INCOMPLETE, last checkpoint {last['update'] if last else 0} of {UPS}"); continue
    done += 1
    base = [r for r in rows if r["update"] == last["update"] - 1000]
    assert base, f"seed {s}: no checkpoint at {last['update'] - 1000}"
    b = base[0]
    share = (last["and_births"] - b["and_births"]) / max(1, last["births"] - b["births"])
    cls = "fixed" if share >= 0.5 else "established" if share >= 0.1 else "background"
    first = next((r["update"] for r in rows if r["and_share_births"] >= 0.5), None)
    fixed += cls == "fixed"
    print(f"seed {s}: AND share last 1000 = {share:.4f} -> {cls}; first 250-window >= 0.5: {first}; "
          f"pop {last['pop']}, AND carriers {last['and']}, genotypes {last['genotypes']}, mean_len {last['mean_len']}")
print(f"complete {done} of {len(runs)}; fixed {fixed} of {done}")
if done == 10:
    v = "mine (lock): fixed <= 1" if fixed <= 1 else "rival: fixed >= 3" if fixed >= 3 else "neither (exactly 2)"
    print("prediction supported:", v)
else:
    print("verdict withheld: the pre-registration counts 10 seeds")
