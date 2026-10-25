# #481 Fable 25.10: censored mutants (CAP 1000) re-run to 6300 steps on the first 400 fills of seed 1 (~20 s per fill)
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, "cap_probe.py", "400", "1"], stdout=open("out/cap_probe_s1.jsonl", "w")))
