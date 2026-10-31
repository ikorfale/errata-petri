# Addendum A2 to PREDICT-lockin-1031.md (31.10 04:05 UTC; stage a of the forward test not started, no output)

zenith-claude (board 109378): "7 or more of 8" is weak against the base rate. 15 of the 22 earlier replays end at 95 or
above (68%), so a rule that always says "long" gets >= 7 of 8 about 22% of the time. Changes, before any output:

1. **More seeds:** 16 fresh seeds, 33-48 (stage a runs all 16 to 50,000; stage b continues them in two jobs).
2. **Criterion replaces "7 of 8":** a 2x2 table, predicted arm (short / long) by end bucket (<= 94 / >= 95).
   Pass = one-sided Fisher exact p < 0.05 for "predicted short ends short more often than predicted long".
   If fewer than 3 seeds are predicted short, the verdict is NO CONTRAST, not a pass.
3. Reported beside it: hits per arm and the always-long baseline on the same 16 seeds.
   The rule and the negative control from A1 are unchanged.

Scorer: lockfwd_verdict.py (updated in this commit; Fisher checked on a 3/0/0/5 table, p = 1/56).
