"""Count every read of the lineage fields Org.anc and Org.ptasks during a Petri daily run, by call site (glitchfox,
board 107096, 29.10). A digest that matches after stripping anc/ptasks over a 400-update sample does not show the
fields are write-only: a read in a rare branch may not have fired yet. This wraps the two slot descriptors so every
read of the whole day is counted where it happens. Writes pass through untouched, so dynamics and digest are unchanged.

Expected readers: petri.py divide (copies the parent's anc to the child; hasattr guard), daily.py lineage census,
and the serialisers (world_digest canon, pickle, snapshot). Any read from another petri.py function is a read by the
dynamics and must be 0."""
import os, sys
from collections import Counter

READS = Counter()


class Watched:
    def __init__(self, name, slot):
        self.name, self.slot = name, slot

    def __get__(self, obj, typ=None):
        if obj is None:
            return self
        f = sys._getframe(1)
        READS[(self.name, os.path.basename(f.f_code.co_filename), f.f_code.co_name, f.f_lineno)] += 1
        return self.slot.__get__(obj, typ)

    def __set__(self, obj, v):
        self.slot.__set__(obj, v)

    def __delete__(self, obj):
        self.slot.__delete__(obj)


def install(cls, names=("anc", "ptasks")):
    for n in names:
        d = cls.__dict__[n]
        if not isinstance(d, Watched):
            setattr(cls, n, Watched(n, d))


def report():
    sites = [{"field": n, "file": fn, "func": fu, "line": ln, "reads": c} for (n, fn, fu, ln), c in sorted(READS.items())]
    dyn = sum(s["reads"] for s in sites if s["file"] == "petri.py" and s["func"] != "divide")
    return {"sites": sites, "engine_reads_outside_divide": dyn}
