"""theone 99870: rebuild epoch 1 from its recipe (World(seed=2026), ancestor, 2000 updates, current petri.py) and judge it
against the frozen out/epoch1_world.pkl with world_digest.compare. Writes out/rebuild_check.json (verdict, differing
fields, the exception used, engine and digest revisions)."""
import json, pickle
from petri import World, ANCESTOR
from world_digest import compare
frozen = pickle.load(open('out/epoch1_world.pkl', 'rb'))
w = World(seed=2026); w.inject(ANCESTOR, "ancestor")
for _ in range(2000): w.run_update()
v = compare(frozen, w); json.dump(v, open('out/rebuild_check.json', 'w'), indent=1); print(json.dumps(v))
