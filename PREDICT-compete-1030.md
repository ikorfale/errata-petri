# Day-3 sweep: does 91 beat 89 head to head? (30.10)

Written before compete.py was run on any seed (only a 20-update timing check of the control arm, seed 99, was run;
its outcome is not a test). Question left open by daily/ERRATA-day-003.md: alone, the top length-91 genotype divides
in 198 steps against 237-241 for the top 89 (+23% merit per step, same 7 tasks). Does that turn into a takeover when
they compete for the same grid, or was the 82-83k sweep luck?

Design (compete.py): 30x30 world, daily settings, copy_mut = indel = 0. Grid filled at random, 450 copies of the top
89 at 82,000 (A) and 450 of the top 91 at 82,500 (B). Stop when one side holds >= 90% of the living, or at 1,500
updates ("none"). Seeds 1-6. Control arm: the same 89 genotype under both labels, seeds 1-3.
Known bias: an injected organism's first merit is its length (89 vs 91, +2% for B) until its first division.

Predictions:
- C1 (decides): B (91) wins in 6 of 6 seeds. Under no advantage at most half would; 6/6 has p <= 1/64.
- C2: median update at which B reaches 90% is under 1,000.
- C3 (control, not a rule): no side reaches 90% in most control seeds by 1,500 updates (neutral drift is slow at N=900).
A miss on C1 means the isolated speed gain does not carry into competition (for example slower in a crowded grid,
or births landing on own kin); I will say so and not call the 82k sweep adaptive.
