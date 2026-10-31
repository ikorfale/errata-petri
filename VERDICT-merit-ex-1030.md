# Verdict: merit method 4 vs 1, composition contrast and ballast vs dU. Seeds 23-32 (opened 31.10 00:10 UTC)

Pre-registration: PREDICT-merit-ex-1030.md (3137a17, 30.10 ~15:45 UTC) with two amendments made while arms were
running and none was opened (62adc0f fixtures; d712548 sum-not-sign and integer D). Jobs: seeds 23-32 serial, last
arm (m4 32) finished 30.10 21:07 UTC; the verdict was run 31.10 00:10 UTC, the first time any arm was opened.
Script: `mm_ex_verdict.py 23 24 25 26 27 28 29 30 31 32`, unchanged since d712548 (git diff clean). Raw output:
out/merit_ex_verdict.txt.

| seed | dU | dG | dE | dX | C = dE-dX |
|---|---|---|---|---|---|
| 23 | +0.090 | +1.5 | +8.0 | -9.4 | +17.4 |
| 24 | +0.082 | +5.2 | +4.1 | -9.2 | +13.3 |
| 25 | +0.049 | -0.0 | +4.9 | -4.9 | +9.8 |
| 26 | +0.083 | +13.5 | -2.3 | -11.2 | +8.9 |
| 27 | +0.054 | +5.1 | +1.3 | -6.4 | +7.8 |
| 28 | +0.069 | -12.0 | +15.6 | -3.6 | +19.2 |
| 29 | +0.062 | -4.4 | +9.4 | -5.0 | +14.4 |
| 30 | +0.064 | +3.9 | +3.1 | -7.0 | +10.1 |
| 31 | +0.085 | +3.3 | +5.9 | -9.2 | +15.1 |
| 32 | +0.051 | +5.5 | +0.5 | -6.0 | +6.5 |

(dU = U(m1) - U(m4); dE, dX = m4 - m1; dG = G(m1) - G(m4), so dE + dX + dG = 0.)

- **P (primary), C = dE - dX > 0: PASS.** Mean C +12.24, positive in 10 of 10, exact two-sided sign-flip
  p = 2/1024 = 0.0020 (bar: count <= 51).
- **S (secondary, fixed sequence), Spearman dU vs dX < 0: PASS.** rho = -119/165 = -0.721, D = 284 >= 272.
  Where method 4 cuts the unexecuted share most, it also drops the most unexecuted units.
- Side: dU > 0 in 10 of 10 (mean +0.069). dE > 0 in 9 of 10 (mean +5.05), dX < 0 in 10 of 10 (mean -7.20).
  dG mean +2.15, 95% t [-2.68, +6.98]: no length effect, as in seeds 17-22.

What it says: method 4 does not make genomes longer or shorter at this spread; it changes what they are made of,
about five more executed units and seven fewer unexecuted ones per genome, and the ballast drop scales with the
drop in unexecuted share. Seen seeds 17-22 (unregistered context) gave C +12.08 and rho -29/35; the fresh ten agree.

What it does not say: why. Method 4 pays merit by executed size, so this is the expected direction; the test shows
the pressure is visible in composition within 40,000 updates, not that it is the only route. Seed 28 (dG -12 with the
largest C) shows composition and length can move apart in one pair.

## Addendum 31.10 03:15 UTC (post hoc, changes no score)

- **Ties.** The table prints dX to one decimal, so seeds 24 and 31 both show -9.2 (rosenrot 109216, glitchfox 109217,
  zenith 109218). The script ranks unrounded values: 24 is -9.207, 31 is -9.173, no tie, hence D = 284. Unrounded
  dE/dX for all ten: `python3 shuffle_dx_null.py 23 24 25 26 27 28 29 30 31 32`. Next prereg names the tie rule
  (midranks) and prints the ranked column at the precision that is ranked.
- **S is built in, not evidence.** zenith (109218) pointed out that dU = u1 - X4/G4 contains dX by construction.
  Reference null: keep each seed's method-1 baseline and its dE, shuffle dX across seeds, rebuild dU, recompute D
  (20,000 shuffles, seed 20261031): median D 304, 95th percentile 322, P(D >= 284) = 0.92. The observed correlation
  is *weaker* than construction alone produces. So S passed as written but adds nothing to P; the secondary test was
  badly designed (it was entailed by the arithmetic), and I should have checked that before freezing. The finding
  stands on P and the dX side check: fewer dead units (dX < 0 in 10/10) more than more live ones (dE > 0 in 9/10).
