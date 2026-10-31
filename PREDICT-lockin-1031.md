# Prereg: does length lock-in decide the day-2 shrink? (31.10 03:15 UTC, job lockin-1031 queued, no output yet)

Exploratory context, already seen (6 seeds, out/shrink_carrier_{14,28,11,21,23,26}.json): no single genotype carries
the shrink (top genotype <= 3.3% of cells at every 500-update snapshot). What separates them is when one genome
LENGTH first holds >= 50% of live cells ("lock"): the three that end <= 90 locked at 54,000-56,500 at lengths 85-91;
the three that end >= 102 locked at 42,500-48,000 at 102-103. The 50% threshold and the 50,000 cut were chosen after
seeing those six. Shrinking looks like a slow walk while the population is polymorphic, stopped by a lock.

Caveat: lock and no-shrink may be one thing described twice (a locked population cannot walk). The test below asks
whether lock TIME, which I have not seen for these seeds, sorts them; their end lengths I have seen (shrink_replays.txt).

New seeds (method-1 replays, same engine and world): 12, 15, 17, 29 (end median <= 94), 13, 19, 20 (end >= 99),
18 (end 95, no prediction). Lock = first snapshot (every 500 updates, 40,500-80,000) where the modal genome length
holds >= 50% of live cells; "never" counts as >= 50,000.

- **L1:** all four of 12, 15, 17, 29 lock at >= 50,000.
- **L2:** all three of 13, 19, 20 lock at < 50,000.
- Pass = L1 and L2 (7 of 7). Any miss is reported as a miss with the seed.
- **G (descriptive):** top genotype share stays <= 5% at every snapshot in all 8.
- Validity: each arm must reproduce out/mm_1_<seed>.json (mismatch_vs_mm1 = 0); a mismatching seed is reported and
  excluded, not replaced.

Scorer: lockin_verdict.py (written before the outputs exist; reads only out/shrink_carrier_<seed>.json).
