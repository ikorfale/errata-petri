# Guess before the neutral arm is read (or_counterfactual.py, rhea0987 board 107241)

Written 2026-10-29T05:16Z, after seeing only the "orig" and seed-1 rows of the real arm.

- Neutral arm (OR worth 2^0, everything else unchanged), from w62500 with the 41 OR performers tagged C:
  the C share at 65,000 is below 0.10 in at least 7 of 8 seeds, and OR performers stay under 50 at every census.
- Real arm: the C share at 65,000 is above 0.80 in at least 7 of 8 seeds.
- Wrong if: any neutral seed ends with C above 0.5 (then the clade had an edge besides OR), or a real seed loses the clade
  (then the sweep needed luck as much as reward).

## Break-even arm (OR worth 2^2 = NOT+NAND together), written 2026-10-29T05:31Z before it runs

C starts at 41 of 877 (4.7%). If OR's reward was the whole edge, C drifts: median C share at 65,000 over seeds 1-8 below 0.25,
no seed above 0.8. Wrong if 4 or more seeds end above 0.5 (then the clade carried an edge besides the reward). One caveat
known in advance: neighbours that do NOT+NAND are not all the same genotype, so "break-even" holds for merit, not
necessarily for every other trait.

## Break-even arm, result read 2026-10-29T06:12Z

C share at 65,000 over seeds 1-8: 0.038, 0, 0, 0, 0.291, 0, 0.034, 0. Median 0.0 (guess: below 0.25), no seed above 0.8, no
seed above 0.5. The guess holds. Mean 0.045 against a start of 0.047, which is what drift predicts, but one seed carries it.

## Neutral-type arm, written 2026-10-29T06:12Z before it runs

At 62,500 the 41 OR performers are 10 task sets; 25 of them are AND ANDN NOR OR ORN (call it D), merit-equal to the
background type AND ANDN NAND NOR NOT ORN when OR = 2^2 (both 2^13). Tag only D (OR_TAG=D), OR = 2^2, seeds 1-32.
If D is neutral, its expected share is a martingale: mean D share at 65,000 stays near 25/877 = 0.0285.
- Guess: the 95% bootstrap CI (over seeds) of the mean D share at 65,000 contains 0.0285, and at least 16 of 32 seeds end at 0.
- Wrong if the CI's lower bound is above 0.057 (D has an edge besides the reward: speed, copy fidelity, placement), or its
  upper bound is below 0.0285 (D is worse than its merit says).
- Known limit: drift shares are heavy-tailed; 32 seeds can only see an edge of roughly 2x, not a few percent.

## Neutral persistence baseline, written 2026-10-29T06:15Z before it runs (neutral_survival.py, w62500, seeds 1-4)

107 of 108 day-2 OR origins were never seen at a second census. Guess: of 877 organisms tagged at 62,500, between 3% and
30% still have descendants 500 updates later. If that share is at least 5%, then 0 of 107 is unlikely under neutrality
(0.95^107 = 0.4%) and most OR origins were worse than their neighbours, not unlucky. Wrong (for that reading) if it is under 2%.
Caveat: "seen at a census" is not the same age distribution as "tagged at a random moment", and a census needs an
OR-capable descendant, so I also count descendants with the ancestor's exact task set.

### Read 06:19Z: 62,500 baseline, and why it is not the baseline

Seeds 1-4 from w62500: 10, 11, 14, 5 of 877 labels have descendants at +500 (40/3508 = 1.1%; same task set 32/3508 = 0.9%),
3-4 at +1000. Below my 3-30% guess. But this world sits at the start of the OR sweep (the real arm takes C to 1.0 by
65,000), so every non-OR label is being killed by the sweep: the survivors here are mostly the sweeping clade. Rerun from
worlds not in a sweep: daily/base/day-001 (update 40,000, start of day 2, OR at 0) and w61500, seeds 1-4. Same guess and
same reading rule as above, decided before those rows are read.

### Read 06:25Z: clean baselines

Worlds not in a sweep, seeds 1-4 each, share of labels with a descendant of the ancestor's exact task set at +500:
40,000: 76/3348 = 2.27% (any descendant 2.81%); 61,500: 80/3464 = 2.31% (2.71%). **My guess was wrong**: below 3%, and
below the 5% line I set for "most OR origins were worse than neighbours". At 2.3%, 107 origins would leave about 2.4 lines
past a second census by luck alone; 0 has probability 0.08. A weak hint that OR origins were on average worse than
neutral, not a finding. And one survivor out of 108 needs no special explanation if the founder was neutral.
