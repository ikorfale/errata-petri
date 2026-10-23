"""theone 98607 ablation: is v1's survival advantage in the epoch-1 world caused by the AND merit bonus?
Same frozen world (out/epoch1_world.pkl), same v1 genome, same insertion seeds 101-120 as epoch_probe20; the only change
is that the probe lineage's AND bonus (x2^2) is neutralised at division. Everyone else keeps every bonus.
Prediction written before the run (23.10): if the bonus causes the advantage, survival at 300 updates falls from 14/20
toward the no-bonus control (1/20); if it stays near 14/20, the advantage comes from elsewhere (copy speed, placement).
Usage: and_ablation.py RNGSEED [UPDATES]"""
import json, pickle, random, sys
from petri import parse
V1 = 'wzcagcyryuopcuymccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccczvfcaxgab'  # as in epoch_probe.py
rs = int(sys.argv[1]); UPS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
w = pickle.load(open('out/epoch1_world.pkl', 'rb')); w.rng = random.Random(rs)
orig = w.divide.__func__
def divide(self, o, c):
    if o.lineage != 'probe' or 'AND' not in o.tasks: return orig(self, o, c)
    o.tasks.discard('AND')            # tasks are cleared at restart anyway; AND births of the probe go uncounted
    return orig(self, o, c)
w.divide = divide.__get__(w)
w.inject(parse(V1), 'probe')
for u in range(1, UPS + 1):
    w.run_update()
    if u in (100, 250, 500, 1000, UPS):
        live = [o for o in w.cells if o is not None]; n = sum(o.lineage == 'probe' for o in live)
        print(json.dumps({"arm": "v1-noAND", "rs": rs, "after": u, "probe": n, "pop": len(live)}), flush=True)
        if n == 0: break
