# #481 neutral-fill scan as a lab job: 1500 fills, seed 1 (~3.3 s per fill)
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, "fill_scan.py", "1500", "1"], stdout=open("out/fill_scan_s1.jsonl", "w")))
