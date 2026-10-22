"""Checks: the ancestor copies itself exactly, and tasks need two distinct inputs."""
from petri import ANCESTOR, M32, Org, World


def test_ancestor_copies_exactly():
    w = World(side=10, seed=1, copy_mut=0.0)
    w.indel = 0.0
    c = w.inject(ANCESTOR, "a", cell=0)
    for _ in range(200):
        w.run_update()
        if w.births:
            break
    kids = [o for o in w.cells if o is not None and o is not w.cells[c]]
    assert w.births >= 1 and kids and kids[0].mem == ANCESTOR


def test_one_input_earns_nothing():
    w = World(side=3, seed=1)
    o = Org(ANCESTOR, "a")
    o.inputs = [12345]
    for v in (0, M32, ~12345 & M32):     # 0 used to pass XOR and ANDN, M32 EQU and ORN
        w.output(o, v)
    assert o.tasks == set()


def test_two_inputs_score():
    w = World(side=3, seed=1)
    o = Org(ANCESTOR, "a")
    a, b = 0b1100, 0b1010
    o.inputs = [b, a]
    w.output(o, a ^ b)
    assert o.tasks == {"XOR"}


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
