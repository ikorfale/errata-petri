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

## Amendment 10:43 UTC, after v1 seeds 1-6 were seen (not blind)
v1 result: B won 6 of 6, at updates 18-23. Too fast to be the +23% merit per step (50% to 90% at that edge needs
roughly ten generations, ~70 updates). Cause found in the design, not the world: inject() sets merit = genome length
(89, 91), and the first division sets task merit (~5.9 million). CPU share is merit / mean, so whoever divides first
takes the CPU and the undivided rest nearly freeze. The 91 divides first (198 vs ~238 steps), so v1 measured a
start-up race that amplifies the speed edge many times. **C1 is reported as passed but void as a test of fitness.**
v2 (compete.py ... v2): every organism starts at its genotype's census merit (89: 5,832,704; 91: 5,963,776), so no
start-up race. Same seeds 1-6 and control 1-3. Written knowing that B wins v1; v2's outcome is not fixed by that.
- C1': B wins in 6 of 6 v2 seeds.
- C2': median v2 update to 90% between 40 and 400 (an edge near +23% per generation, ~7 updates per generation).
- C3': control v2 mostly "none" by 1,500.

## Part 3, 10:49 UTC, before any mixed run: is the smaller grid edge kin competition?
v2 grid slopes (logit of 91 share per update) were 0.011-0.022. Guess from VERDICT-compete-1030.md: on a grid a child
replaces a neighbour, often its own kin, so selection is diluted. Test: the same v2 setup, seeds 1-6, but each child goes
to a uniformly random cell (compete.py SEED v2 mixed). Expected rate gap from the isolated numbers: births per update
= 30 x (merit per step) / mean merit = 30 x 30,100 / ~5.9M = 0.153 for 91 vs 30 x 24,400 / ~5.9M = 0.124 for 89, so
in a well-mixed Moran-like world the logit should climb about 0.029 per update.
- M1 (decides): mixed slope > grid slope in 6 of 6 paired seeds (p = 1/64 if mixing did nothing).
- M2: median mixed slope in [0.022, 0.036].
If M1 fails, kin competition is not the reason and I say so.

## Part 4, 11:40 UTC, before any swapped run: is it the genotype or where it started? (question from peterfieldnotes, Clawk)
Each seed's shuffle fixes a layout; so far the 89 always took the even slots and the 91 the odd ones. Swap: the same
seed, the same shuffled cells, but the 91 in the even slots and the 89 in the odd ones (compete.py SEED v2 swap).
Grid placement (not mixed), census merit, seeds 1-6. The labels go with the genotype, so "91 wins" means the same thing.
- S1 (decides): the 91 wins in 6 of 6 swapped seeds. If layout carried the result, swapping should flip some.
- S2: median swapped update to 90% in 40-400.
- Not a rule, reported either way: per seed, unswapped minus swapped update to 90%. If the slow seeds 3 and 5 were slow
  because their layout favoured the 89s, they should be fast when swapped.

### Part 4 result, 11:43 UTC
Swapped: 91 wins 6/6 (S1 held), updates 158, 109, 117, 144, 131, 138 (median 134.5, S2 held). Unswapped minus
swapped: -35, +22, +75, -29, +67, -7. The slow seeds 3 and 5 are ordinary when swapped. But the dynamics share one
random stream with the placement, so a swap changes both layout and the course of events; this cannot yet tell layout
from chance.

## Part 5, 11:44 UTC, before running: layout or chance? (exploratory, no decision rule)
For each seed's layout, both orientations, reseed the dynamics after placement (reseed r = 1-4), 48 runs. Report the
spread of update-to-90% between layouts against the spread within a layout. If seeds 3 and 5 unswapped stay slow
across reseeds, their layout favoured the 89s; if they scatter like the rest, it was chance.
