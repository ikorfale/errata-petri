cd "$(dirname "$0")/.."
for rs in $(seq 101 120); do for arm in v1 inc0; do PYTHONPATH=. python3 out/epoch_probe.py $arm $rs 300; done; done > out/epoch_probe20.jsonl 2> out/epoch_probe20.err
