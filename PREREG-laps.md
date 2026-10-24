# PREREG-laps (#491) — DRAFT, NOT FROZEN

Question: from a genome's text alone, can we predict its first division outcome (class and lap) without stepping the
world? Two predictors, one truth runner, one scoring rule, all fixed before any truth is computed on the test set.

## Test set (fresh: no genome in out/two_step_filter.json)
- Random stratum: 946 one- and two-edit mutants of 5 parents (`laps_gen.py`, `out/laps_mutants.json`).
- Targeted stratum: 283 single-edit variants drawn from 12 cells (p, arith class, static class) of the full
  single-edit neighbourhood, up to 25 per cell, 5 cells where the predictors disagree (`laps_targeted.py`,
  `out/laps_targeted.json`).
- Predictions for both strata are committed before truth (`out/laps_predictions.json`, `out/laps_targeted.json`).

## Predictors
- static: `static_lap.predict` — abstract run of the VM, every if-label forced to fail, every h-divide a failed
  carve, run to 10 laps; abstains whenever a branch, head move or carve depends on an unknown value.
- arith: `static_lap.arith` — e, p from the forced-fail check schedule; least odd j with j*L = e (mod p) by
  `least_odd_j`; abstains when the schedule has fewer than 3 checks or is not periodic over its first 6.

## Truth
`laps_truth.truth`: mutation and indels off, run until a birth or ncopy > 10*L; a 400*L step cap that binds first is
"unresolved". Run under world seeds 7 and 8.

## Scoring (scoring.py, the whole rule; table printed by `python3 scoring.py`)
- abstain is counted, never scored; truth unresolved is out-of-scope.
- A non-abstained prediction whose truth differs between seeds 7 and 8 is a miss.
- static: hit iff class and parameter equal (j, ncopy, child length; never = never).
- arith: exact j hits only truth ("exact", j); never hits only truth never; exact j > 10 against truth never is
  out-of-scope; any other resolved truth is a miss.

## Reported, per stratum and per predictor
hits, misses, abstentions, out-of-scope; every miss listed with its genome. For arith, separately: j = 1, j >= 3,
gcd(L, p) > 1. For each of the 5 disagreement cells: which predictor matched truth, in how many of the drawn variants.

## Decision rules (proposed, to be fixed at freeze)
- static is called sound on this set if it has 0 seed-dependent misses and at most 1% misses among scored cases,
  with at least 200 scored; otherwise every miss is analysed as a predictor bug or a theory failure, publicly.
- arith: a single miss in a cell where arith is not abstaining refutes the rule as stated for that cell; the
  headline gives hits/scored for j = 1 and for j >= 3 separately, never pooled.

## What this test cannot claim
- The odd-lap carve theorem is not tested: predict() reproduces carve() verbatim.
- Nothing generalises to census genomes: parents were chosen as genomes predict() handles, in-sample abstention was
  high.
- Static tests path-neutrality of a failed check and soundness of the abstain rules; arith tests that the schedule
  is periodic from its first points and that the label passes only at lap boundaries.

## In-sample (development data, 1576 census genomes): `out/static_insample.txt`, scored by scoring.py.

## Freeze: sha256 of static_lap.py, laps_truth.py, scoring.py, laps_gen.py, laps_targeted.py and both prediction
files, recorded in this file's freeze commit.
