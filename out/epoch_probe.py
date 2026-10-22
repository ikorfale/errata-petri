"""zenith #98438 follow-up: drop one copy of a genome into the real epoch-1 world (out/epoch1_world.pkl, update 2000,
mutation on as in the epoch) and count its lineage. Arms: v1, and the top incumbent as a no-bonus control dropped the
same way. Usage: epoch_probe.py ARM RNGSEED"""
import json, pickle, random, sys
from petri import parse
V1 = 'wzcagcyryuopcuymccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccczvfcaxgab'
INC = json.load(open('out/epoch1_incumbents.json'))['top'][0]['genome']
arm, rs = sys.argv[1], int(sys.argv[2])
w = pickle.load(open('out/epoch1_world.pkl', 'rb')); w.rng = random.Random(rs)
w.inject(parse(V1 if arm == 'v1' else INC), 'probe')
UPS = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
for u in range(1, UPS + 1):
    w.run_update()
    if u in (100, 250, 500, 1000, UPS):
        live = [o for o in w.cells if o is not None]; n = sum(o.lineage == 'probe' for o in live)
        print(json.dumps({"arm": arm, "rs": rs, "after": u, "probe": n, "pop": len(live)}), flush=True)
        if n == 0: break
