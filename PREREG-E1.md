# E1 preregistration: how long can a parasite be and still spread? (plan #421)

Written 2026-10-23 before any run of `e1_sweep.py` on the seeds below. Design reviewed by a second model
(Claude Fable 5.1); where I depart from its answer it is said here.

## Question
A parasite in Petri is the ancestor with `h-divide` replaced by `inject nop-B` and its padding cut to length L.
It copies itself at half its host's speed and infects a neighbour. Below some critical length it spreads; above it,
hosts are overwritten before it can copy itself. Where is that length?

## What was already seen (so not evidence for anything below)
- L=20 under the reset-after-failed-inject rule: established in 5/5 seeds, 412-549 infected at +1500 (`out/fix_trial3.log`).
- L=101 died within 250 updates in an old-rule pilot, and in a 250-update smoke test of this script on seed 99 (not in the sample).
- Warm-up measurements on seeds 1-3 and 99 (no parasites): births per occupied cell-update h = 0.0487-0.0509;
  on seed 99 median host merit / mean merit = 0.52 (task-doers take most of the CPU).

## Design
- Seeds 1-14. Per seed one warm world: 2000 updates, parasites on, mutation never draws `inject` (`w.nops = len(OPS) - 1`),
  so no parasite can arise or return by mutation and extinction is final. h and the merit ratio are logged from updates 1500-2000.
- Arms L in {16, 20, 24, 28, 32, 36, 40, 44, 48}: a deep copy of the warm world, indel set to 0 (no length evolution;
  copy mutation stays on), the same 9 host cells get the parasite in every arm. 3000 updates; stop early at 0 infected.
- Two lab jobs: seeds 1-7 and 8-14. Command: `python3 e1_sweep.py 3000 SEEDS 16,20,24,28,32,36,40,44,48`.

## Outcome per world, at +3000
established = infected >= 45 (5% of the grid); extinct = 0; otherwise unresolved, reported and excluded from the fit.

## Three rival predictions for L50 (logistic fit of established vs extinct on L, 14 seeds per arm)
R0(L) = s * v(L) / (exp(h * g) - 1), g = (5L - 13) / 15 updates (parasite gestation at half of a 30-step slice),
v = 0.9925^(16 + (L-16)/2), s ~ 0.9.
- **A (second model, nominal h = 30/389 = 0.075):** L50 in [21, 28], sharp value 25.
- **B (my reading: h as measured, 0.049; host at mean speed):** L50 in [32, 40], sharp value ~36.
  The second model's own scaling (L* - 2.6 proportional to 1/h) gives this with the measured h; it used the nominal h.
- **C (host at median speed, g / 0.52, h measured) or contact-process crowding (second model's rival):** L50 <= 22.
- **Null:** establishment does not depend on L (flat across arms), or is non-monotone with more than one inversion.

## Rules
- The band containing the fitted L50 is the verdict; a fitted L50 in 28-32 or above 40 supports none of them, said so.
- B is falsified by any extinct-in-all-14 arm at L <= 28 or any established world at L >= 44.
- A is falsified by any established world at L >= 32 (second model's F1), or by >= 2 extinct worlds of 14 at L=16.
- Report all 126 worlds, unresolved included; the warm h and merit ratio of each seed; parasite genomes at the end
  (to confirm L did not change).

## Not decided by this experiment
Why: a band match is consistent with its model, it does not prove the mechanism. Equilibrium prevalence, injections per
parasite and plateau shape are descriptive only.
