# Verdict on PREDICT-swaps-1030.md (what drives the day-2 89/90 swaps)
Written 30.10 after replay_swaps.py (day 2 from daily/base/day-001, 40,000 updates, 81 censuses, ended on the day-2 digest
e3388c8a..., so the run is valid). Outputs: out/swaps_diff_day2.txt (swaps_diff.py), out/swaps_flip_day2.txt (swaps_flip.py).

- S1 HIT. At the 75,000 -> 75,500 swap the dominant 89 differs from the dominant 90 by Levenshtein 17.
- S2 HIT, BUT NOT BLIND. The dominant 89 at 75,500 does NAND alone (merit 5,832,704 vs 2,949,120, steps 237 vs 233);
  the 90 does not. out/sweep_iso.txt (29.10, commit 5ff1ccb) already showed this for the 74.5k -> 75.5k sweep. I did not
  reread it before writing the prediction, so S2 tests nothing.
- S3 HIT, BUT A WEAK TEST. All 8 modal swaps have distance >= 2 (17 to 41). 89 and 90 are two old clades, 17-41 edits
  apart, not one indel apart, so ">= 2" holds trivially. The prediction should have used the between-clade distance as the
  baseline.

What the data shows. The mode swaps 8 times, but most swaps are jitter near 50/50. With glitchfox's definition (89's
share of 89+90 crossing 0.8 <-> 0.2) there are three majority flips:
1. 50k-57.5k, 90 -> 89 (f89 0.19 -> 0.92). At 56.5k the only fast genotype among the top three of each class is an 89
   (240 steps vs 323-333). By 57.5k both classes copy in ~240 steps. The flip lines up with the copy-speed sweep and
   starts on an 89 background.
2. 68k-72k, 89 -> 90 (0.79 -> 0.09). Same tasks on both sides. Alone, the top 90s get 1-3% more merit per step than the
   top 89s (12,288-12,549 vs 12,051-12,202). Merit scales with length, and the extra instruction does not slow copying
   here. A weak, constant gap in 90's favour, also visible at 57.5k (3,059-3,085 vs 3,025-3,051).
3. 75k-75.5k, 90 -> 89 (0.37 -> 0.96). NAND arrives on an 89 background, merit x2.

Reading: the length gap favours 90 by about 1-3%, and it moved the world one way (flip 2), as a fixed gap should
(glitchfox's toy). 89 won twice against it by hitchhiking on a large background step that first appeared on an 89
(copy speed, then NAND). That fits glitchfox's hitchhiking hypothesis and not drift.
Limits: merit per step alone in a 5x5 world, top 3 genotypes per class, seeds 1-3. Realised fitness on the grid (age
limit, neighbours, CPU credit) is not measured. The world has about 860 organisms on 900 cells, not 3,600.
