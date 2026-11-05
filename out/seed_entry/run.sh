#!/bin/bash
cd "$(dirname "$0")/../.." || exit 1
python3 seed_entry.py out/seed_entry/world-day009.pkl 120000 1,2,3,4,5,6,7,8,9,10,11,12 ANC-len,DOM-len,ANC-mean,DOM-mean 4
python3 seed_entry_verdict.py > out/seed_entry/verdict.txt 2>&1 || true
