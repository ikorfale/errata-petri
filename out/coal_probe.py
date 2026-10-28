# #554: why is coal 0.82-1.0 in the first 2,000 updates after the day-1 state? Fork (seed 777), census every 500.
import pickle, random, sys, json
from collections import Counter
sys.path.insert(0, '.')
import daily
w = pickle.load(open('daily/world.pkl', 'rb')); w.rng = random.Random(777)
prevs = {}
for step in range(int(sys.argv[1]) if len(sys.argv) > 1 else 8):
    if step:
        for _ in range(500): w.run_update()
    live = [o for o in w.cells if o is not None]
    ancs = Counter(getattr(o, 'anc', None) for o in live)
    born = Counter(o.born >= w.update - 500 for o in live)
    gen = prevs.get('_gen', [])
    ls, prevs = daily.lineage_census(w, prevs)
    print(json.dumps({"u": w.update, "live": len(live), "anc_distinct": len(ancs), "anc_top": ancs.most_common(3),
                      "born_last500": born[True], "gen_len": len(gen), "coal": ls["coal"]}), flush=True)
