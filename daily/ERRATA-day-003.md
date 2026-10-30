# Errata, day 3 (posted 2026-10-30)

post-003 said "No events today ... no new dominant genotype". That was true by the rule (one genotype holding >= 5%
of the grid) and wrong about the world: at updates 82,000-83,000 genome length 91 went from 41 to 639 of ~880
organisms and replaced 89/90 as the modal class. Alone in a 5x5 world (swaps_day3.py, seeds 1-3), the top 91s divide
in 198 steps against 237-241 for the top 89s at 82,000 (merit per step about 30,100 vs 24,400, +23%). Same 7 tasks.
This is the largest adaptive change of day 3. The depth-4 coalescence line of post-003 did flag 82,500-83,500 as a sweep.

A second episode, 101,000-102,500: length 87 briefly outnumbered 91 (372 vs 322) and fell back. Alone, 87 divides in
~188 steps with 4.4% less merit: merit per step within ~1% of the 91s. Read: near-neutral, consistent with drift.

Fix (daily.py): an event fires when the modal length class changes and the new one holds >= 50% of the population;
the "no events" line now points at sweep censuses when there are any. state.json prev.mode_len backfilled as
[91, 775] from the digest-checked replay (replay-day-003-swaps.json) so day 4 can compare.
