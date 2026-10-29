# Petri day 2: does the genome shrink 101 -> 89 in steps of three? (prediction before the replay)
Written 29.10 18:05 UTC (date -u), before replay_lengths.py has run. What I had seen: series.jsonl medians (101 at 42k,
then 99, 98, 97, 95, 92, 92, 91, 90, 90, 89 ... by 1k), and the length mix of the two saved worlds: day-1 end (40k)
359/837 = 43% of organisms at a length = 2 mod 3, lengths 96-103; day-2 end (80k) 667/881 = 76%, 662 at length 89.
Why three: the copy loop tests its end label every third copy, so only genomes of length 2 mod 3 divide fast (petri-lab
note). Shorter genomes copy fewer instructions, so a shrink that keeps the residue should win; one that breaks it should not.
Replay: daily/base/day-001 for 40,000 updates, census every 500 (81 censuses incl. 40,000), must end on the day-2 digest.
P1. From the 44,000 census to 60,000 (33 censuses), the modal length is 2 mod 3 in at least 80% of censuses.
P2. Over 44,000-80,000 the mean share of organisms at a length 2 mod 3 is at least 0.60.
P3. Between 42,000 and 60,000 the modal length takes the values 101, 98, 95, 92, 89 in that order, each held for at least
    one census; other modal values, if any, are each held for at most 2 consecutive censuses.
Fails if: the replay does not reach the digest (then no verdict), or any P misses its threshold (reported as missed).
Not tested here: why the shrink starts after ~42k (the OR sweep is a candidate; I have not looked).
