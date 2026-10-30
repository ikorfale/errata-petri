# Merit method 1 vs 4, seeds 14-16 (30.10, written after seeds 11-13 were seen, before 14-16 ran)

Same design as PREDICT-merit-method-1030.md: day-1 end (update 40,000), reseed 14, 15, 16, method 1 and 4, 40,000
updates each. Same U and G definitions. Seeds 11-13 are already known (VERDICT-merit-method-1030.md), so the
6-pair result below is partly seen; only seeds 14-16 are blind.

Decision rule (glitchfox, board 108301): over all 6 pairs,
- D1: one-sided sign test on dU = U(1) - U(4) > 0. "Method 4 lowers U" counts as supported only at 6 of 6 (p = 1/64);
  5 of 6 (p = 7/64 = 0.11) is not enough.
- D2: report the mean paired dU with a t interval (5 df) and the same for dG; no claim from dG unless its interval
  excludes 0.
- On seeds 14-16 alone: I expect dU > 0 in at least 2 of 3 and dG of either sign (P3 failed once already).
