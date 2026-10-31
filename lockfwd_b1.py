"""Queue wrapper (the lab queue passes no arguments): runs lockfwd.py b 33 34 35 36 37 38 39 40."""
import os, runpy, sys
sys.argv = ['lockfwd.py', 'b', '33', '34', '35', '36', '37', '38', '39', '40']
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lockfwd.py"), run_name="__main__")
