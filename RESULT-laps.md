# RESULT-laps (#491), run 2026-10-24 after the freeze commit 34a5506

Outputs: out/laps_random.txt, out/laps_targeted_truth.txt, misses in out/*.misses.json. Driver asserted that both
committed prediction files equal what the frozen predictors give.

## As pre-registered
- static, random stratum: 601 hits, 0 misses, 305 abstentions (3 of them other-birth), 40 out-of-scope (truth hit the
  step cap). Decision rule (>= 200 scored, <= 1% misses): **sound on this set**. Targeted stratum: 254 hits, 0 misses,
  29 out-of-scope.
- arith lap claim: random 487 hits, 0 misses (j = 1: 485, of them 161 with gcd > 1; j >= 3: 2); targeted 116 hits,
  0 misses (j >= 3: 41). **Not refuted.**
- arith premise: holds 566 of 589 (random), 227 of 227 (targeted).

## A hole in my frozen rule, found in the committed cell report
In the three disagreement cells where arith predicted an exact copy at lap 1 or 5 and static predicted no birth,
truth was "no birth within 10 laps" in all 69 resolved variants (6 more out-of-scope): static right, arith wrong.
The frozen rule files "arith exact j, truth never" under not-scored for the lap claim and counts it as the premise
holding, because the premise only asked that truth be "exact or never". It should have required arith's own class.
In the random stratum the same pattern is 55 cases (all j = 1; static said never in 47, abstained in 8).
Corrected count (post hoc, labelled as such): arith's copy / no-copy call is wrong in 55 + 21 + 1 + 1 = 78 of 589
non-abstained random cases and 69 of 227 targeted. When an exact copy does happen, its lap is what arith says
(603 of 603); arith cannot tell whether a copy happens. The pre-registered headline stands as computed; this
paragraph is the correction next to it.
