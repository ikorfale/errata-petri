"""#541 (zenith 105772): E3 rerun with breakup counting per arm, optionally under a strict division rule.
Same worlds as e3_sweep.py (counting draws no random numbers, so the default run must reproduce out/e3_*.jsonl world
for world). --strict: a host division where the parent would keep < 75% of its genome fails (as a failed h-divide:
IP+1, keep running), in the warm-up too. Injections are unchanged. Breakup = a host birth after which the parent keeps
< 75% of its genome (breakups.py). Usage: python3 e3_brk.py UPD SEEDS ARMS [--strict]
--- e3_sweep.py docstring ---
E3 (PREREG-E3.md): E2 sweep plus two age modes: host (age counts only the host's own steps) and updates (age in updates vs 20 x glen / slice).
The rest is e2_sweep.py unchanged.
"""
"""E2: E1's sweep with one switch per arm (PREREG-E2.md): MODE local (E1 control, now with failure logging),
global (a parasite's copy lands in a uniformly random cell: no crowding) or noage (hosts never die of old age).
Usage: python3 e2_sweep.py UPD SEED[,SEED..] MODE:L[,L..][;MODE:L..]
--- E1 docstring ---
E1 (plan #421): parasite length sweep, preregistered in PREREG-E1.md before any run of this script.
One warm world per seed (2000 updates; h = births per occupied cell-update over updates 1500-2000; parasites on but mutation never draws inject: w.nops = len(OPS) - 1),
the same 9 hosts get the parasite of length L in every arm (deep copy of the warm world), then UPD updates with indel 0 (no length evolution; copy mutation stays on).
Census every 250 updates: infected cells, population, parasite lengths, hosts holding the complement of nop-B.
Usage: python3 e1_sweep.py UPD SEED[,SEED..] L[,L..]   (L = 16 + pad; L=101 is the uncut ancestor)"""
import copy, json, sys, time
from collections import Counter
from petri import World, ANCESTOR, Org, CODE, COMP, OPS, show, RH, IP
STRICT = "--strict" in sys.argv; sys.argv = [a for a in sys.argv if a != "--strict"]
_orig_div = World.divide
def _divide(self, o, c):
    if STRICT:
        rh = o.heads[RH] or len(o.mem)
        if rh < 0.75 * o.glen:
            o.heads[IP] = (o.heads[IP] + 1) % len(o.mem); return
    g0, b = o.glen, self.births; _orig_div(self, o, c)
    if self.births > b:
        self.brk[0] += 1
        if o.glen < 0.75 * g0: self.brk[1] += 1
World.divide = _divide

def make_parasite(L):
    pad = L - 16
    g = list(ANCESTOR); i = g.index(CODE["h-divide"])
    g[i:i + 1] = [CODE["inject"], CODE["nop-B"]]
    return g[:6] + g[6 + 85 - pad:] if pad < 85 else g

KEY = bytes([COMP[CODE["nop-B"]]])
upd = int(sys.argv[1]); seeds = [int(x) for x in sys.argv[2].split(",")]; arms = [(m, int(L)) for part in sys.argv[3].split(";") for m, ls in [part.split(":")] for L in ls.split(",")]
assert all(m in ("local", "global", "noage", "host", "updates") for m, _ in arms), arms
for seed in seeds:
    w = World(seed=seed, parasites=True); w.nops = len(OPS) - 1; w.brk = [0, 0]
    w.inject(ANCESTOR, "ancestor")
    for _ in range(1500): w.run_update()
    b0 = w.births; occ = 0
    for _ in range(500):
        w.run_update(); occ += sum(o is not None for o in w.cells)
    live = [o for o in w.cells if o is not None]; merits = sorted(o.merit for o in live)
    warm = {"seed": seed, "h_occupied": round((w.births - b0) / occ, 5), "h_cell": round((w.births - b0) / 500 / len(w.cells), 5),
            "merit_median_over_mean": round(merits[len(merits) // 2] / (sum(merits) / len(merits)), 4),
            "host_len_median": sorted(o.glen for o in live)[len(live) // 2], "brk_warm": list(w.brk), "strict": STRICT}
    print(json.dumps({"warm": warm}), flush=True)
    hosts = [c for c, o in enumerate(w.cells) if o is not None and o.para is None]; w.rng.shuffle(hosts)
    for mode, L in arms:
        v = copy.deepcopy(w); v.indel = 0.0; v.para_global = mode == "global"; v.age_limit = mode != "noage"; v.age_mode = {"host": "host", "updates": "updates"}.get(mode, "instr"); v.brk = [0, 0]
        from collections import Counter as _C; v.inj_fail, v.para_lost = _C(), _C(); b0, occ = v.births, 0
        t = time.process_time(); par = make_parasite(L)
        assert len(par) == L, (L, len(par))
        for c in hosts[:9]:
            p = Org(par, "seeded-parasite", merit=0.0, born=v.update); p.is_para = True; v.cells[c].para = p
        inj0, sec0 = v.injections, v.secondary; rows = []
        for u in range(upd):
            v.run_update(); occ += sum(o is not None for o in v.cells)
            if (u + 1) % 250 == 0:
                live = [o for o in v.cells if o is not None]; paras = [o.para for o in live if o.para is not None]
                lc = Counter(p.glen for p in paras)
                rows.append({"u": v.update, "pop": len(live), "inf": len(paras),
                             "plen_med": sorted(p.glen for p in paras)[len(paras) // 2] if paras else None,
                             "plen_top": lc.most_common(3),
                             "susc": round(sum(KEY in bytes(o.mem[:o.glen]) for o in live) / max(len(live), 1), 4)})
                if not paras:
                    break                   # extinct: no thread can come back (inject is never drawn)
        end = Counter(show(o.para.mem[:o.para.glen]) for o in v.cells if o is not None and o.para is not None)
        print(json.dumps({"seed": seed, "mode": mode, "L": L, "upd": upd, "h_arm": round((v.births - b0) / max(occ, 1), 5),
                          "inj_fail": dict(v.inj_fail), "para_lost": dict(v.para_lost), "end_genomes": end.most_common(5), "injections": v.injections - inj0,
                          "secondary": v.secondary - sec0, "brk": list(v.brk), "strict": STRICT, "cpu_s": round(time.process_time() - t, 1), "census": rows}), flush=True)
