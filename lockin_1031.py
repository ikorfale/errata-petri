"""Lab job for PREDICT-lockin-1031.md: shrink_carrier.py on 8 more method-1 day-2 replays (seeds below)."""
import runpy, sys, os
sys.argv = ["shrink_carrier.py", "12", "15", "17", "29", "13", "19", "20", "18"]
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shrink_carrier.py"), run_name="__main__")
