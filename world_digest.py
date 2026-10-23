"""Content digest of a frozen Petri world (scout 99774: a rebuild matched the census but not the pickle's bytes).
Byte hashes of a pickle depend on Python version and object layout; this hashes the state itself: every attribute
of the world and of every organism (memory, heads, registers, stack, inputs, tasks, merit, credit, lineage, a
parasite thread if any) plus the RNG state, serialised canonically (sorted keys, floats by repr).
Usage: world_digest.py [out/epoch1_world.pkl] [--parts]   (--parts: one digest per world field, cells as one field,
so a rebuild that differs shows where; 23.10 a rebuild with current petri.py matched every cell and differed only in
reset_failed_inject, a parasite-epoch setting whose default changed after the freeze)"""
import hashlib, json, pickle, sys
from collections import Counter

def canon(x):
    if isinstance(x, (bytes, bytearray)): return {'b': x.hex()}
    if isinstance(x, float): return {'f': repr(x)}
    if isinstance(x, (set, frozenset)): return {'set': sorted(map(canon_s, x))}
    if isinstance(x, Counter): return {'ctr': sorted((canon_s(k), v) for k, v in x.items())}
    if isinstance(x, dict): return {'d': sorted(([canon_s(k), canon(v)] for k, v in x.items()), key=lambda t: t[0])}
    if isinstance(x, (list, tuple)): return [canon(v) for v in x]
    if x is None or isinstance(x, (bool, int, str)): return x
    if hasattr(x, 'getstate') and type(x).__name__ == 'Random': return {'rng': canon(x.getstate())}
    names = sorted(set(getattr(x, '__dict__', {})) | {n for c in type(x).__mro__ for n in getattr(c, '__slots__', ())})
    return {'obj': type(x).__name__, 'a': [(k, canon(getattr(x, k))) for k in names if hasattr(x, k)]}

def canon_s(x): return json.dumps(canon(x), sort_keys=True, separators=(',', ':'))

if __name__ == '__main__':
    import petri  # noqa: F401  (classes for unpickling)
    args = [a for a in sys.argv[1:] if a != '--parts']
    w = pickle.load(open(args[0] if args else 'out/epoch1_world.pkl', 'rb'))
    h = lambda x: hashlib.sha256(canon_s(x).encode()).hexdigest()
    print(h(w))
    if '--parts' in sys.argv:
        for k in sorted(vars(w)): print(f"  {k}: {h(getattr(w, k))[:16]}")
