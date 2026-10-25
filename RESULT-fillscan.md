# #481 neutral-fill scan: result (25.10.2026)

Question: does the s2 dominant (ANDN NAND NOT ORN, 194 steps/gestation) sit one mutation away from a fitter genotype
that gains a task, once its never-executed code drifts neutrally?

Method: fill_scan.py (design reviewed by Fable 25.10). Random fills of the 35 dead positions that are neutral for all
substitutions, input seed 7; every distinct one-step mutant (sub/ins/del) of every neutral fill run to CAP=1000 steps.
Lab job petri-fillscan-481b, seed 1: killed at the 2 h limit after 1276 of 1500 fills (5.5 s/fill, not 3.3).

Numbers (out/fill_scan_s1.jsonl):
- fills 1276, neutral 1254 (98.3%)
- one-step mutants scanned: 6,097,643 (4858-4864 per fill)
- mutants with AND: 43,910 (35-38 per fill, every fill)
- AND+ANDN: 8 mutants in 6 fills; of those dividing within CAP: 0
- task-gaining mutants that divide: 35,116 (28-30 per fill); of those fitter than the dominant: 0

Positive control (fill_control.py, out/fill_control_s1.jsonl): 8 random bases drawn from the 1476 one-step mutants of
the dominant that lose >=1 task and still divide. Scanner must find a fitter task-gainer one step away. Found in 8/8,
reversion to the dominant found in 8/8, including the 3 hardest bases (lost NAND only, relfit 0.50, 1-8 fitter gainers).
The control only exercises regaining tasks the dominant has; AND detection itself is exercised by the 43,910 AND rows.

Reading: 0 of 1254 neutral neighbourhoods holds a fitter task-gainer. Rule of three: the share of neutral fills with
one is below 3/1254 = 0.24% (95%), for this dominant, this fill sampler, seed 7 inputs, CAP 1000. One seed of fills.
Not shown: anything about two-step paths, other dominants, other input seeds, or births in a running world.

## Censoring (Fable review 25.10, blocking)
CAP=1000 only justifies AND. Dominant bonus is 7; a one-step gainer of OR beats it up to 1552 steps, NOR/XOR up to 3104,
EQU up to 6208. So the zero above holds only for mutants dividing within 1000 steps.
Probe (cap_probe.py, fills 0-1 of seed 1): ~2580 mutants per fill hit CAP 1000; re-run to 6300 steps, 5 per fill
divide, 0 gain a task. Lab job petri-capprobe-481 re-runs fills 0-399 the same way (out/cap_probe_s1.jsonl).
Public sentence until it finishes (Fable): "In 1254 neutral fills of the s2 dominant's dead code, none of 6.1 million
one-step mutants that divided within 1000 steps gained a task and beat the dominant (95% upper bound 0.24% of fills;
one dominant, one fill seed, input seed 7)."

## Censoring probe: result (lab job petri-capprobe-481, 25.10)
Killed at its 3 h limit after fills 0-317 of the 400 planned (seeded prefix, so the cut is independent of outcome).
out/cap_probe_s1.jsonl: 318 fills, 774,970 mutants hit CAP 1000 (2338-2659 per fill), re-run to 6,300 steps:
1,417 divide (1-7 per fill), 0 gain a task, 0 fitter. Break-even of a +5-bit gain with an insertion: 32*194*96/95 = 6,273.
Rule of three for gains up to 5 bits at copied length <= 96: below 3/318 = 0.94% of fills.

## Copied length (Fable review 25.10, blocking)
petri.py pays merit = min(ncopy, len(child)) * 2^bonus, and carve() allows a child up to 2x the parent. fill_scan.py and
cap_probe.py scored fitness with genome length, so a mutant that copies a longer child was under-scored.
copylen_probe.py scores by the merit actually paid at the first division (kid.merit / steps, dominant 12160/194).
Fills 0-11 (out/copylen_s1.jsonl, matches cap_probe counts per fill): 29,075 divide within 1000, 62 with a child longer
than the parent (max 126), 336 gain a task, 0 fitter; 29,277 capped, 44 divide by 6,300, 0 gain.
At the 2x limit (child 190) the +5-bit break-even is 32*194*190/95 = 12,416 steps: fills 0-317 re-run to 12,500 with true
merit (out/copylen12500_s1.jsonl; its "div6300"/"gain6300" columns mean 12,500 in that file).
