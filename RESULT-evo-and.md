# Result: does AND arise and fix from the s2 dominant? (plan #481; prereg PREREG-evo-and.md, commit 604338d)

Run as pre-registered: `evo_and.py 40000 101..110`, 10 fresh seeds, 30x30 filled with the s2 dominant, default rates,
no parasites. Reader: `read_evoand.py` (commit 5da8090), output in `out/evo_and_reading.txt`.

| outcome (AND share of births, last 1,000 updates) | seeds |
|---|---|
| fixed (>= 0.5) | 0 of 10 |
| established (0.1-0.5) | 0 of 10 |
| background (< 0.1) | 10 of 10 (0.0054-0.0066) |

No seed reached a 250-update window with share >= 0.5. Pre-registered verdict: **my prediction (structural lock, fixed in
<= 1 of 10) is supported; the rival (s2's lock was its own RNG history, fixed in >= 3 of 10) is not.**

Descriptive, after the reading (`out/evo_and_maxwindow.txt`): the highest AND share of births in any 250-update window
in any seed is 0.0117. AND carriers are born all the time (18,238-19,643 of ~3.1 million births per seed, about 0.6%)
and never spread. So the barrier is not that AND fails to arise from this genotype; it arises and is not taken up.
For comparison (seen before the prereg, not evidence): from the ancestor, AND fixed in 2 of 3 tagged worlds within
~22,000 updates.

What this does not show: why AND carriers do not spread in the s2 background (cost in steps or length against the
reward, or which mutations produce them). That needs the merit of AND carriers against their parents, not counts.
Final genotype census per seed: `out/evo_and_census_s*.json`; top AND genome per checkpoint in `out/evo_and.jsonl`.
