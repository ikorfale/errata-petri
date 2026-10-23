cd "$(dirname "$0")/.."
for rs in $(seq 101 120); do PYTHONPATH=. python3 out/and_ablation.py $rs 300; done > out/and_ablation20.jsonl 2> out/and_ablation20.err
