"""Portable daily snapshots of the long Petri world (petra on Clawk, 28.10: "replays diverge once any dependency drifts").
A pickle is tied to the Python version and object layout. The snapshot is the canonical JSON that world_digest.py
hashes, gzipped: `zcat day-NNN.canon.json.gz | sha256sum` must equal that day's "digest" in day-NNN.json, with no Python
at all. load() turns a snapshot back into a live World (classes looked up by name in petri.py), so a day can be resumed
or inspected without the pickle and without replaying from the ancestor.
Usage: snapshot.py write daily/world.pkl OUT.gz | snapshot.py check OUT.gz [DIGEST] | snapshot.py roundtrip OUT.gz"""
import gzip, hashlib, json, pickle, random, sys
from collections import Counter
import petri
from world_digest import canon_s

def write(w, path):
    s = canon_s(w).encode()
    with gzip.GzipFile(path, "wb", compresslevel=9, mtime=0) as f: f.write(s)
    return hashlib.sha256(s).hexdigest()

def digest(path): return hashlib.sha256(gzip.open(path).read()).hexdigest()

def _tup(x): return tuple(_tup(v) for v in x) if isinstance(x, list) else x

def unc(x):
    if isinstance(x, list): return [unc(v) for v in x]
    if not isinstance(x, dict): return x
    # canon writes bytes and bytearray alike; the world holds only bytearrays (cell .mem, .copied; checked 28.10)
    if 'b' in x and len(x) == 1: return bytearray.fromhex(x['b'])
    if 'f' in x and len(x) == 1: return float(x['f'])
    if 'set' in x: return {unc(json.loads(s)) for s in x['set']}
    if 'ctr' in x: return Counter({unc(json.loads(k)): v for k, v in x['ctr']})
    if 'd' in x: return {_key(unc(json.loads(k))): unc(v) for k, v in x['d']}
    if 'rng' in x: r = random.Random(); r.setstate(_tup(unc(x['rng']))); return r
    if 'obj' in x:
        o = object.__new__(getattr(petri, x['obj']))
        for k, v in x['a']: setattr(o, k, unc(v))
        return o
    raise ValueError("unknown canonical node: %r" % list(x)[:3])

def _key(k): return tuple(_key(v) for v in k) if isinstance(k, list) else k

def load(path): return unc(json.loads(gzip.open(path).read()))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "write": print(write(pickle.load(open(sys.argv[2], "rb")), sys.argv[3]))
    elif cmd == "check":
        d = digest(sys.argv[2]); print(d); sys.exit(0 if len(sys.argv) < 4 or d == sys.argv[3] else 1)
    elif cmd == "roundtrip":
        w = load(sys.argv[2]); d2 = hashlib.sha256(canon_s(w).encode()).hexdigest(); d1 = digest(sys.argv[2])
        print("snapshot", d1[:16], "reloaded", d2[:16], "OK" if d1 == d2 else "MISMATCH"); sys.exit(d1 != d2)
