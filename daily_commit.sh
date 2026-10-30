#!/bin/bash
# Commit and push the day's public outputs after daily.py + revisions.py (day 2 sat uncommitted for a day, 30.10).
set -u; cd "$(dirname "$0")"
git add daily/day-*.json daily/post-*.md daily/snap/*.canon.json.gz daily/lineage.jsonl daily/revisions.jsonl \
        daily/series.jsonl daily/state.json 2>/dev/null
git diff --cached --quiet && exit 0
if git diff --cached | grep -q '/home/'; then echo "daily_commit: /home/ path in staged diff, not committing"; git reset -q; exit 1; fi
d=$(ls daily/post-*.md | sort | tail -1 | grep -o '[0-9]\+')
git commit -qm "Petri daily: day $((10#$d)) outputs (post, summary, canonical snapshot, lineage)" && git push -q
