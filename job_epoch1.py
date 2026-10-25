# Epoch 1 verdict (plan #440) as a lab job: the lab runner only takes .py files, so this replaces job_epoch1.sh
# with the same loop (seeds 1..5 outer, control then entries in file order). Queue only after the close (26.10 00:00 UTC).
import json, os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
arms = ["control"] + [json.loads(l)["agent"] for l in open("submissions/epoch-1.jsonl") if l.strip()]
env = dict(os.environ, PYTHONPATH=".")
with open("out/epoch1_verdict.jsonl", "w") as out:
    for s in range(1, 6):
        for arm in arms:
            rc = subprocess.call([sys.executable, "epoch1_insert.py", arm, str(s)], stdout=out, env=env)
            if rc: sys.exit(rc)
