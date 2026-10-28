# E3 result: do parasite steps age the host? (PREREG-E3.md, frozen; verdict by e3_verdict.py)

Run 27.10 as lab jobs petri-e3a/e3b; read 27.10 ~19:30Z. 196 worlds of 196; the local anchor equals E2 world for world
(42 of 42), so the verdict stands. Full output: out/e3_verdict.txt.

| age mode | L50 (point) | seed-cluster bootstrap 95% | shift vs E1 26.88 |
|---|---|---|---|
| local (instr, anchor) | 26.85 | 25.33-28.27 | - |
| host (only the host's own steps age it) | 29.57 | 28.68-30.37 | straddles +3 |
| updates (slice per update lived) | 27.73 | 26.35-28.75 | < 3 |

- **H1 (parasite steps age the host): undecided.** The host-mode interval straddles 29.88. Point estimate: host mode
  reproduces 0.58 of the no-age shift (E2: 31.52). My prior was ~55% for "supported"; the data neither support nor reject it.
- **H2 (updates-age is equivalent for this question): holds.** The updates-mode interval lies wholly below 29.88.
- Not tested (descriptive): share of parasites lost to their host's old age falls from 17.5% (local) to 4.5% (host mode).

## Note 2026-10-28 (canary run of the blocking-only prompt, lab/canary/RESULT.md)
The frozen PREREG-E3.md has two text flaws its 27.10 review (NONE, run with the code attached) did not list:
"Shift vs 26.88" is E1's reference L50 (named only in e3_verdict.py), while the section above quotes E2's local 26.85;
and "before any E3 world ran" sits next to the seed-1 L=24 anchor, a preregistered world that had run. Neither changes
the verdict: the host interval 28.68-30.37 straddles both 29.85 and 29.88, and the anchor is deterministic (42/42 match E2).
