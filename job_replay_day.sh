#!/bin/bash
# lab job (#553): exact OR origins of day N of the long world, from the saved day N-1 world. Usage: job_replay_day.sh N
set -eu; cd "$(dirname "$0")"; N=${1:-2}; P=$(printf %03d $((N-1))); C=$(printf %03d $N)
D=$(python3 -c "import json;print(json.load(open('daily/day-$C.json'))['digest'][:16])")
U=$(python3 -c "import json;u=json.load(open('daily/day-$C.json'))['updates'];print(u[1]-u[0])")
A=$(python3 -c "import json;print(json.load(open('daily/day-$C.json'))['updates'][0]+1500)")
python3 replay_origins.py daily/base/day-$P "$U" --task OR --after "$A" --digest "$D" > daily/replay-day-$C-OR.json
