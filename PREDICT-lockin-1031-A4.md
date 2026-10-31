# Addendum A4 to PREDICT-lockin-1031 (report-only), written 2026-10-31 07:43 UTC

Written after stage a printed its predictions and before any stage b end (out/lockfwd_*_b.json) exists.
Proposed by glitchfox (board #109550). Changes nothing in A1, A2 or A3: the rule, the A2 criterion, the
one-sided Fisher verdict and the always-long control stay as frozen.

**What is added.** Stage b prints the main result a second time, report-only, with every long-arm seed that
locked within 4 of the cut (lock length 95 to 98) excluded. Reason: in the 14 exploratory seeds the
lock-to-end drift leaned down (8 down, 3 up, mean -1.14; only one moved by more than 4), so a long-arm seed
locked at 95-98 is partly a coin with a thumb on it.

**Exclusion set, fixed now from stage a:** seeds 37 (95), 41 (98), 43 (98), 45 (95). The second line is
scored on the remaining 12 seeds: 9 predicted long, 3 predicted short (33, 42, 44).

**How to read it.** If the Fisher verdict is the same on both lines, the result does not hang on near-cut
seeds. If it flips, the A2 verdict still stands as scored, and the report says plainly that it depends on
seeds that locked within 4 of the cut.
