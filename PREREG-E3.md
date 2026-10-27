# E3 preregistration: why did switching off old age move L50 from 26.9 to 31.5? (plan #483)

Written 2026-10-27 before any E3 world ran (smoke tests on seed 99 only, 30 updates; one anchor check on seed 1, L=24).

## What E2 found (fixed, out/e2_verdict.txt)
Local L50 26.85 (bootstrap 25.33-28.27), global 28.8 (27.45-29.99, straddles +3), **noage 31.52 (30.36-32.42, shift >= 3)**.
My E2 prediction was that old age shifts L50 by less than 3; it was wrong. Age accounted for 17.5% of parasites lost
with their host in local mode.

## Candidate mechanism (mine, found 27.10 by reading petri.py, after seeing E2)
`o.age += n` counts every instruction run in the cell, and an infected host gives every second one to its parasite
(petri.py, run_update). The age limit is 20 x genome length instructions, so an infected host dies after the same
number of updates as a healthy one but has done only half of its own work. The parasite thread dies with it.

## Arms (switch `age_mode` in petri.py; default "instr" reproduces E1/E2 bit for bit)
- **local** (anchor): age_mode instr. L in {24, 28, 32}. Must equal E2's local arms world for world.
- **host**: age counts only the host's own steps, so an infected host lives about twice as many updates. L in {24, 28, 30, 32, 36, 40}.
- **updates**: age grows by `slice` (30) per update lived, whatever the merit, so the limit is 20 x glen / 30 updates
  for everyone. L in {24, 28, 30, 32, 36}. Ages carried from the warm world stay on the same scale.
Same seeds 1-14, warm worlds, 9 seeded hosts, indel 0, inject never drawn, 3000 updates, as E2. 196 worlds, two lab jobs
(`job_e3a.py` seeds 1-7, `job_e3b.py` 8-14).

## Predictions (mine, written now)
- **H1, parasite steps age the host:** host-mode L50 interval lies wholly at or above 29.88 (shift >= 3). I put this at
  about 55%: noage removed age death for everyone, host mode only halves it for infected hosts.
- **H2, updates-age is equivalent for this question:** updates-mode interval wholly below 29.88 (shift < 3), because an
  infected host's lifetime in updates is the same as in instr mode; only merit differences change it.

## Verdict (`e3_verdict.py`, mechanical, written before data)
- Local arms must match E2 local world for world (outcome and final infected count); any mismatch voids the verdict.
- Outcomes, L50 and the seed-cluster bootstrap interval (2000 resamples) are e2_verdict.py's functions, unchanged.
- Shift vs 26.88: >= 3 only if the whole interval is >= 29.88; < 3 only if the whole interval is < 29.88; else undecided.
- H1 supported if host shift >= 3; falsified as the main cause if < 3. H2 holds if updates shift < 3, fails if >= 3.
- Descriptive only: share of the noage shift (31.52 - 26.88) reproduced by host mode's point L50.

## Not decided here
Why age matters at all at the population level (fewer injection attempts per infected host vs fewer births of
infected hosts). The loss counts by cause are reported, not tested.
