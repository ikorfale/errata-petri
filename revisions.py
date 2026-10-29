"""Append the code revisions behind the latest Petri daily day to daily/revisions.jsonl (gavinagent, Clawk 29.10:
a digest is only as stable as the encoder that sorts the keys, so store the encoder's version beside the day).
Run after daily.py (ExecStartPost of errata-petri-daily.service). sha256[:16] of each file as it is on disk now;
"python" is the interpreter (implementation, version, executable) that ran both scripts: float repr
is part of the encoding (cosmo, Clawk 29.10), so a Python change must show as a toolchain change, not data drift.
The day record's own engine_sha16 is written by daily.py at run time and must equal petri here."""
import hashlib, json, os, platform, sys
D = os.path.dirname(os.path.abspath(__file__))
FILES = {"engine": "petri.py", "encoder": "world_digest.py", "snapshot": "snapshot.py", "runner": "daily.py", "readwatch": "readwatch.py"}
st = json.load(open(os.path.join(D, "daily", "state.json")))
day = st["day"]
rec = json.load(open(os.path.join(D, "daily", "day-%03d.json" % day)))
rev = {k: hashlib.sha256(open(os.path.join(D, f), "rb").read()).hexdigest()[:16] for k, f in FILES.items()}
out = os.path.join(D, "daily", "revisions.jsonl")
seen = {json.loads(l)["day"] for l in open(out)} if os.path.exists(out) else set()
if day not in seen:
    row = {"day": day, "digest": rec["digest"], **rev, "python": "%s %s %s" % (platform.python_implementation(), platform.python_version(), sys.executable),
           "engine_matches_record": rev["engine"] == rec["engine_sha16"]}
    open(out, "a").write(json.dumps(row) + "\n"); print(row)
