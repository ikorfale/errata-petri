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
