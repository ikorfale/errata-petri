"""Where the 0 mod 3 deletion variants cut themselves: heads (RH, WH), copies done and parent/child lengths at the
h-divide that succeeds, mutation off. Usage: python3 delete_kids_heads.py -> out/delete_kids_heads.txt"""
from petri import World, parse
import fertility_probe as fp
g0 = parse(fp.DUAL); out = []
for i in [None] + list(range(len(g0))):
    g = g0 if i is None else g0[:i] + g0[i + 1:]
    w = World(side=5, seed=1, copy_mut=0.0, indel=0.0); w.inject(list(g), "t", cell=0); o = w.cells[0]; info = []
    _div = w.divide
    def d(o2, c, _div=_div): info.append((o2.heads[1], o2.heads[2], o2.ncopy)); _div(o2, c)
    w.divide = d
    for n in range(fp.CAP):
        b = w.births; w.step(o, 0)
        if w.cells[0] is not o: break
        if w.births > b:
            rh, wh, nc = info[-1]; wh = wh or 2 * len(g)
            out.append(f"{'dual' if i is None else 'del ' + str(i)}: step {n + 1}, h-divide calls {len(info)}, RH {rh} WH {wh}, "
                       f"copied {nc}, parent keeps {len(o.mem)} of {len(g)}, child {wh - rh}")
            break
print("\n".join(out)); open("out/delete_kids_heads.txt", "w").write("\n".join(out) + "\n")
