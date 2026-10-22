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
    assert w.births >= 1 and kids and list(kids[0].mem) == ANCESTOR


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


def test_divide_needs_copying():
    # padding exploit: a child region that was never copied must not be born
    w = World(side=5, seed=1)
    o = Org(ANCESTOR, "a")
    w.cells[0] = o
    o.mem.extend(bytes(len(o.mem)))
    o.heads = [0, 100, 0, 0]               # read head at the split, write head wrapped
    w.divide(o, 0)
    assert w.births == 0
    o.ncopy, o.heads = 100, [0, 100, 0, 0]
    w.divide(o, 0)
    assert w.births == 1


def test_inject_needs_label_match():
    from petri import CODE
    w = World(side=3, seed=1, parasites=True)
    for cell in range(9):
        w.cells[cell] = Org(ANCESTOR, "host")     # ancestor holds nop-B (complement of nop-A)
    g = [CODE["inc"]] * 20 + [CODE["inject"], CODE["nop-A"]] + [CODE["inc"]] * 18
    o = Org(g, "para")
    o.mem.extend(bytes(o.mem))
    o.ncopy, o.heads = 40, [20, 40, 0, 0]
    w.cells[4] = o
    w.step(o, 4)
    assert w.injections == 1 and sum(h.para is not None for h in w.cells) == 1
    w2 = World(side=3, seed=1, parasites=True)     # hosts without the complement resist
    for cell in range(9):
        w2.cells[cell] = Org([CODE["nop-C"]] * 50, "host")
    o2 = Org(g, "para")
    o2.mem.extend(bytes(o2.mem))
    o2.ncopy, o2.heads = 40, [20, 40, 0, 0]
    w2.cells[4] = o2
    w2.step(o2, 4)
    assert w2.injections == 0



def test_submit_parser_is_strict():
    from submit import Reject, parse_strict
    from petri import show
    letters = show(ANCESTOR)
    assert parse_strict(letters) == ANCESTOR
    assert parse_strict("# my seed\n" + letters + "  # trailing comment\n") == ANCESTOR
    names = " ".join(__import__("petri").OPS[i] for i in ANCESTOR)
    assert parse_strict(names) == ANCESTOR
    for bad, why in [(letters[:50] + "!" + letters[51:], "unknown letter"),
                     (names.replace("h-copy", "h-kopy"), "unknown op"),
                     ("abcdefghi", "length"), (letters * 3, "length"),
                     (letters[:-1] + "A", "inject")]:
        try:
            parse_strict(bad)
        except Reject as e:
            assert why in str(e), (why, e)
        else:
            raise AssertionError(f"accepted: {why}")


def test_submit_refuses_non_copier_and_duplicates():
    import tempfile
    tmp_path = tempfile.mkdtemp()
    from submit import add, check
    from petri import show
    assert not check("c" * 50)["ok"]
    a = show(ANCESTOR)
    assert add(a, "x", 1, root=str(tmp_path))["ok"]
    assert "already seeded" in add(a, "x", 1, root=str(tmp_path))["reason"]
    assert "same genome" in add(a, "y", 1, root=str(tmp_path))["reason"]
    assert add(a, "y", 2, root=str(tmp_path))["ok"]


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)


def test_tagged_inputs_never_coincide():
    # every output value that earns a task earns exactly one task, and sums/differences earn none
    import random
    from petri import TAGS, TASKS
    rng = random.Random(5)
    for _ in range(3000):
        i, j = rng.sample(range(3), 2)
        a = (TAGS[i] << 24) | rng.getrandbits(24)
        b = (TAGS[j] << 24) | rng.getrandbits(24)
        vals = {}
        for name, f, _ in TASKS:
            for v in set(f(a, b)):
                vals.setdefault(v, set()).add(name)
        assert all(len(names) == 1 for names in vals.values())
        for v in ((a + b) & M32, (a - b) & M32, (b - a) & M32, (a + (~b & M32)) & M32):
            assert v not in vals


def test_tag_pairs_cover_all_bit_pairs():
    from petri import TAGS
    for i in range(3):
        for j in range(3):
            if i != j:
                pairs = {((TAGS[i] >> k) & 1, (TAGS[j] >> k) & 1) for k in range(8)}
                assert pairs == {(0, 0), (0, 1), (1, 0), (1, 1)}
