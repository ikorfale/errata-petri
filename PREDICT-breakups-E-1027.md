# Prediction before any --e run of breakups.py (#537), 2026-10-27 ~21:50 UTC

Setting: E1-E3 warm worlds (side 30, parasites on, inject never drawn), indel 0.05 for updates 1-2000, then indel 0
(the arms' setting, no parasite seeded here). Seeds 1, 2, 3; 3000 updates. Smoke run only: seed 99, 250 updates.

- Warm phase (updates 1-2000): breakup share of births 1.0-2.0% per seed, like plain ancestor worlds (1.37-1.49%).
- Indel-0 phase (2001-3000): within +-0.5 points of the same seed's share over updates 1501-2000, because a breakup
  depends on the genome (heritable) and indel 0 freezes lengths, so the mix does not move much in 1000 updates.
- If the indel-0 share falls below half of the warm share, my "heritable" reading is wrong.
