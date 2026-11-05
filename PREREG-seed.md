# Seed entry preregistration: can a seed sent under SUBMIT.md live in the mature daily world? (plan #426)

Written 2026-11-05 15:28 UTC, before any run on seeds 1-12. Smoke test on seed 99 only (400 updates; excluded from the
verdict): ANC-len and DOM-len extinct at update 12 with 0 births; ANC-mean extinct at 51 with 4 births; DOM-mean
extinct at 240 with 297 births, peak 25. I saw these before writing the predictions below.

## Why
Plan #426 asked whether a hand-designed copier survives 30 epochs next to the evolved population. The daily world at
day 9 (update 360,000) has 893 organisms, mean merit about 4.1 million (tasks double merit), and about 73 births per
update, so a cell is overwritten every ~12 updates. SUBMIT.md lets a seed enter with merit = its length (10-256). Its
CPU share is merit / mean, so a seed may starve before its first division whatever its genome. This test separates
the genome from the entry rule.

## Design (`seed_entry.py`, world copy `out/seed_entry/world-day009.pkl`, sha256 prefix 05c361853762a700)
- 9 copies of one genome injected into the same 9 random cells per seed, label "seed"; every other organism "native".
- Arms: ANC (the hand-designed ancestor, 100 instructions, no tasks) or DOM (the world's most common genome at load);
  start merit "len" (the SUBMIT rule) or "mean" (population mean merit at injection). Four arms, seeds 1-12.
- World RNG reseeded per seed (same for all arms of a seed). Mutation as in the daily world.
- Stop at extinction of the label, fixation (all living organisms carry it), or 120,000 updates (3 daily epochs).
  The plan said 30 epochs; one epoch of this world costs ~16 CPU minutes, so 30 epochs x 48 worlds is out of reach.
  A label that fixes cannot die except with the whole population, so fixation counts as survival.

## Predictions
- P1: ANC-len extinct in 12/12, with 0 seed births in at least 11/12.
- P2: DOM-len extinct in 12/12, with 0 seed births in at least 11/12 (the entry rule kills even the dominant genome).
- P3: ANC-mean extinct in 12/12 before update 5,000 (the genome fails: no tasks, children start at merit ~100).
- P4: DOM-mean outlives DOM-len in at least 11/12 paired seeds, and fixes in at most 1/12 (neutral expectation for
  9 of ~893 is ~1%).

## What follows
If P2 holds, SUBMIT.md's entry rule is a death sentence for any seed in a mature world, and I change it before the next
seeding epoch (candidate: a seed starts at the population's mean merit), and say so where epoch 1 was announced.
If P2 fails, the rule is fine and the genome decides.
