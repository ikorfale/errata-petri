# PREREG-laps (#491) — FROZEN 2026-10-24 (after five blocking-only review rounds; the fifth returned NONE)

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

## Scoring (scoring.py is the whole rule; `python3 scoring.py` prints the table)
- Truth unresolved under seed 7 or seed 8: out-of-scope. A non-abstained static prediction whose truth differs
  between the seeds: miss (arith handles seed divergence through the premise, below).
- static: hit iff class and parameter equal (j for exact, ncopy for exact-offlap and rotated; never = never).
  Abstain and other-birth are not scored; other-birth is reported with its truth, length match and seed stability
  (in-sample 7 other-birth predictions: 2 seed-stable with matching child length, 5 whose truth differed between
  the seeds; decided on development data before any test truth exists).
- arith is two things, scored apart:
  - lap claim: scored on the seeds whose truth is an exact copy at a lap (not scored if neither seed gives one).
    Hit iff arith is exact j and every such seed has that j; arith never against any exact copy is a miss. What the
    other seed did goes to the premise.
  - premise ("a non-abstained arith meets, under both seeds, an exact copy at a lap or no birth"): a measurement,
    reported as holds / fails with the breakdown by (arith class, truth classes). It is already false in-sample
    (holds 166 of 263), so it carries no refute rule.
- The scoring driver is static_insample.py: it asserts that committed predictions equal what the frozen predictors
  give, prints every count in this file (including the arith lap claim by j class and gcd, and the targeted cells),
  and writes every miss and premise failure with its genome to `<prefix>.misses.json`.

## Reported, per stratum and per predictor
hits, misses, abstentions, out-of-scope, not-scored; for arith the lap claim separately for j = 1 and j >= 3 and for
gcd(L, p) > 1, and the premise breakdown. For each of the 5 targeted disagreement cells: which predictor matched truth,
in how many of the drawn variants.

## Decision rules
- static soundness is judged on the random stratum only (the targeted stratum is adversarially selected and is
  reported alongside, never pooled): sound if it has at least 200 scored cases and at most 1% misses. In-sample:
  256 hits, 0 misses, 1320 abstentions (7 of them other-birth).
- arith lap claim: any miss refutes the arithmetic as stated; the headline gives hits/scored for j = 1 and j >= 3
  separately, never pooled. In-sample: 166 hits, 0 misses (j = 1: 69, of them 62 with gcd > 1; j >= 3: 97, all gcd = 1).
  The test-set arith predictions are almost all j = 1 (574 j = 1, 3 j = 5, out/laps_gen.txt), so the j >= 3 cells
  get their power from the targeted stratum.
- Every headline carries the abstain count and the premise rate next to the hit counts.

## What this test cannot claim
- The odd-lap carve theorem is not tested: predict() reproduces carve() verbatim.
- Nothing generalises to census genomes: parents were chosen as genomes predict() handles, in-sample abstention was
  high.
- Arith never against truth never confirms only within the 10-lap horizon; arith's never is unbounded in j.
- Static tests path-neutrality of a failed check and soundness of the abstain rules; arith tests that the schedule
  is periodic from its first points and that the label passes only at lap boundaries.

## In-sample (development data, 1576 census genomes): `out/static_insample.txt` and `out/static_insample.misses.json`,
produced by static_insample.py with scoring.py. Seed 7 or 8 hits the step cap on 98 genomes where arith does not abstain (out-of-scope).

## Freeze: sha256 of petri.py, static_lap.py, laps_truth.py, scoring.py, static_insample.py, laps_gen.py,
laps_targeted.py and both prediction files, recorded in this file's freeze commit.

### Frozen sha256
- `petri.py` 2036499c2c707e7517d77bd086365d16c2da5413198becc5f2535bb44b8fa20c
- `static_lap.py` 002d4a0b4be6e6acc0b6141d9aa128d654f19d07088d5c5ebb28765b77418d55
- `laps_truth.py` 61f9a4aafc508a049cceeef546e7fd06e0b23dc7542ccd924de28843c4af9005
- `scoring.py` b4d78de5d66372849e2563979edcda55ed3ec669b616f3f1ae81057a7f8f4a6c
- `static_insample.py` 32761b8381bb0d6f3b03df39ba328fb8ac71513257c8e3fc5dd26986c307df55
- `laps_gen.py` 2106a39098c9c9c098d946b22bc0779c564a839e83688d9952cb409f92e6c554
- `laps_targeted.py` 45baaddc7e48c00f07d72c7c116cd41cb0782e0fec7dc1d231ba488bff8c3b9c
- `out/laps_predictions.json` 5130f8dc4db17a147b5a2c238f906b54ab822df3221b7d5e13a93dfad9b2cd8b
- `out/laps_targeted.json` 9e5a74d534c417ded4aa3f83eb927170d18114063b69ebebf50fe67a6ff24b55

Run after the freeze commit: `python3 static_insample.py out/laps_predictions.json out/laps_random` and
`python3 static_insample.py out/laps_targeted.json out/laps_targeted_truth`; outputs committed as they come out.
