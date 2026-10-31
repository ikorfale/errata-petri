"""Queue wrapper (the lab queue passes no arguments): runs lockfwd.py b 41 42 43 44 45 46 47 48."""
import os, runpy, sys
sys.argv = ['lockfwd.py', 'b', '41', '42', '43', '44', '45', '46', '47', '48']
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lockfwd.py"), run_name="__main__")
