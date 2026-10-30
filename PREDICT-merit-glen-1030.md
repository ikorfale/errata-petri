# Does merit method 4 grow genomes? Six fresh paired seeds (30.10)

Written after the six-pair verdict (VERDICT-merit-method-1030b.md), before seeds 17-22 run. Same design: day-1 end
(update 40,000), reseed, method 1 and method 4, 40,000 updates each. G = mean genome length at 80k (glen_mean),
dG = G(method 1) - G(method 4). Seeds 11-16 are seen and are not counted here; only 17-22 decide.

Lead being tested: method-4 genomes ended longer in 5 of 6 seen pairs (dG mean -5.6, sd 6.6; two pairs near -14).

Prediction: G is higher under method 4 (dG < 0).
Decision rules, over the 6 new pairs only, both reported:
- G1: sign, dG < 0 in 6 of 6 (p = 1/64); 5 of 6 is not enough.
- G2: one-sided paired t on dG (H1: mean dG < 0), alpha 0.05, df 5.
Power at the seen spread (true mean -5.6, sd 6.6): roughly two in three for G2, lower for G1. A miss is not proof of
no effect; it will be reported as "not detected at this spread".
Side check, not a rule: does dU > 0 hold again (expected 5 or 6 of 6)?
Jobs: petri-meritmethod-1030c (seeds 17-19), petri-meritmethod-1030d (20-22). Verdict script: mm_verdict.py 17 18 19 20 21 22.
