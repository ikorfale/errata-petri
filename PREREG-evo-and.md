# Pre-registration: does AND arise and fix from the s2 dominant? (plan #481, written 2026-10-25 18:20 UTC before the run)

Design reviewed by a second model (Claude Fable 5.1) before the run; its three blocking points are adopted below.

## Seen before writing (not evidence)
- Tagged worlds from the ancestor, AND birth share per 1,000-update window (`out/tagged_s*.json`):
  s1 first >= 0.1 at 19,000, >= 0.5 at 22,000, then 0.94-0.95; s3 >= 0.5 at 10,000, then 0.94-0.96;
  s2 never above 0.11, flat at about 0.01 from 10,000 to 100,000. Fixation, when it happens, takes ~3,000 updates.
- One-step scan: 0 of 1,254 neutral dead-region fills hold a fitter task gainer.
- Smoke tests (seeds 998, 999, 500 updates): AND share of births 0.005-0.007, AND transients present.
- Not known: when the s2 dominant itself arose, so s2's ~90,000 updates at 0.01 is an upper bound on its own waiting time.

## Design
`python3 evo_and.py 40000 101,...,110`: 10 fresh seeds, default rates (copy_mut 0.0075, indel 0.05), no parasites,
30x30 filled with the s2 dominant (no standing variation: this tests the genotype, not s2's population).
40,000 updates = about twice the slower ancestor fixation (22,000). Checkpoint every 250 updates.

## Outcome per seed (on births, not on snapshot task sets, which reset at each division)
AND share of births over the last 1,000 updates: **fixed** >= 0.5; **established** 0.1-0.5; **background** < 0.1.
Also reported: the first checkpoint where the 250-update share reaches 0.5, if any.

## Predictions
- Mine (structural lock): fixed in <= 1 of 10.
- Rival (s2's lock was its own RNG history): fixed in >= 3 of 10, the ancestor's 2 of 3 rate scaled down.
- Exactly 2 of 10 supports neither; said so.
Counts of seeds only, no per-mutation rates. All 10 seeds reported, with the top AND genome at every checkpoint
where carriers exist and the final genotype census per seed.
