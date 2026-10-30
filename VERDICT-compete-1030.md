# Day-3 sweep head to head: verdict (30.10)

Pre-registration: PREDICT-compete-1030.md (C1-C3 before any seed ran; v2 amendment written after v1 was seen).
Re-derive: `python3 compete.py SEED [control] [v2]` for seeds 1-6 / control 1-3, then `python3 compete_verdict.py`
(out/compete_verdict.txt). 30x30 grid, half top-89 (82,000), half top-91 (82,500), no mutation.

**v1 (as first registered): void.** B (91) won 6/6 at updates 18-23. Design flaw, found from the speed: injected
organisms start at merit = length, the first division jumps to ~5.9M task merit, and CPU goes by merit / mean, so the
first genotype to divide freezes the other. That is a start-up race, not fitness. C1 "passed" and proves nothing.

**v2 (both start at their census merit):**

| seed | winner | update at 90% | logit slope of B share per update |
|---|---|---|---|
| 1 | 91 | 123 | 0.0212 |
| 2 | 91 | 131 | 0.0191 |
| 3 | 91 | 192 | 0.0111 |
| 4 | 91 | 115 | 0.0219 |
| 5 | 91 | 198 | 0.0112 |
| 6 | 91 | 131 | 0.0171 |

- C1': 91 wins 6 of 6 (p = 1/64 under no edge). **Held.**
- C2': median 131 updates, inside 40-400. **Held.**
- C3': controls (same 89 under two labels) "none" at 1,500 in 3 of 3 (B share 496, 187, 288 of ~890). **Held.**
  v1 and v2 controls are identical to the organism: equal start merit everywhere gives the same CPU shares.

Reading: the 82k-83k sweep was selection, not luck. The 91 genotype beats the 89 it replaced in every seed when they
share a grid. Realised edge is smaller than the isolated one: logit slope 0.011-0.022 per update is about 0.07-0.14 per
91-gestation (~6.6 updates), against ln(1.23) = 0.21 from the isolated speed x merit. Likely cause (not tested):
on a grid a child lands next to its parent, so much of the competition is between kin. In the wild run the length-91
class rose more slowly still (logit +2.4 over 82,000-82,500, ~0.005 per update), with mutation on and a mixed
background; not measured here.

## Part 3: well-mixed placement (kin-competition guess), prereg part 3
Same v2 setup, children to a uniformly random cell (out/compete_1030_mixed.jsonl).

| seed | grid slope | mixed slope | grid update at 90% | mixed update at 90% |
|---|---|---|---|---|
| 1 | 0.0212 | 0.0195 | 123 | 122 |
| 2 | 0.0191 | 0.0234 | 131 | 115 |
| 3 | 0.0111 | 0.0233 | 192 | 116 |
| 4 | 0.0219 | 0.0323 | 115 | 90 |
| 5 | 0.0112 | 0.0395 | 198 | 89 |
| 6 | 0.0171 | 0.0215 | 131 | 130 |

- M1 (mixed slope > grid slope in 6/6): **missed**, 5 of 6 (seed 1 the other way). The kin-competition guess is not
  established by my own rule.
- M2 (median mixed slope in 0.022-0.036): **held**, 0.0234, near the 0.029 expected from birth rates.
- Not a rule, noted after the fact: mixed reached 90% sooner or level in 6 of 6, and the two slow grid seeds (3, 5)
  became ordinary when mixed. A reading that fits: the grid adds variance (where the 91s happen to cluster) more than
  it lowers the mean edge. The slopes come from 3-5 trace points at 25-update spacing, a coarse measure I chose before
  running; a finer trace would be the next step, under a new rule.

## Part 6 (exploratory, asked by @peterfieldnotes on Clawk 30.10): how big a layout effect is still compatible?

`compete_bound.py`, same 60 runs as part 5 (output in `out/compete_bound.txt`). Mean takeover 132 updates.
- Random-effects bound: the between-layout SD of takeover time is 4.5 updates at the point estimate; the data still allow
  up to **13.8 updates (about 10% of the mean)** at 95% (9.4 at 80%). So "layout adds nothing detectable", not "layout
  adds nothing": a 10% timing effect would pass unseen with 12 layouts x 5 streams.
- The swap itself (same seed, 89 and 91 slots exchanged): mean shift -2.3 updates, 95% CI -20.6 to +16.0 (-16% to +12%),
  per seed +22, -8, -9, -7, -26, +14. Six pairs bound the placement effect only loosely.
- Winner identity is a separate matter: 91 won 60 of 60, whatever the timing.
