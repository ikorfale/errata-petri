"""Plan #436 follow-up: does resetting a parasite after a failed inject (World.reset_failed_inject) turn the seeded
20-long parasite from near-critical into an established one? Paired: one warm world per seed (2000 updates, the
same 9 hosts seeded), copied, then run AFTER updates with the reset off and on. Usage: python3 fix_trial.py AFTER SEED..."""
import copy, json, sys
from petri import World, ANCESTOR, Org, CODE
def make_parasite(pad=4):
    g = list(ANCESTOR); i = g.index(CODE["h-divide"])
    g[i:i + 1] = [CODE["inject"], CODE["nop-B"]]
    return g[:6] + g[6 + 85 - pad:] if pad < 85 else g
after = int(sys.argv[1])
ARMS = [False, True, "heads"]   # off, full reset, heads-only reset (zenith 98438)
for seed in map(int, sys.argv[2:]):
    w = World(seed=seed, parasites=True); w.inject(ANCESTOR, "ancestor")
    for _ in range(2000): w.run_update()
    hosts = [o for o in w.cells if o is not None and o.para is None]; w.rng.shuffle(hosts)
    for h in hosts[:9]:
        p = Org(make_parasite(), "seeded-parasite", merit=0.0, born=w.update); p.is_para = True; h.para = p
    for reset in ARMS:
        v = copy.deepcopy(w); v.reset_failed_inject = reset; inj0 = v.injections; traj = []
        for u in range(after):
            v.run_update()
            if (u + 1) % 100 == 0: traj.append(sum(o is not None and o.para is not None for o in v.cells))
        print(json.dumps({"seed": seed, "reset": reset, "infected_end": traj[-1], "peak": max(traj),
                          "extinct_at": next((2000 + 100 * (i + 1) for i, x in enumerate(traj) if x == 0), None),
                          "injections": v.injections - inj0, "traj": traj}), flush=True)
