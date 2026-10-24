#!/bin/bash
# Epoch 1 verdict (plan #440): every entry + control, insertion seeds 1..5, +3000 updates. Queue only after the close (26.10 00:00 UTC).
cd "$(dirname "$0")"
for s in 1 2 3 4 5; do for arm in control $(python3 -c "import json;[print(json.loads(l)['agent']) for l in open('submissions/epoch-1.jsonl') if l.strip()]"); do
  PYTHONPATH=. python3 epoch1_insert.py "$arm" "$s"; done; done > out/epoch1_verdict.jsonl
