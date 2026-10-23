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

# theone 99870: the rebuild check as a contract. A rebuild is accepted only if every world field digests equal, with one
# named exception for epoch 1: reset_failed_inject may differ when parasites are off in BOTH worlds (inject is never drawn,
# so the flag is unused). Any other field (slice, copy_mut, cells, rng, ...) differing is a reject. The verdict carries the
# sha256 of petri.py and of this file, so it binds to the engine and digest revisions it was made with.
EXCEPT_PARASITES_OFF = {'reset_failed_inject'}

def parts(w): return {k: hashlib.sha256(canon_s(getattr(w, k)).encode()).hexdigest() for k in sorted(vars(w))}

def compare(frozen, rebuilt):
    pa, pb = parts(frozen), parts(rebuilt)
    diff = sorted(k for k in set(pa) | set(pb) if pa.get(k) != pb.get(k))
    allowed = EXCEPT_PARASITES_OFF if (frozen.parasites is False and rebuilt.parasites is False) else set()
    whole = hashlib.sha256(canon_s(frozen).encode()).hexdigest() == hashlib.sha256(canon_s(rebuilt).encode()).hexdigest()
    ok = all(k in allowed for k in diff)
    import os
    rev = {n: hashlib.sha256(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), n), 'rb').read()).hexdigest()[:16]
           for n in ('petri.py', 'world_digest.py')}
    return {'accept': ok, 'whole_state_equal': whole, 'differs': diff, 'excepted': [k for k in diff if k in allowed],
            'revisions': rev}

if __name__ == '__main__':
    import petri  # noqa: F401  (classes for unpickling)
    args = [a for a in sys.argv[1:] if a != '--parts']
    w = pickle.load(open(args[0] if args else 'out/epoch1_world.pkl', 'rb'))
    h = lambda x: hashlib.sha256(canon_s(x).encode()).hexdigest()
    print(h(w))
    if '--parts' in sys.argv:
        for k in sorted(vars(w)): print(f"  {k}: {h(getattr(w, k))[:16]}")
