# Verdict on PREDICT-shrink-1029.md (day-2 shrink in steps of three)
Written 30.10 after reading daily/replay-day-002-lengths.json. The replay of day 2 (40,000 updates from daily/base/day-001,
81 censuses) ended on the day-2 digest e3388c8a..., so the run is valid.

- P1 MISSED. Modal length is 2 mod 3 in 22 of 33 censuses from 44,000 to 60,000 (67%, needed 80%).
- P2 MISSED. Mean share of organisms at a length 2 mod 3 over 44,000-80,000 is 0.537 (73 censuses, needed 0.60).
- P3 MISSED. Modal runs 42,000-60,000: 101, 102 x2, 100 x2, 92, 99 x3, 92 x6, 90 x2, 89, 90 x3, 89 x7, 90, 87, 89 x7.
  98 and 95 are never modal; the mode jumps from 99 to 92, and 90 (0 mod 3) holds it for 3 censuses in a row.

What the data shows instead: the end state 89 is 2 mod 3, but 90 is a stable rival, not a passing step. At 72,000-74,000
length 90 holds about 80% of the world (share at 2 mod 3 falls to 0.09-0.10), and 89 takes it back by 76,000.
Median merit by length within a census tracks length closely (89 vs 90: equal at 54,000 and 64,000, 1% apart at 72,000 and 80,000), so the
copy-loop advantage of 2 mod 3 is at most a weak push. The "steps of three" story is wrong for day 2.
Not tested: why the shrink starts after ~42k; what decides the 89/90 swaps (drift or a real fitness gap).
