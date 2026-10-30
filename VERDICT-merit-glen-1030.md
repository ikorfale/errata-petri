# Verdict: does merit method 4 grow genomes? Seeds 17-22 (30.10)

Pre-registration: PREDICT-merit-glen-1030.md (commit 2b9fc74, 10:14 UTC; amendment E1/E2 before any output of seeds
17-22 was opened). Jobs petri-meritmethod-1030c (17-19) and -1030d (20-22); last arm finished 14:37 UTC.
Script: `mm_verdict.py 17 18 19 20 21 22` (G1 line added 14:36 UTC, before the last arm finished; it only counts
dG < 0). Raw output: VERDICT-merit-glen-1030.txt.

| seed | U m1 | U m4 | dU | G m1 | G m4 | dG |
|---|---|---|---|---|---|---|
| 17 | 0.231 | 0.182 | +0.049 | 92.0 | 92.8 | -0.8 |
| 18 | 0.237 | 0.186 | +0.051 | 94.3 | 98.0 | -3.7 |
| 19 | 0.269 | 0.166 | +0.102 | 100.8 | 92.3 | +8.6 |
| 20 | 0.262 | 0.218 | +0.044 | 99.5 | 100.4 | -0.9 |
| 21 | 0.254 | 0.177 | +0.077 | 101.1 | 93.5 | +7.6 |
| 22 | 0.269 | 0.203 | +0.065 | 96.7 | 102.7 | -6.0 |

Primary rules (genome length G):
- G1, dG < 0 in 6 of 6: **failed**, 4 of 6 (p = 0.34).
- G2, one-sided paired t on dG: **failed**, t = 0.33, p = 0.62. Mean dG +0.8, 95% interval [-5.5, +7.1].

The seen lead (method-4 genomes longer in 5 of 6 pairs, mean dG -5.6) did not replicate. Under the pre-registered
wording: an effect on length is not detected at this spread; a true effect of the seen size (-5.6) is outside the
new interval's centre but not excluded by it.

Amendment rules (glitchfox 108519), composition of the genome:
- E1, executed units E = G(1-U) higher under method 4 in 6 of 6: **held** (p = 1/64), mean +5.6.
- E2, unexecuted units X = G·U lower under method 4 in 6 of 6: **held** (p = 1/64), mean -6.4.

Side check: dU > 0 in 6 of 6 again (mean +0.065, interval [+0.042, +0.088]; seeds 11-16 gave +0.040).

Reading: in this world the merit method clearly changes what a genome is made of; whether it changes length, 6 pairs
cannot tell. Method 1 (merit from copied size) carries about 6 more unexecuted units and about 6 fewer executed ones,
with no length difference detected. Limits: arm
means, not per-genome values; one world, one reseed point (update 40,000); 40,000 updates per arm.
