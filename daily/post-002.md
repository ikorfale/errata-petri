Petri daily, day 2: updates 40,000 to 80,000 of one world that never restarts.

- engine changed since the last day (f3adc8decfa991a0 -> 4b1613c9cc004946)
- median genome length 101 -> 89

End of day: 881 organisms, 610 genotypes, median genome 89 instructions. Tasks performed now (organisms): NOT 581, NAND 642, AND 469, ORN 702, OR 537, ANDN 699, NOR 462.
Tasks ever performed, with first update: NOT 1,500, NAND 2,000, AND 2,000, ORN 2,000, OR 2,000, ANDN 2,000, NOR 5,500.
Dominant genome (89): wtyjagcycuuyuwsmbyffrjyuyxuycpntcmksdqyuehjuyycucnpdevjcuoucycuycucucpuyzmwftpzvvfcxglmua

Lineage (a performer descends from a performer at the previous census, or opens a new clade): NOT 802 new clades, largest 672, 6 of 78 censuses with no continuing performer; NAND 1199 new clades, largest 711, 24 of 78 censuses with no continuing performer; AND 605 new clades, largest 623, 0 of 78 censuses with no continuing performer; ORN 271 new clades, largest 749, 0 of 78 censuses with no continuing performer; OR 465 new clades, largest 671, 40 of 75 censuses with no continuing performer; ANDN 263 new clades, largest 740, 0 of 78 censuses with no continuing performer; NOR 663 new clades, largest 605, 0 of 78 censuses with no continuing performer.
New clades by counting rule (carry 1 / carry 1 merged / unlimited carry merged / plus shared ancestor within 4 censuses): NOT 802 / 121 / 0 / 0; NAND 1199 / 318 / 0 / 0; AND 605 / 37 / 0 / 0; ORN 271 / 11 / 0 / 0; OR 465 / 127 / 120 / 53; ANDN 263 / 11 / 0 / 0; NOR 663 / 39 / 0 / 0.
Baseline for the last rule: share of random pairs of live organisms whose ancestries meet within 4 censuses, median over the day: 0.247 (per census and per depth in lineage.jsonl). Censuses with this share >= 0.5 (a sweep in the window; the last rule merges everything there): 12, at updates 57,500, 58,000, 58,500, 63,000, 63,500, 64,000, 66,500, 67,000, 67,500, 75,500, 76,000, 76,500.

Continuity: state digest e3388c8a3cfce9fb (previous 141ea0cf00142dd9), engine 4b1613c9cc004946. Reads of the lineage fields anc/ptasks by the engine outside divide: 0 (all sites in day-002.json). Rules: tagged inputs, no parasites. Code: https://github.com/ikorfale/errata-petri (daily.py)
