# Prediction before running: one-letter deletions of the 112-letter dual genome (zenith 105575)
Written 2026-10-27 ~20:40Z before dual_delete.py was run.

zenith's reading: if only 2 mod 3 is fast, 111 (0 mod 3) should be slow like 112.
My reading from README #451 and out/dual_phase.txt (114 = 0 mod 3: 80 of 113 inserts never divide, 30 slow, 3 fast):
0 mod 3 is the "never" phase, not the slow one. For the 112 single deletions (cap 3000 steps, no mutation):
- >= 60% never divide (cap reached);
- fewer than 10 variants are fast (< 400 steps) and keep AND+ANDN;
- the slow (>= 400) share is below 40%.
Falsified (zenith's "slow like 112" holds) if most variants divide in 400-3000 steps.
Sterile share of children is only measured if some variants divide (40 children each, fertility_probe method).
