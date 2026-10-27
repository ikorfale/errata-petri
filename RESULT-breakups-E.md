# #537: half-copy breakups in the E1-E3 settings (2026-10-27)

Prediction committed before the run: e4e414b (PREDICT-breakups-E-1027.md). Command:
`python3 breakups.py SEED 3000 30 --e`, seeds 1-3 (side 30, parasites on, inject never drawn, indel 0.05 until
update 2000, then 0; no parasite seeded). Breakup = a birth after which the parent keeps < 75% of its genome.

| seed | updates 1-2000 | 1501-2000 | 2001-3000 (indel 0) |
|---|---|---|---|
| 1 | 929 / 67043 = 1.39% | 1.41% | 560 / 42230 = 1.33% |
| 2 | 923 / 68979 = 1.34% | 1.40% | 637 / 43800 = 1.45% |
| 3 | 897 / 66132 = 1.36% | 1.47% | 572 / 43441 = 1.32% |

- Prediction held on all 3 of 3 seeds: warm share in 1.0-2.0%, indel-0 share within 0.5 points of 1501-2000
  (largest gap 0.15 points). Same level as plain ancestor worlds (1.37-1.49%, 20x20).
- Most common: parents of 97-102 letters halving to 49-51.
- What it means for E1-E3: about 1 host birth in 70 is a breakup in every arm, a constant background that the arms
  share. It does not explain differences between arms by itself.
- Not measured: whether these breakup children are sterile in these worlds (shown only for 0 mod 3 deletions of the
  dual genome), and breakups of infected hosts (no parasite seeded here).
