# #541 result: breakups per arm and E3 under a strict division rule (PREDICT-e3brk-1028.md, committed 2669d50 before the runs)

Read 2026-10-28. Default rule: out/e3brk_{a,b}.jsonl, scored by score_e3brk.py. Strict rule: out/e3strict_{a,b}.jsonl,
scored by score_e3strict.py (out/score_e3strict.txt). The seeds 1-7 strict rerun with refusal counters (out/e3strict_c.jsonl)
equals e3strict_a world for world apart from the new fields and CPU time.

| | prediction | outcome |
|---|---|---|
| P1 | every mode's pooled breakup share 1.0-2.0% | hit: local 1.59%, host 1.53%, updates 1.51% |
| P2 | modes differ by at most 0.3 points at each L | hit: largest spread 0.12 points (L=36) |
| P3 | counter neutral, 196 worlds equal E3 | hit: 196/196 |
| P4 | strict: 0 breakups; warm-up h_occupied within 20% seed for seed | hit: 0 breakups in 196 worlds + 14 warm-ups; widest seeds 11 (-18.1%) and 12 (+16.6%) |
| P5 | strict host-local shift within 1.0 of 2.72; H1 still undecided (p 0.6) | hit: shift 1.98 (-0.74); host strict bootstrap 27.97-30.89 contains local strict + 3 = 30.46 |

Strict L50s (seed-cluster bootstrap 95%): local 27.46 (26.14-28.89), host 29.44 (27.97-30.89), updates 28.14 (26.97-29.00).
The strict rule lowers the point shift from 2.72 to 1.98, i.e. away from the +3 line, but inside the noise; E3's verdict
(H1 undecided) is not re-decided by this sensitivity run and stays as it is.

Refusals per arm under strict (seeds 1-7, refusals_per_arm.py): viable refusals per 1,000 host divisions are flat
(local 315, host 310, updates 310); refusal episodes per 1,000 are 16.3 / 17.1 / 22.9; 31-35% of episodes end with the
host lost before dividing; the first division after a refusal takes ~411-418 steps vs ~354-357 without (+57-61). Host and
local arms do not differ in refusals, so the strict rule cannot be what makes the host-local gap.

Not explained: the downward drift of the breakup share with L inside each mode (default rule).
