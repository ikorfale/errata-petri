# #535: can a swapped AND carrier get ANDN back in one more step? (written 29.10 12:58 UTC, date -u, before the run)

Step 0 (out/and_census_phase.txt): in the 10 evo_and final censuses, 94 organisms compute AND and none keeps ANDN; 52 of
them are AND+NAND+NOT+ORN and fast (<300 steps). In s2's background, AND replaces ANDN.

Run: swapback.py takes every distinct genotype in those censuses that computes AND without ANDN and divides in <2000
steps, enumerates every one-step mutant (substitution, insertion, deletion, alphabet a-z), traces it (genome_trace,
seed 7, cap 2000, as out/two_step.py) and keeps mutants computing AND+ANDN. Reports per parent: count, fastest, and
length mod 3 of the hits; overall share of hits that are fast (<300) and 2 mod 3.

Guesses (no test, a guess I can lose):
- G1: at least one parent has a fast (<300) AND+ANDN one-step mutant. If none does, the dual is at least two steps from
  every swapped carrier, which with ~0.6% AND births would explain why it never showed.
- G2: among hits that divide at all, those at 2 mod 3 are faster than those at 0 or 1 mod 3 (median steps), as the phase
  rule says for the s2 copy loop.
- If G1 holds, the next step is selection, not reachability: head to head of the fastest hit vs its parent (h2h as
  out/h2h_hand.py). Not run in this pass.

## Result (29.10 13:04 UTC, date -u; out/swapback.txt, 295 s)

62 parents, every one-step mutant traced. AND+ANDN mutants: 8 in total, from 5 parents; 3 divide in <2000 steps, all at
0 mod 3 (325, 514, 545 steps against parents at 186 and 545), none fast.
- G1 (a fast one-step AND+ANDN mutant exists): **wrong.** 0 fast.
- G2 (2 mod 3 hits faster): **not testable.** The only 2 mod 3 hit never divides.
So from what s2 worlds actually hold, the dual is at least two steps away from every swapped carrier, and the one-step
forms that do divide are slower than their parents. With AND births at ~0.6% and AND lines short-lived, this fits the
dual never appearing. Limits: parents are the final-census snapshot (94 AND organisms, 62 genotypes), not the ~19,000 AND
births per seed; two-step paths not searched; trace seed 7 only.
