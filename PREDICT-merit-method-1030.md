# Does Petri's merit rule pay for unexecuted instructions? Predictions (30.10, before any arm ran)

Background: petri.py:326 gives a child merit = copied size (like Avida's BASE_MERIT_METHOD 1). On day 2 about a quarter of
each dominant genome never runs in a gestation, and the 1-3% edge of length 90 over 89 came from ~1.5 extra unexecuted
instructions (VERDICT-swaps-1030.md). Avida's default (method 4) pays min(executed, copied).

Design (merit_method.py): start from the saved end of day 1 (update 40,000, 837 organisms), reseed the world RNG with
11, 12, 13; for each seed run method 1 and method 4 for 40,000 updates. Not the long world. "Executed" = distinct
positions inside the parent genome visited by the IP during the gestation. Check done before launch: the patched engine
with method 1 ends on the same digest as the unpatched engine after 300 updates (f4faf5d17f200645). Smoke run, 1000
updates, seed 11: unexecuted fraction of births 0.261 (method 1) vs 0.252 (method 4); I have seen nothing else.

Outcome: U = mean unexecuted fraction over births in the last five 1000-update rows (+36k..+40k); G = mean genome length
at +40k.

- P1: U lower under method 4 than method 1 in all 3 seed pairs.
- P2: pooled over seeds, U(method 1) - U(method 4) >= 0.05.
- P3: G lower under method 4 in at least 2 of 3 pairs.

If P1 fails in any pair, I write: over 40k updates in this world the rule does not measurably pay for unexecuted code.
Limits: 3 seeds, one starting world, one mutation regime; executed set counts positions, not instruction executions.
