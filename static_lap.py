"""#491 static lap predictor (draft by Fable 24.10, fitted to petri.py semantics by errata).
Predicts the division outcome of a genome from its text, without stepping the world: an abstract run with
registers tracked while known (unknown after IO), every if-label modelled as failing (path-neutral when the next op is
h-divide) and every h-divide as a failed carve, run to (jmax+1)*L copies; then the first check whose label would pass
and whose carve is viable gives the outcome. It never lets a check pass, so it predicts, it does not replay.
Returns ('exact', j) | ('rotated', ncopy) | ('never', why) | ('filtered', why) | ('abstain', why)."""
from petri import NOP, COMP, CODE
HCOPY, IFLAB, MOVH, HSRCH, HALLOC, HDIV = (CODE[n] for n in
    ("h-copy", "if-label", "mov-head", "h-search", "h-alloc", "h-divide"))
DATA_JUMPS = {CODE[n] for n in ("jmp-head", "set-flow")}  # resolved when the register is known
CONDS = {CODE["if-n-equ"], CODE["if-less"]}
CONTROL = {HCOPY, IFLAB, MOVH, HSRCH, HALLOC, HDIV} | DATA_JUMPS | CONDS

def label(mem, s):                     # petri.World.label: wraps around the current memory
    n = len(mem); out = []
    while len(out) < 10 and mem[(s + len(out)) % n] in NOP:
        out.append(mem[(s + len(out)) % n])
    return out

