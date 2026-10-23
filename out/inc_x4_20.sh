cd "$(dirname "$0")/.."
for rs in $(seq 101 120); do PYTHONPATH=. python3 out/inc_x4.py $rs 300 4; done > out/inc_x4_20.jsonl 2> out/inc_x4_20.err
