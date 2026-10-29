# Clawk (gavinagent, cosmo 28.10): does the portable canon snapshot alone reproduce the world, without the pickle?
# Load day-001.canon.json.gz and daily/world.pkl, check both have the recorded digest, run 500 updates from each, compare.
import pickle, json, hashlib, sys
sys.path.insert(0, '.')
import snapshot
from world_digest import canon_s
d = lambda w: hashlib.sha256(canon_s(w).encode()).hexdigest()
rec = json.load(open('daily/day-001.json'))['digest']
a = pickle.load(open('daily/world.pkl', 'rb')); b = snapshot.load('daily/snap/day-001.canon.json.gz')
print('recorded', rec[:16], 'pickle', d(a)[:16], 'snapshot', d(b)[:16], 'zcat', snapshot.digest('daily/snap/day-001.canon.json.gz')[:16])
for _ in range(500): a.run_update(); b.run_update()
print('after 500 updates: pickle', d(a)[:16], 'snapshot', d(b)[:16], 'update', a.update, b.update, 'equal', d(a) == d(b))
