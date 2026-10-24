**Bottom line:** your tautology worry is right, a static predictor is feasible only for a restricted loop class and must abstain outside it, and the test worth running predicts exactness and the lap together from the genome text, with the "never divides" and the p=5 "j=7 or 9" cells as the risky predictions.

**(1) Tautology.** Yes, in two layers. Given the trace of `if-label` executions, the division lap is literally the last entry divided by L. The content you add is only that the label passes at every lap boundary, which is guaranteed by the exact-copy conditioning: with copy_mut 0 and RH starting at 0, the n-th copied letter is genome[n mod L] (`petri.py:137-145`), so the pass test at `petri.py:152` depends only on the genome tail at every multiple of L. Parity is a theorem of `carve` (`petri.py:266-270`) given RH=0 and WH=L at the first copy, not an observation. The "mod 3" rule is then a lossy summary of the check schedule: it equals the tautology exactly when checks form one arithmetic progression of period 3 starting at the first check. The 242 fits measure how often that structural assumption holds in the file. The 8 misses are precisely where it fails (period 1, or an irregular gap). The honest statement is "242 of 250 copy loops in this file check every third copy", which is a claim about loop structure, testable by reading p from the trace, not via j.

**(2) Static predictor.** Fully general is infeasible: control flow can depend on registers (`if-n-equ`, `if-less`, `jmp-head`, `set-flow`, lines 159-175), on IO randomness feeding those registers, on `h-search` scanning the child half whose content changes with ncopy (`petri.py:233` searches the doubled memory), and on labels or nop modifiers read past position L into the zero-filled child half (`petri.py:129, 149, 248`). Restricted to loops closed only by `mov-head` to a statically resolvable flow head, it is a cycle detection over (ip, FH, RH, WH, alloc) with if-label modelled as failing, which is path-neutral whenever the instruction after the label is `h-divide` (fail lands at ip+k+2; pass plus failed carve lands at `petri.py:321`, the same spot). Then enumerate the check schedule arithmetically. Untested draft, hand-traced on the ancestor to ("exact", 1):

```python
# static_lap.py: predict the division outcome from the genome text, without stepping it
from petri import NOP, COMP, CODE
HCOPY, IFLAB, MOVH, HSRCH, HALLOC, HDIV = (CODE[n] for n in
    ("h-copy", "if-label", "mov-head", "h-search", "h-alloc", "h-divide"))
DATA_JUMPS = {CODE[n] for n in ("if-n-equ", "if-less", "jmp-head", "set-flow")}

def label(g, s):                       # petri.label (244-250); edge=True if the read would enter the child half
    out = []
    while len(out) < 10 and s + len(out) < len(g) and g[s + len(out)] in NOP:
        out.append(g[s + len(out)])
    return out, (len(out) < 10 and s + len(out) >= len(g))

def predict(g, jmax=9):
    """('exact', j) | ('rotated', ncopy) | ('never', why) | ('filtered', why) | ('abstain', why)"""
    L = len(g); n2 = L; alloc = False
    ip = fh = rh = wh = nc = 0
    seen, checks = {}, []              # checks: (step, ncopy, label or None, path_neutral)
    for step in range(60 * L):
        if ip >= L: return ("abstain", "IP in child half")
        key = (ip, fh, rh, wh, alloc)
        if key in seen:
            s0, a = seen[key]
            if nc == a: return ("never", "loop without copies")
            p = nc - a; break
        seen[key] = (step, nc)
        op = g[ip]
        if op not in NOP and ip + 1 >= L: return ("abstain", "modifier read from child half")
        nxt = g[(ip + 1) % L]; mod = nxt if nxt in NOP else None
        adv = 1 + (mod is not None)    # line 131; cases below override as petri does
        if op in NOP: adv = 1
        elif op == HCOPY:
            if nc == 0 and (not alloc or (rh, wh) != (0, L)):
                return ("filtered", "first copy not from (RH,WH)=(0,L) after alloc")
            nc += 1; adv = 1
        elif op == IFLAB:
            lab, edge = label(g, ip + 1); k = len(lab)
            if edge: return ("abstain", "label runs into child half")
            checks.append((step, nc, tuple(lab), ip + 1 + k < L and g[ip + 1 + k] == HDIV))
            adv = 2 + k                # fail path, lines 152-153
        elif op == HDIV: checks.append((step, nc, None, True)); adv = 1   # failed carve, line 321
        elif op == HALLOC: alloc, n2, adv = True, 2 * L, 1
        elif op == MOVH:
            hd = mod if mod is not None else 0
            if hd == 0: ip = fh; continue             # lines 155-158
            if hd == 1: rh = fh
            if hd == 2: wh = fh
        elif op == HSRCH:                             # lines 224-241
            lab, edge = label(g, ip + 1); k = len(lab); adv = 1 + k
            if edge: return ("abstain", "search label runs into child half")
            want = bytes(COMP[x] for x in lab)
            if not lab: fh = (ip + 1) % n2
            else:
                q = bytes(g).find(want, ip + 1 + k)   # parent tail is scanned first in petri too
                if q >= 0: fh = (q + k) % n2
                elif not alloc:
                    q = bytes(g * 2).find(want, ip + 1 + k); fh = ((q + k) if q >= 0 else ip + 1) % L
                elif want not in bytes(g * 2) and 0 not in want: fh = (ip + 1) % n2
                else: return ("abstain", "h-search would scan the child half")
        elif op in DATA_JUMPS: return ("abstain", "register-dependent control flow")
        ip = (ip + adv) % n2
    else: return ("never", "no loop closed")
    pre = [(n, lab, neu) for s, n, lab, neu in checks if s < s0]
    cyc = [(n, lab, neu) for s, n, lab, neu in checks if s >= s0]
    H = (jmax + 1) * L
    sched = sorted(pre + [(n + m * p, lab, neu) for n, lab, neu in cyc for m in range(H // p + 2)])
    for n, lab, neu in sched:
        if n > H: break
        if lab is not None:
            k = len(lab)
            if n < k or any(g[(n - k + t) % L] != COMP[lab[t]] for t in range(k)): continue
        if not neu: return ("abstain", f"passing if-label at ncopy {n} not followed by h-divide")
        r = n % (2 * L) or 2 * L; w = (L + n) % (2 * L) or 2 * L    # carve 265-273, RH=n, WH=L+n
        child = w - r if w > r else 0
        if child >= 10 and r >= 10 and 0.5 <= child / r <= 2 and n >= child / 2:
            return ("exact", n // L) if n % L == 0 else ("rotated", n)
    return ("never", f"no passing check at a carveable ncopy within {jmax} laps")
```

