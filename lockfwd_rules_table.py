"""Report-only (zenith-claude #109783): per seed of the lock-in forward test, what each rule said at 50k and who won.
Lock rule = A1 (locked before 50k at modal length >= 95 -> long). Current-length rule = median length at 50k >= 95 -> long.
Net change = end median at 80k minus median at 50k. Reads the same out/lockfwd_<seed>_{a,b}.json as lockfwd_verdict.py."""
import json
from lockfwd_verdict_lock import lock
print("seed | lock at 50k | med 50k | end 80k | net | lock rule | length rule | outcome | where they differ")
dis = []; nets = []
for s in range(33, 49):
    a = json.load(open(f"out/lockfwd_{s}_a.json"))["rows"]; b = json.load(open(f"out/lockfwd_{s}_b.json"))["rows"]
    u, L = lock(a); m50 = a[-1]["glen_med"]; end = b[-1]["glen_med"]
    pl = "L" if (u is not None and L >= 95) else "S"; pm = "L" if m50 >= 95 else "S"; o = "L" if end >= 95 else "S"
    diff = ""
    if pl != pm: diff = "lock wins" if pl == o else "length wins"; dis.append(diff)
    nets.append(end - m50)
    print(f"{s} | {L if u is not None else 'none'} | {m50} | {end} | {end - m50:+g} | {pl} | {pm} | {o} | {diff}")
print(f"seeds where the rules differ: {len(dis)}; lock wins {dis.count('lock wins')}, length wins {dis.count('length wins')}")
print(f"net change 50k->80k: down {sum(n < 0 for n in nets)}, zero {sum(n == 0 for n in nets)}, up {sum(n > 0 for n in nets)} of {len(nets)}")
