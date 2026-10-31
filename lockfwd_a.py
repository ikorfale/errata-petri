"""Queue wrapper (the lab queue passes no arguments): runs lockfwd.py a."""
import os, runpy, sys
sys.argv = ['lockfwd.py', 'a']
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lockfwd.py"), run_name="__main__")
