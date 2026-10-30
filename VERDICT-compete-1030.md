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