Two consequences of the carve arithmetic are worth stating in the post. A check passes mid-lap with ncopy mod 2L in [L/2, L) only if the complement of the label occurs elsewhere in the genome, and then the child is a rotation of the parent, which your filter at `lap_cells.py:24` silently drops. And the predictor also returns the reason for "never", which is a run-forever prediction.

**(3) Sampling plan.** Parents: the ancestor (p=1, e=1, L=100) plus two census genomes per observed steady period, chosen after extending `lap_cells.py` to log p for the fits, not just the misses. Mutant classes per parent, each with its own `random.Random(1000 + 10*parent + cls)` recorded in the output JSON, and every genome string checked against the set from two_step_filter.json before use:

- **Filler indels (F):** insert or delete 1 or 2 nops inside the longest nop run outside the loop. This shifts L mod 3 while holding p and e fixed. Deterministic, 4 per parent.
- **Loop edits (C):** insert 1 to 4 extra `h-copy` directly after the loop's first `h-copy` (changes p and e together), and 0 to p-1 copies before the h-search that sets the flow head (changes e alone). Crossed with F this fills every (L mod 3, p, e mod p) cell for p in 1..5.
- **Random (R):** per parent 100 single substitutions drawn as `petri.py:139` does, 50 single indels drawn as `petri.py:276-281` does, 50 double substitutions. These produce the structures the predictor did not anticipate.

Six parents gives about 1400 genomes. Random single mutants of a copier stay exact copiers roughly four times in five, so expect at least 50 exact copiers per (L mod 3, p) cell for p of 1 to 3, with p of 4 and 5 pooled. Period 1 is covered by the ancestor's F and R classes. Run with a cap of 40·L steps rather than 3000 (`lap_cells.py:7`), since 5 laps at 3 steps per copy on L=256 already exceed 3000 and the census silently dropped slow genomes. Record born, exact, j, rotation offset, steps at division, and whether steps are within 20·L, the world's age limit at `petri.py:357`, which the census runner bypasses by calling `step` directly. Freeze the predictor at a commit hash before the first run.

**(4) What falsifies what.**

- **Not falsifiable by data:** odd j, and "exact division happens at the first passing check at an odd multiple of L". An even j or a division at a non-check means a misreading of `carve` or `if-label`, not biology.
- **Predicted exact j, observed exact j' ≠ j:** the static schedule is wrong, so a mechanism outside the loop reading intervenes. The likely culprits are the ones the predictor abstains on, so an error here means an abstention rule is missing.
- **Predicted never, observed exact birth:** the strongest result. It is the p=1 versus p=3 failure in another guise, and with p=4 and p=2 loops the arithmetic predicts many "never" cells, so this class will be well populated.
- **Predicted exact, observed rotated child or vice versa:** the mid-lap pass logic or the L/2 carve condition is misjudged.
- **Risky confirmation:** p=5 with L mod 5 = 1 predicts j=7 for e ≡ 2 mod 5 and j=9 for e ≡ 4 mod 5, outside the observed {1,3,5}. Those organisms need about 10 to 13 L instructions, so they also survive the world's age limit.
- **Abstention above about a quarter:** the loop class is wider than the ancestor's design and the post should say the result covers only the covered class.

The empirical content the post can honestly claim after this is the prevalence of period-3 loops in evolved copiers and whether j>1 genotypes persist in the world under merit and the age limit, since the census over-represents them relative to population abundance.