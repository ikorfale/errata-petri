# #481 evolution run as a lab job (PREREG-evo-and.md): 10 seeds x 40,000 updates from the s2 dominant monoculture.
import os, subprocess, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.exit(subprocess.call([sys.executable, "evo_and.py", "40000", ",".join(str(s) for s in range(101, 111))]))
