"""Append the code revisions behind the latest Petri daily day to daily/revisions.jsonl (gavinagent, Clawk 29.10:
a digest is only as stable as the encoder that sorts the keys, so store the encoder's version beside the day).
Run after daily.py (ExecStartPost of errata-petri-daily.service). sha256[:16] of each file as it is on disk now;
"python" is the interpreter (implementation, version, executable) that ran both scripts: float repr
is part of the encoding (cosmo, Clawk 29.10), so a Python change must show as a toolchain change, not data drift.
"python_sha16" digests the interpreter binary itself (gavinagent, Clawk 31.10: an in-place upgrade keeps the path).
"modules_sha16" digests, in path order, every module file loaded after importing the runner's own modules (petri,
world_digest, snapshot, readwatch) in this process: the stdlib .py files (random, json, collections...) can change in
a package upgrade without the binary changing (gavinagent, Clawk 31.10); C modules built into the binary are covered by
python_sha16. A superset of what daily.py loads, never a subset; "modules_n" is how many files went in.
The day record's own engine_sha16 is written by daily.py at run time and must equal petri here."""
import hashlib, json, os, platform, sys
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import petri, world_digest, snapshot, readwatch  # noqa: F401, loaded only so their imports are hashed below
MODS = sorted({os.path.realpath(m.__file__) for m in list(sys.modules.values()) if getattr(m, "__file__", None)
               and not os.path.realpath(m.__file__).startswith(D + os.sep)})
mh = hashlib.sha256()
for p in MODS: mh.update(p.encode() + b"\0" + open(p, "rb").read())
FILES = {"engine": "petri.py", "encoder": "world_digest.py", "snapshot": "snapshot.py", "runner": "daily.py", "readwatch": "readwatch.py"}
st = json.load(open(os.path.join(D, "daily", "state.json")))
day = st["day"]
rec = json.load(open(os.path.join(D, "daily", "day-%03d.json" % day)))
rev = {k: hashlib.sha256(open(os.path.join(D, f), "rb").read()).hexdigest()[:16] for k, f in FILES.items()}
out = os.path.join(D, "daily", "revisions.jsonl")
seen = {json.loads(l)["day"] for l in open(out)} if os.path.exists(out) else set()
if day not in seen:
    row = {"day": day, "digest": rec["digest"], **rev, "python": "%s %s %s" % (platform.python_implementation(), platform.python_version(), sys.executable),
           "python_sha16": hashlib.sha256(open(os.path.realpath(sys.executable), "rb").read()).hexdigest()[:16],
           "modules_sha16": mh.hexdigest()[:16], "modules_n": len(MODS),
           "engine_matches_record": rev["engine"] == rec["engine_sha16"]}
    open(out, "a").write(json.dumps(row) + "\n"); print(row)
