"""record_timelapse.py — frames of one reference world (v0.2 rules, seed 1) for the lab.errata.page player.
Each frame: per cell a task mask (tasks its parent computed, which earned its merit, or tasks it has computed itself),
a lineage hue byte (md5 of the first 12 instructions) and genome length. Writes out/timelapse_s1.json.
Usage: python3 record_timelapse.py [UPDATES] [EVERY]"""
import json, sys, base64, hashlib, time
import petri
from petri import World, ANCESTOR, TASKS, show

NAMES = [t[0] for t in TASKS]


class Rec(World):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.inh = {}                       # id(org) -> task mask it was born with

    def divide(self, o, c):
        mask = sum(1 << i for i, n in enumerate(NAMES) if n in o.tasks)
        before = self.births
        cells_before = None
        if True:
            cut = self.carve(o)
            if cut is None:
                o.heads[petri.IP] = (o.heads[petri.IP] + 1) % len(o.mem)
                return
            child, parent = cut
            bonus = float(min(o.ncopy, len(child)))
            for name, _, b in TASKS:
                if name in o.tasks:
                    bonus *= 2 ** b
            for name in o.tasks:
                self.task_births[name] += 1
            kid = petri.Org(child, o.lineage, merit=bonus, born=self.update)
            self.cells[self.neighbour(c)] = kid
            self.births += 1
            self.restart(o, parent, bonus)
            self.inh[id(kid)] = mask
            self.inh[id(o)] = mask


def frame(w):
    tm, hue, ln = bytearray(), bytearray(), bytearray()
    for o in w.cells:
        if o is None:
            tm += b'\xff\xff'; hue.append(0); ln.append(0); continue
        m = w.inh.get(id(o), 0) | sum(1 << i for i, n in enumerate(NAMES) if n in o.tasks)
        tm += m.to_bytes(2, 'little')
        g = show(o.mem[:o.glen])
        hue.append(int(hashlib.md5(g[:12].encode()).hexdigest()[:2], 16))
        ln.append(min(o.glen, 255))
    return {'u': w.update, 't': base64.b64encode(bytes(tm)).decode(), 'h': base64.b64encode(bytes(hue)).decode(),
            'l': base64.b64encode(bytes(ln)).decode()}


if __name__ == '__main__':
    ups = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    every = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    w = Rec(seed=1); w.inject(ANCESTOR, 'ancestor')
    frames, counts, t0 = [frame(w)], [], time.time()
    for u in range(ups):
        w.run_update()
        if w.update % every == 0:
            live = {id(o) for o in w.cells if o is not None}
            w.inh = {k: v for k, v in w.inh.items() if k in live}
            frames.append(frame(w))
            c = w.census()
            counts.append({'u': w.update, 'pop': c['pop'], 'gen': c['genotypes'], 'tasks': c['tasks_now']})
            if w.update % 3000 == 0:
                print(w.update, round(time.time() - t0), c['tasks_now'], flush=True)
    json.dump({'side': w.side, 'seed': 1, 'every': every, 'tasks': NAMES, 'frames': frames, 'counts': counts},
              open('out/timelapse_s1.json', 'w'), separators=(',', ':'))
    print('done', len(frames), 'frames', round(time.time() - t0), 's')
