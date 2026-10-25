#!/bin/bash
# #481 neutral-fill scan, 1500 fills, seed 1 (~3.3 s per fill)
cd "$(dirname "$0")" && python3 fill_scan.py 1500 1 > out/fill_scan_s1.jsonl
