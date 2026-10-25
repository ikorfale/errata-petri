# #481 Fable 25.10: re-score all 1276 fills of seed 1 at CAP 1000 with the merit actually paid (copied length)
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, "copylen_probe.py", "1276", "1", "1000"], stdout=open("out/copylen1000_s1.jsonl", "w")))
