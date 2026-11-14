# Petri daily: what is known about days 5-17 (no revisions row)

source: out/daily.log (stdout/stderr of each run, appended at run time), systemd user journal, dpkg log.
NOT recorded by revisions.py. No revisions.jsonl rows are written for these days, now or later.

## Cause
Commit e3dc123 (2026-10-31 09:38 UTC) changed daily.py (runner sha16 e0fe1a22d813a9d8 -> 58c3577b844ce13b)
and added an end-of-run step that reads `os.path.join(D, "daily", "state.json")` while D is already `daily/`.
Day 4 ran at 03:20 on 31 Oct, before that commit, so it did not crash. Every run from day 5 (1 Nov) to day 18
(14 Nov) wrote its state and post, then raised FileNotFoundError on that line (daily.py:244); systemd marked
it failed, so ExecStartPost (revisions.py, daily_commit.sh) never ran. Fixed in ae3465e (runner bb915bc09d94fdb4).
git log -- daily.py has no commit between e3dc123 and ae3465e, so days 5-18 ran runner 58c3577b844ce13b
(inference from git; the day-18 row recorded it before the fix).

## Per day, from the run's own log
| day | date | state digest | previous | engine | crashed at line 244 |
|---|---|---|---|---|---|
| 5 | 2026-11-01 | 0e5db2359b14d066 | a0342428b6f6cf6a | 4b1613c9cc004946 | yes |
| 6 | 2026-11-02 | 4c8795e479d2b927 | 0e5db2359b14d066 | 4b1613c9cc004946 | yes |
| 7 | 2026-11-03 | e5d3c7c10b087089 | 4c8795e479d2b927 | 4b1613c9cc004946 | yes |
| 8 | 2026-11-04 | b17d8a24a246b781 | e5d3c7c10b087089 | 4b1613c9cc004946 | yes |
| 9 | 2026-11-05 | 76bb26d591697983 | b17d8a24a246b781 | 4b1613c9cc004946 | yes |
| 10 | 2026-11-06 | 162120fbc0fc737a | 76bb26d591697983 | 4b1613c9cc004946 | yes |
| 11 | 2026-11-07 | 9dbdcec5f47ea255 | 162120fbc0fc737a | 4b1613c9cc004946 | yes |
| 12 | 2026-11-08 | 78a73f7f76dfe775 | 9dbdcec5f47ea255 | 4b1613c9cc004946 | yes |
| 13 | 2026-11-09 | cd4c27067dc5cd7b | 78a73f7f76dfe775 | 4b1613c9cc004946 | yes |
| 14 | 2026-11-10 | 502653baaaabcd21 | cd4c27067dc5cd7b | 4b1613c9cc004946 | yes |
| 15 | 2026-11-11 | 224c339a42a8cf5f | 502653baaaabcd21 | 4b1613c9cc004946 | yes |
| 16 | 2026-11-12 | dd9ed6913c8a7001 | 224c339a42a8cf5f | 4b1613c9cc004946 | yes |
| 17 | 2026-11-13 | f66c8c1d736d2921 | dd9ed6913c8a7001 | 4b1613c9cc004946 | yes |
| 18 | 2026-11-14 | 23e5798df91959e6 | f66c8c1d736d2921 | 4b1613c9cc004946 | yes |

Each day's `previous` equals the day before's `state digest`: the chain is unbroken.

## What the other logs say
- systemd journal (available from 6 Nov, days 10-18): every run started 03:20:17 UTC and exited status=1/FAILURE
  between 03:47:51 and 03:48:33. Earlier journal entries (days 5-9) are not available.
- package log: no change to python3.14 (3.14.4-1ubuntu0.2) from 5 Nov 10:34 UTC onwards.
  For 1-5 Nov no package log is available, so an interpreter change on those days can be neither shown nor excluded
  by logs; python_sha16 is equal on day 4 and day 18 (52e0a13e60a981d8).
- modules_sha16 for days 5-17: unknown (nothing recorded).

