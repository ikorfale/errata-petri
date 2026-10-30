# Merit method 1 vs 4, six paired seeds: verdict (30.10)

Pre-registration: PREDICT-merit-method-1030b.md (D1, D2 written 05:26 UTC before seeds 14-16 ran; D3 and the dG note
added 08:39 UTC after the arms finished but before any output was opened). Re-derive: `python3 mm_verdict.py 11 12 13 14 15 16`
(output in out/mm_verdict_6.txt). U = mean unexecuted share of births over rows 76k-80k; G = mean genome length at 80k.

| seed | U m1 | U m4 | dU | G m1 | G m4 | dG |
|---|---|---|---|---|---|---|
| 11 | 0.278 | 0.211 | +0.067 | 89.3 | 94.2 | -4.9 |
| 12 | 0.227 | 0.207 | +0.020 | 91.3 | 92.4 | -1.1 |
| 13 | 0.244 | 0.233 | +0.012 | 99.9 | 99.0 | +0.9 |
| 14 | 0.248 | 0.191 | +0.057 | 84.2 | 98.1 | -13.9 |
| 15 | 0.231 | 0.192 | +0.039 | 89.5 | 103.2 | -13.6 |
| 16 | 0.282 | 0.238 | +0.043 | 96.9 | 98.1 | -1.2 |

(Seeds 11-13 recomputed by the script: dU for seed 12 is +0.020 here, +0.021 in the first verdict; dG -1.1 vs -1.2.
Rounding of the earlier hand table, same data.)

- Blind expectation for seeds 14-16 (dU > 0 in at least 2 of 3): **held**, 3 of 3.
- D1, sign test over 6 pairs: **supported**, 6 of 6, one-sided p = 1/64 = 0.016.
- D3, one-sided paired t on dU: **supported**, t = 4.65, df 5, p = 0.003.
- D2: mean dU +0.040, 95% t interval [+0.018, +0.062]. Mean dG -5.6, interval [-12.5, +1.3]: contains 0, **no dG claim**.

Reading: in this world, paying merit by executed length (Avida method 4) instead of copied size (method 1) lowers the
unexecuted share of births by about 4 points (2 to 6). That is the cost of carrying unexecuted code under method 1,
measured, with 3 of the 6 seeds blind.

Not claimed: anything about genome length. Note only, as a lead for a separate pre-registration: method-4 genomes
ended longer in 5 of 6 pairs, by about 14 units in seeds 14 and 15 and 1 to 5 in the others. That is the opposite of
my first guess (P3 in PREDICT-merit-method-1030.md expected shorter). If it holds, method 4 removes ballast and the
genome fills with code that runs instead of shrinking.
