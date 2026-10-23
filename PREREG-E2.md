# E2 preregistration: why did E1's threshold land at L50 = 27? (plan #467 follow-up)

Written 2026-10-23 after E1's verdict and before any E2 run on seeds 1-14 (smoke tests on seed 99 only, 30 updates).

## What E1 found (fixed, `e1_verdict.py` on out/e1_a.jsonl, out/e1_b.jsonl)
L50 = 26.88 (seed-cluster bootstrap 25.4-28.0, 1765 of 2000 resamples fit; the rest were separated), band A of PREREG-E1.
All 14 seeds established at L <= 20, extinct at L >= 32. A's input hazard (0.075) is contradicted by the measured
h = 0.049-0.060 in all 14 seeds, so the band match is numerical, not a confirmation of A's mechanism. The mean-field
form with the measured h (B) predicts 36.5; at L = 27 its R0 is about 1.55, not 1.

## Two post-hoc explanations (both written after seeing E1, so E2 is their first test)
- **Crowding (second model, Claude Fable 5.1):** a parasite's copy goes to one random neighbour and fails if that
  host already holds a parasite; kin fill the neighbourhood, so the realised success rate s falls (2D contact process).
  Prediction: with the copy sent to a uniformly random cell, L50 rises by at least 3, into B's band [32, 40]; switching
  off old age changes L50 by less than 3.
- **Old age (mine):** hosts die at 20 x genome length in instructions; this adds hazard beyond h. My crude model
  (uniform residual host life up to 67 updates) gives 27.2. The second model counted age deaths at ~5% of host deaths,
  which makes this small. My own prediction, written now: noage shifts L50 by less than 3; global by 3 or more.

## Design
- Same seeds 1-14, same warm worlds and the same 9 seeded hosts as E1 (deep copy, indel 0, inject never drawn).
- Switches in `petri.py` (defaults reproduce E1 bit for bit; checked on seed 1, L=28: warm row and first census equal):
  `para_global` (copy to a uniformly random cell) and `age_limit` (off: no old-age death).
- Arms per seed: global L in {24,28,30,32,36,40,44,48}; noage L in {24,28,30,32,36,40}; local L in {24,28,32} (E1's
  control, now with failure logging). 17 worlds per seed, 238 in all. 3000 updates, early stop at 0 infected.
- Logged per world: h_arm (births per occupied cell-update during the arm), failed injections by reason
  (empty, occupied, resistant, nolabel, nocut), parasites lost with their host (overwrite, age).
- Two lab jobs: seeds 1-7 and 8-14. `python3 e2_sweep.py 3000 SEEDS "local:24,28,32;global:24,28,30,32,36,40,44,48;noage:24,28,30,32,36,40"`.

## Verdict (`e2_verdict.py`, mechanical, E1's outcome and L50 rules; changed after a second-model review, before any data)
- Local arms must equal E1 world for world (outcome and final infected count); any mismatch voids the verdict (exit 1).
- L50 interval per mode: seed-cluster bootstrap, 2000 resamples, each resample's L50 interval (separation included),
  from the 2.5% point of the lows to the 97.5% point of the highs; a resample with no L50 makes it undetermined.
- Shift = L50(mode) - 26.88; it counts as >= 3 only if the whole interval is >= 29.88, and < 3 only if the whole
  interval is below 29.88; otherwise undecided.
- Crowding: supported if global shift >= 3; falsified as the main cause if < 3. Global copies also remove local host
  depletion and clustering of resistant hosts, so a supported shift is named "crowding by occupied neighbours" only if
  occupied-host failures are >= 50% of failed injections in local mode and < 10% in global; otherwise "spatial structure".
- Old age: supported if noage shift >= 3; not material if < 3.
- If global L50 lies inside [32, 40]: the measured-h mean field works once crowding is removed. Above 40: it does not.
- Failure shares and loss causes are descriptive, not a test.

## Not decided here
Whether crowding acts through occupied neighbours or through local host depletion (both are removed by global copies).
