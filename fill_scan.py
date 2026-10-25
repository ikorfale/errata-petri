"""#481 barrier crossing, the neutral-network version (design reviewed by Fable 25.10): dead code drifts freely, so
sample random fills of the 50 never-executed positions of the s2 dominant, keep the fills that are neutral (same
tasks and same steps per gestation, input seed 7), and scan every one-step mutant (sub/ins/del) of each for task
gains. Fitness = copied length x 2^bonus / steps per gestation (petri.py divide()), relative to the dominant.
Reports per fill: neutral or not; mutants with AND, with AND+ANDN, AND+ANDN that divide within CAP steps, and of
those the ones fitter than the dominant, re-checked on input seeds 1-5. Positive control: any one-step mutant that
gains a task the dominant lacks and is fitter. Usage: python3 fill_scan.py NFILLS SEED > out/fill_scan.jsonl"""
import sys, json, random, string, time
sys.path.insert(0, ".")
from genome_trace import trace
from petri import parse, TASKS
BON = {n: b for n, _, b in TASKS}
D = json.load(open("out/s2_dump.json")); top = max(D["genotypes"], key=lambda g: g["n"])["genome"]
# Of the 50 never-executed positions (dead_region.txt) only 35 are neutral for all 25 substitutions: the others are
# read as nop modifiers or label templates (25.10 probe). Fills use the 35; 197/200 random fills stay neutral.
DEAD = list(range(13, 21)) + list(range(32, 59))
AL = string.ascii_lowercase; CAP = 1000          # AND (x4) lets a full-task genome take up to ~776 steps and still win


def run(g, seed=7):
    try: log, n = trace(parse(g), seed, 1, cap=CAP)
    except Exception: return (), CAP
    return (tuple(sorted(set().union(*[set(r[7]) for r in log]))) if log else ()), n


def fit(g, t, n):
    return len(g) * 2 ** sum(BON[x] for x in t) / n if n < CAP else 0.0


def neigh(g):
    for i in range(len(g) + 1):
        if i < len(g): yield g[:i] + g[i + 1:]
        for c in AL:
            yield g[:i] + c + g[i:]
            if i < len(g) and c != g[i]: yield g[:i] + c + g[i + 1:]


t0, n0 = run(top); F0 = fit(top, t0, n0)
nf, seed = int(sys.argv[1]), int(sys.argv[2]); rng = random.Random(seed)
print(json.dumps({"dominant": top, "tasks": t0, "steps": n0, "fit": F0, "cap": CAP, "seed": seed}), flush=True)
for k in range(nf):
    g = list(top)
    for i in DEAD: g[i] = rng.choice(AL)
    g = "".join(g); t, n = run(g)
    row = {"fill": k, "neutral": t == t0 and n == n0}
    if row["neutral"]:
        c = dict(mut=0, AND=0, AND_ANDN=0, AND_ANDN_div=0, gain_div=0, gain_fitter=0); hits = []; seen = set(); s = time.time()
        for x in neigh(g):
            if x in seen: continue
            seen.add(x); c["mut"] += 1
            tx, nx = run(x); fx = fit(x, tx, nx) / F0
            if set(tx) - set(t0) and nx < CAP: c["gain_div"] += 1
            if set(tx) - set(t0) and fx > 1: c["gain_fitter"] += 1
            if "AND" in tx:
                c["AND"] += 1
                if "ANDN" in tx:
                    c["AND_ANDN"] += 1
                    if nx < CAP:
                        c["AND_ANDN_div"] += 1
                        rs = [run(x, s2) for s2 in range(1, 6)]
                        hits.append({"g": x, "tasks": tx, "steps": nx, "relfit": round(fx, 3),
                                     "relfit_seeds": [round(fit(x, a, b) / F0, 3) for a, b in rs]})
        row.update(c, hits=hits, sec=round(time.time() - s, 1))
    print(json.dumps(row), flush=True)
