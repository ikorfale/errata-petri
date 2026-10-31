"""lock() copied verbatim from lockfwd_verdict.py (that file runs on import)."""
def lock(rows):
    for r in rows:
        L, n = max(r["len_hist"], key=lambda x: (x[1], x[0]))
        if n / r["pop"] >= 0.5: return r["update"], L
    return None, None
