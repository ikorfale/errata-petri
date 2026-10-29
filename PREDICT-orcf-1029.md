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
