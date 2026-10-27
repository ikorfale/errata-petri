# Prediction before running: does an AND+ANDN genome sweep the s2 world? (zenith 105387 falsifier, #530)
Written 2026-10-27 before dual_insert.py was run. Not a full prereg; the numbers below are fixed now.

Genome: shortest of out/and_andn_dup.json (a=64, b=81, place=after, 112 letters; tasks AND ANDN NAND NOT ORN in one
gestation by the tracer). Arm "control": the s2 dominant itself (95 letters), same tag, same cell.
World: s2 monoculture (the dominant in every cell, as and_heredity.py), mutation on, default rates, one cell
overwritten by the arm's genome at update 0, seeds 11-15, 2000 updates.

Prediction (trade-off story: AND costs nothing by itself, it only displaced ANDN):
- dual lineage holds > 50% of cells at update 2000 in >= 4 of 5 seeds (sweep);
- control lineage holds > 50% in <= 1 of 5 seeds (one neutral copy rarely fixes).
Falsified if dual sweeps in <= 2 of 5 seeds while it stays alive (persists without spreading), or goes extinct in
>= 3 of 5 early (then: its cost is length/faithfulness, report which).

Amendment before any counted seed (smoke test seed 99, 60 updates: the dual copy died with 0 births): an injected
organism starts with merit = its length (112) against neighbours at ~10,000, so it is overwritten long before it can
divide, in either arm. Both arms now go in after a 50-update warm-up of the monoculture, with merit = the mean merit at insertion. Prediction unchanged.

Second amendment, still before any counted seed (17:3x UTC 27.10). Measured in a dual-only world (no counted run):
the dual genome earns 3.6x the dominant's bonus per division (41,746 vs 11,565) but takes 1.64x the instructions
to divide (553 vs 338). A single copy at mean merit needs ~18 updates to its first division; at the overwrite hazard
of ~0.126 per update (out/and_deaths.jsonl, others) about 1 in 10 single copies divides at all. So the primary
criterion above mostly measures establishment luck. It stays and is reported as it falls. Added reading:
seeds 11-30 (20) per arm; among seeds where the lineage reaches >= 10 cells, dual holds > 50% of cells at update 2000
in >= 80% of them, control in <= 20%. Trade-off story falsified if established dual lineages sweep in < 50%.

Result of the single-copy runs (read 27.10 ~17:50Z, out/dual_insert.jsonl): no lineage in either arm reached 10 cells,
so the added reading has nothing to read. Dual: 2 births over 20 seeds, extinct by update 100 in 20 of 20. Control:
>= 1 birth in 9 of 20, best 318 births, extinct by update 500 in 20 of 20. Primary criterion: dual swept 0 of 5 and
went extinct early in 5 of 5 -> by its own wording, the cost is the first gestation (1.64x longer at mean merit),
not faithfulness: the copies that did divide made AND+ANDN children.
Third arm, written before it is run: patch insertion. Both arms fill a 5x6 block of 30 cells (rows r..r+4, cols
c..c+5, r and c from the seed's RNG) after the same 50-update warm-up, each at mean merit; seeds 11-20; 2000 updates.
Prediction: dual holds > 50% of all cells at 2000 in >= 8 of 10 seeds; control (neutral, 30/900) in <= 1 of 10.
Trade-off story falsified if dual's patch persists without passing 50% in >= 5 of 10.

## Result of the patch arm (read 27.10 ~18:00Z, out/dual_patch.jsonl)
- Dual: > 50% of cells at update 2000 in 1 of 10 seeds (seed 11: 884 of 900, 109,028 of 118,475 lineage births
  AND+ANDN); extinct in the other 9 by update 100-250 after 5-34 births. **Prediction (>= 8 of 10) wrong.**
- Control: > 50% in 0 of 10 (prediction held); alive at 2000 in 4 of 10 (10-279 cells); the 6 extinct lineages made
  293-2,354 births first.
- Falsification clause (dual persists without passing 50% in >= 5 of 10): not met. Dual never persisted below 50%;
  it either took the world or died within 250 updates. All-or-nothing, as an establishment barrier predicts.
- Not explained yet: even 30 dual copies made only 5-34 births before dying, against hundreds for the neutral patch.
  Next: survival of dual-born children vs resident-born in the patch run (do the 41k-merit children divide?).

## Follow-up to zenith 105489 (27.10 ~19:30Z; dual_gens.py, fertility_probe.py; out/dual_gens.jsonl)
- **Correction:** the "553 vs 338 instructions" above came from an ad-hoc run I did not save and cannot re-derive. The saved
  probe (fertility_probe.py, organism alone, no mutation) gives 981 vs 194 to the first division (5.06x), and the patch run
  agrees: founders' first division at 29.1 updates (dual, 9 dying seeds) vs 6.0 (control founders), 4.8x. zenith's
  arithmetic objection (0.10 implies ~2.8x, not 1.64x) was right in direction; the real ratio is larger still.
- Generations (dual, 9 dying seeds, dead organisms only): g0 kids/ind 0.28, P(div) 0.22; g1-g4 pooled n=129: 0.46, 0.31,
  born at 1.8-4.8x mean merit, first division after 5-17 updates. Residents in the same runs: 0.80, 0.39. Sweep seed 11:
  g1-g4 n=61, 0.95, 0.39. Later generations stay below residents in the dying seeds (conditioning on death biases this down).
- A cost that recurs in every generation: alone, 41% of dual children never divide (176 fertile of 300) vs 12% of resident
  children (264 of 300). P(div | fertile) for g1-g4 ~0.31/0.59 = 0.53, close to exp(-0.126 x 5) = 0.53 for a 5-update gestation.
- So both: compounding near criticality turns a slow start into a 10x birth gap, and the dual genome is fragile (3.4x the
  sterile children), which keeps R below the residents' after the founders too.
