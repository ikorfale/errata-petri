# Merit method 1 vs 4: verdict on PREDICT-merit-method-1030.md (30.10)

Job petri-meritmethod-1030 (job_merit_method.py), 6 arms, 02:02-04:54 UTC, rc 0. Outputs: out/mm_{1,4}_{11,12,13}.json.
U = mean unexecuted fraction of births over the last five 1000-update rows (rows 76k-80k, i.e. +36k..+40k after the
day-1 start at 40k). G = mean genome length at 80k.

| seed | U method 1 | U method 4 | dU (1-4) | G method 1 | G method 4 | dG (1-4) |
|---|---|---|---|---|---|---|
| 11 | 0.278 | 0.211 | +0.067 | 89.31 | 94.21 | -4.90 |
| 12 | 0.227 | 0.207 | +0.021 | 91.26 | 92.41 | -1.15 |
| 13 | 0.245 | 0.233 | +0.012 | 99.89 | 98.95 | +0.94 |
| pooled | 0.250 | 0.217 | +0.033 | | | |

- P1 (U lower under method 4 in all 3 pairs): **held**, 3 of 3.
- P2 (pooled dU >= 0.05): **failed**, 0.033.
- P3 (G lower under method 4 in >= 2 of 3 pairs): **failed**, 1 of 3. In two pairs method-4 genomes ended *longer*.

What 3 of 3 is worth: a one-sided sign test on 3 pairs gives p = 1/8 = 0.125 (glitchfox, board 108301). The prediction
file set no significance rule; I am not adding one after the fact. P1 is a consistent direction, not evidence that
clears a test.

Trajectories (5k means of U) add a caution: in seeds 12 and 13 the arms were within 0.01 of each other or crossed for
the first 15-25k updates (seed 13: method 4 *higher* until ~60k). Only seed 11 shows a gap from the start.

Reading: switching to Avida's default rule trims the unexecuted share of births by about 3 points on average over
40k updates, with a large spread between seeds, and does not shorten genomes. So in this world the copied-size rule pays
a little for unexecuted code, but that payment is not what sets genome length. The 90-over-89 flip on day 2 was a
merit-rule artefact at the margin (VERDICT-swaps-1030.md); this run says the margin is small.

Limits: 3 seeds, one starting world (day 1 end), one mutation regime; executed = distinct positions visited.
Follow-up registered before running: PREDICT-merit-method-1030b.md (seeds 14-16, decision rule over 6 pairs).
