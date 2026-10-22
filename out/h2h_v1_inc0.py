"""zenith #98438: v1 vs top epoch-1 incumbent head to head, 20x20, mutation off, 300 updates, seeds 1-4."""
import json, time
from petri import World, parse
V1 = 'wzcagcyryuopcuymccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccczvfcaxgab'
INC = json.load(open('out/epoch1_incumbents.json'))['top'][0]['genome']
import sys
SWAP = int(sys.argv[1]) if len(sys.argv) > 1 else 0
for s in (1, 2, 3, 4):
    w = World(side=20, seed=s, copy_mut=0.0, parasites=False); w.indel = 0.0
    a, b = (0, 210) if SWAP == 0 else (210, 0); w.inject(parse(INC), "inc0", cell=a); w.inject(parse(V1), "v1", cell=b)
    for u in range(300):
        w.run_update()
        if u + 1 in (100, 300):
            live = [o.lineage for o in w.cells if o is not None]
            print(s, u + 1, len(live), "v1 share", round(live.count("v1") / max(1, len(live)), 2), flush=True)
