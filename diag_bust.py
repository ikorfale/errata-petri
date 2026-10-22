"""Plan #436: why does the seeded 20-long parasite boom and crash in seeds 2 and 3 but persist in seed 1?
Reruns pilot_seeded.py's setup (WARM 2000, K 9, PAD 4) and logs every 50 updates: inject attempts by parasite
threads by outcome, how parasites were lost (host died of age / host cell overwritten), the parasite genome census,
and host susceptibility (hosts holding the complement of the parasite's label). Usage: python3 diag_bust.py SEED [AFTER]"""
import json, sys
from collections import Counter
import petri
from petri import World, ANCESTOR, Org, show, COMP, CODE
def make_parasite(pad):
    g = list(ANCESTOR); i = g.index(CODE["h-divide"])     # same as pilot_seeded.make_parasite (that module exits on import)
    g[i:i + 1] = [CODE["inject"], CODE["nop-B"]]
    return g[:6] + g[6 + 85 - pad:] if pad < 85 else g
seed = int(sys.argv[1]); after = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
PAR = make_parasite(4)
KEY = bytes([COMP[CODE["nop-B"]]])
class W(World):
    def __init__(s, *a, **k):
        super().__init__(*a, **k); s.why = Counter()
    def inject_para(s, o, c, ip):
        lab = s.label(o.mem, ip + 1); cut = s.carve(o)
        if not o.is_para: why = 'host-thread'
        elif not lab: why = 'no-label'
        elif cut is None: why = 'carve-failed'
        else:
            host = s.cells[s.neighbour(c)]
            why = ('empty' if host is None else 'host-infected' if host.para is not None else
                   'no-complement' if bytes(COMP[x] for x in lab) not in bytes(host.mem[:host.glen]) else 'ok')
        s.why[why] += 1
        return World.inject_para(s, o, c, ip) if why in ('ok', 'host-thread') else False
w = W(seed=seed, parasites=True); w.inject(ANCESTOR, "ancestor")
for _ in range(2000): w.run_update()
hosts = [o for o in w.cells if o is not None and o.para is None]; w.rng.shuffle(hosts)
for h in hosts[:9]:
    p = Org(PAR, "seeded-parasite", merit=0.0, born=w.update); p.is_para = True; h.para = p
def snap():
    return {id(o.para): (c, o) for c, o in enumerate(w.cells) if o is not None and o.para is not None}
prev = snap(); lost = Counter()
for u in range(after):
    w.run_update()
    cur = snap()
    for pid, (c, o) in prev.items():
        if pid not in cur:
            lost['host-gone' if w.cells[c] is None else 'host-overwritten' if w.cells[c] is not o else 'para-cleared'] += 1
    prev = cur
    if (u + 1) % 50 == 0:
        live = [o for o in w.cells if o is not None]; paras = [o.para for o in live if o.para is not None]
        gen = Counter(show(p.mem[:p.glen]) for p in paras)
        print(json.dumps({"update": w.update, "pop": len(live), "infected": len(paras),
              "susceptible": round(sum(KEY in bytes(o.mem[:o.glen]) for o in live) / max(1, len(live)), 3),
              "para_len": Counter(p.glen for p in paras).most_common(3),
              "para_mem_doubled": sum(len(p.mem) > p.glen for p in paras),
              "top": gen.most_common(3), "attempts": dict(w.why), "lost": dict(lost)}), flush=True)
        w.why.clear(); lost.clear()
