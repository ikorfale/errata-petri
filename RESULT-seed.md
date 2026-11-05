# Seed entry: result (plan #426, 2026-11-05)

Pre-registration: PREREG-seed.md (committed ad44c11 before seeds 1-12 ran). Re-derive: `python3 out/seed_entry/run.py`
(about 3 minutes on 4 cores), verdict in `out/seed_entry/verdict.txt` from `seed_entry_verdict.py`.
World: a copy of the daily world at day 9 (update 360,000; 893 organisms; mean merit ~4.1 million; ~82 births per
update over the last 500 updates; the prereg's ~73 was the all-time average). 9 copies of one genome per run, 12 seeds per arm.

| arm | extinct | seed births (12 seeds) | last copy gone at update (median, range) |
|---|---|---|---|
| ANC-len: hand-designed ancestor, SUBMIT rule (merit = length) | 12/12 | 0 in all | 30 (12-52) |
| DOM-len: the world's own dominant genome, SUBMIT rule | 12/12 | 0 in all | 30 (12-52) |
| ANC-mean: ancestor, starting at the population's mean merit | 12/12 | 0-4 | 43 (14-73) |
| DOM-mean: dominant, starting at mean merit | 12/12 | 37-57,898 | 579 (76-4,647) |

All four predictions held (P1-P4).

**What it shows.** Under the entry rule of SUBMIT.md, a seed's genome does not matter at all: ANC-len and DOM-len died
at exactly the same update in every seed, because neither executed a single instruction. With merit ~100 against a mean
of ~4 million, a seed gets about one instruction per 1,400 updates, and its cell is overwritten by a neighbour's child
every ~11 updates. The best genome in the world, sent in under my rules, was dead in under 60 updates.

With a fair start the genome decides: the ancestor (no logic tasks) still dies within 73 updates because its children
start at merit ~100; the dominant genome lives like a native and drifts out (9 of 893 copies, neutral; peak 320 copies
in seed 6, never fixed). So the plan's question "does a hand-designed copier survive 30 epochs?" has a short answer:
no seed survives one epoch in this world, and under the old rule none could even start.

**Change made.** SUBMIT.md: from the next seeding epoch a seed starts at the population's mean merit (one fair
gestation); after that its children earn merit like everyone else. Smoke test on seed 99 (seen before the predictions)
is excluded from the table.

**Limits.** One world state (day 9), one injection size (9), mutation on. "Neutral drift out" for DOM-mean is the
expected result for a tiny neutral minority; it is not evidence that the dominant genome is weak.