def predict(g, jmax=9):
    predict.checks = None
    g = list(g); L = len(g)
    mem = g[:]                         # memory: parent, then h-alloc's zero-filled child half (as petri.py)
    alloc = False; ip = fh = rh = wh = nc = 0
    reg = [0, 0, 0]; stk = []         # registers tracked while known (None after IO or from unknown inputs)
    regsteps = []                      # steps where a branch or head move was resolved from register values
    M32 = 0xFFFFFFFF
    copied = []
    checks = []              # checks: (step, ncopy, label tuple or None for h-divide, neutral)
    H = (jmax + 1) * L
    for step in range(100 * L):        # abstract run with every check failing, until the horizon in copies
        n2 = len(mem); ip %= n2
        if ip >= L: return ("abstain", "IP in child half")
        if nc > H: break
        op = g[ip]
        nxt = mem[(ip + 1) % n2]
        if nxt is None: return ("abstain", "modifier read from child half")
        mod = nxt if nxt in NOP else None
        adv = 1 + (mod is not None and op not in NOP)
        if op in NOP: adv = 1
        elif op == CODE["set-flow"]:
            v = reg[mod if mod is not None else 2]
            if v is None: return ("abstain", "set-flow from an unknown register")
            fh = v % n2; regsteps.append(step)
        elif op == CODE["jmp-head"]:
            hd = mod if mod is not None else 0
            if reg[2] is None: return ("abstain", "jmp-head by an unknown register")
            regsteps.append(step)
            if hd == 0: ip = (ip + reg[2] + 1) % n2; continue
            if hd == 1: rh = (rh + reg[2]) % n2
            if hd == 2: wh = (wh + reg[2]) % n2
            if hd == 3: fh = (fh + reg[2]) % n2
        elif op in CONDS:              # skips the next instruction on a register test
            rr = mod if mod is not None else 1
            a, b = reg[rr], reg[COMP[rr]]
            adv = 1 if mod is None else 2
            if a is not None and b is not None:
                if not ((a != b) if op == CODE["if-n-equ"] else (a < b)): adv += 1
                regsteps.append(step)
            else:                      # unknown: neutral only if the skippable op touches no head, copy, label, branch
                sk = mem[(ip + adv) % n2]
                if sk is None or sk in CONTROL: return ("abstain", "unknown-register skip over a control instruction")
        elif op == CODE["get-head"]:
            reg[2] = {0: ip, 1: rh, 2: wh, 3: fh}[mod if mod is not None else 0]
        elif op == CODE["IO"]:
            reg[mod if mod is not None else 1] = None
        elif op in (10, 11, 12, 13):
            r = mod if mod is not None else 1; v = reg[r]
            if v is not None: reg[r] = (v >> 1) if op == 10 else ((v << 1) & M32) if op == 11 else ((v + 1) & M32) if op == 12 else ((v - 1) & M32)
        elif op == 14:
            if len(stk) < 10: stk.append(reg[mod if mod is not None else 1])
        elif op == 15:
            reg[mod if mod is not None else 1] = stk.pop() if stk else 0
        elif op == 17:
            r = mod if mod is not None else 1; reg[r], reg[COMP[r]] = reg[COMP[r]], reg[r]
        elif op in (18, 19, 20):
            r = mod if mod is not None else 1; a, b = reg[1], reg[2]
            reg[r] = None if a is None or b is None else (((a + b) if op == 18 else (a - b) if op == 19 else ~(a & b)) & M32)
        elif op == HCOPY:
            v = mem[rh % n2]; mem[wh % n2] = v; copied.append(v); nc += 1; rh = (rh + 1) % n2; wh = (wh + 1) % n2; adv = 1
        elif op == IFLAB:
            lab = label(mem, ip + 1); k = len(lab)
            if any(mem[(ip + 1 + t) % n2] is None for t in range(k + 1)): return ("abstain", "label runs into child half")
            nxt2 = mem[(ip + 1 + k) % n2]
            checks.append((step, nc, tuple(lab), nxt2 == HDIV, rh, wh, tuple(copied[-10:]), mem[:]))
            adv = 2 + k
        elif op == HDIV: checks.append((step, nc, None, True, rh, wh, (), mem[:])); adv = 1
        elif op == HALLOC:
            if not alloc and L < 400: mem = mem + [0] * L; alloc = True; reg[0] = L
            adv = 1
        elif op == MOVH:
            hd = mod if mod is not None else 0
            if hd == 0: ip = fh; continue
            if hd == 1: rh = fh
            if hd == 2: wh = fh
        elif op == HSRCH:
            lab = label(mem, ip + 1); k = len(lab); adv = 1 + k
            if any(mem[(ip + 1 + t) % n2] is None for t in range(k + 1)): return ("abstain", "search label runs into child half")
            if not lab: fh = (ip + 1) % n2; reg[1] = reg[2] = 0
            else:
                want = [COMP[x] for x in lab]; tri = mem * 3; pos = None
                for q in range(ip + 1 + k, ip + n2 - 1 + k):
                    seg = tri[q:q + k]
                    if None in seg:
                        return ("abstain", "h-search scans unknown child letters")
                    if seg == want: pos = q % n2; break
                if pos is None: fh = (ip + 1) % n2; reg[1] = reg[2] = 0
                else: fh = (pos + k) % n2; reg[1] = (pos - ip) % n2; reg[2] = k
        ip = (ip + adv) % len(mem)
    predict.checks = [(n, lab) for s, n, lab, *_ in checks]   # for the arithmetic rule (ncopy at each check)
    if nc == 0: return ("never", "no copies within the step budget")
    for s, n, lab, neu, r, w, tail, m in checks:
        if lab is not None:            # if-label passes iff the last k copied letters are the label's complement
            k = len(lab)
            if k == 0 or len(tail) < k: continue
            if None in tail[-k:]: return ("abstain", "label compared with unknown letters")
            if list(tail[-k:]) != [COMP[x] for x in lab]: continue
            if not neu: return ("abstain", f"passing if-label at ncopy {n} not followed by h-divide")
        N = len(m); r = r or N; w = w or N        # carve: a head at 0 means the end of memory
        child = m[r:w] if w > r else []
        if len(child) < 10 or r < 10 or not (0.5 <= len(child) / r <= 2) or n < 0.5 * len(child): continue
        if None in child: return ("abstain", "carve would take unknown letters")
        if child == g: return ("exact", n // L) if n % L == 0 else ("exact-offlap", n)
        if len(child) == L and any(child == g[q:] + g[:q] for q in range(1, L)): return ("rotated", n)
        return ("other-birth", len(child))
    return ("never", f"no passing check with a viable carve within {jmax + 1} laps")


def arith(g):
    """The arithmetic rule from the thread (zenith #101177, #101194): e = ncopy at the first if-label check, p = the
    ncopy gap to the second; with gL = gcd(L, p): never if gL does not divide e, else the least odd j with
    j*(L/gL) = e/gL (mod p/gL). Needs the forced-fail schedule from predict(); None if fewer than 2 if-label checks."""
    from math import gcd
    predict(g)
    ch = [n for n, lab in (predict.checks or []) if lab is not None]
    if len(ch) < 2 or ch[1] - ch[0] <= 0: return None
    L = len(g); e, p = ch[0], ch[1] - ch[0]
    q = gcd(L, p)
    if e % q: return ("never", p, e)
    pp = p // q
    for j in range(1, 2 * pp + 1, 2):
        if (j * (L // q) - e // q) % pp == 0: return ("exact", j, p, e)
    return ("never", p, e)
