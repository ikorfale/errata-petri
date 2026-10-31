# Verdict: PREDICT-lockin-1031 (scored 31.10 06:10 UTC, lockin_verdict.py, output VERDICT-lockin-1031.txt)

All 8 seeds valid (each reproduces its method-1 run, 0 mismatches).

- **L2 (the part A1 counts as evidence): 3 of 3.** Seeds 13, 19, 20 (end >= 99) locked at 48,000, 42,000, 41,500.
- **L1: 3 of 4, miss seed 17.** It locked at 42,500 at length 95 and still ended at 93.
- Original prereg (L1 and L2, 7 of 7): **FAIL**, by one seed.
- **G (descriptive): holds.** Top genotype share at most 2.7% at every snapshot in all 8.

## What the miss shows (exploratory, lockin_explore.py, out/lockin_explore.txt)
A1 said L1 was "mostly circular" if a lock is absorbing. **It isn't.** Once a population has locked, one length
keeps >= 50% of cells in 46-96% of the later snapshots, and **the modal length keeps moving while it's held**:
- seed 17 went 95 -> 93 and seed 18 went 99 -> 95;
- seed 12 went 98 -> 92 (its lock at exactly 50,000 counts as >= 50k);
- seed 20 went 105 -> 101.

So "a lock stops the walk" is wrong. A locked population walks in steps of one length at a time, the whole lock
moving together. What the 14 seeds do support: an early lock goes with a long end.
- A1 item 3: Spearman of modal-length share at 44,000 vs end median, over 14 seeds, is 0.49. Exploratory.
- Applied after the fact, the forward rule (locked before 50k at >= 95 -> ends >= 95) gets 13 of 14 right. That
  includes the 6 seeds that chose the cuts. On the 8 new seeds it gets 7 of 8, and the miss is 17. Seed 18 is a hit
  with 0 to spare (95).

The forward test (lockfwd, fresh seeds 33-48, criterion per A2) is unchanged and still decides.
