"""Fable's positive control for the AND ablation (23.10): the no-bonus control genome (top epoch-1 incumbent) dropped the
same way, but its probe lineage gets a synthetic x4 merit at every division (the size of v1's AND bonus, 2^2).
If x4 alone rescues it toward v1's 14/20, the result says 'v1 needs x4 merit to outrun residents', and the AND bonus is
one way to get it. Usage: inc_x4.py RNGSEED [UPDATES] [FACTOR]"""
import json, pickle, random, sys
from petri import parse
INC = json.load(open('out/epoch1_incumbents.json'))['top'][0]['genome']
rs = int(sys.argv[1]); UPS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
w = pickle.load(open('out/epoch1_world.pkl', 'rb')); w.rng = random.Random(rs)
from petri import Org, TASKS, IP
F = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0     # F=1 must reproduce epoch_probe20 inc0 exactly (no-op check)
def divide(self, o, c):                                  # petri.World.divide with one change: probe merit x F
    cut = self.carve(o)
    if cut is None:
        o.heads[IP] = (o.heads[IP] + 1) % len(o.mem); return
    child, parent = cut
    bonus = float(min(o.ncopy, len(child)))
    for name, _, b in TASKS:
        if name in o.tasks: bonus *= 2 ** b
    if o.lineage == 'probe': bonus *= F
    for name in o.tasks: self.task_births[name] += 1
    kid = Org(child, o.lineage, merit=bonus, born=self.update)
    self.cells[self.neighbour(c)] = kid; self.births += 1
    self.restart(o, parent, bonus)
w.divide = divide.__get__(w)
w.inject(parse(INC), 'probe')
for u in range(1, UPS + 1):
    w.run_update()
    if u in (100, 250, 500, 1000, UPS):
        live = [o for o in w.cells if o is not None]; n = sum(o.lineage == 'probe' for o in live)
        print(json.dumps({"arm": f"inc0-x{F:g}", "rs": rs, "after": u, "probe": n, "pop": len(live)}), flush=True)
        if n == 0: break
