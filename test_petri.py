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
    import json, tempfile
    tmp_path = tempfile.mkdtemp()
    from submit import add, check
    from petri import show
    assert not check("c" * 50)["ok"]
    a = show(ANCESTOR)
    assert add(a, "x", 1, root=str(tmp_path))["ok"]
    assert "already seeded" in add(a, "x", 1, root=str(tmp_path))["reason"]
    assert "same genome" in add(a, "y", 1, root=str(tmp_path))["reason"]
    assert add(a, "y", 2, root=str(tmp_path))["ok"]
    assert "origin must be" in add(a, "z", 3, root=str(tmp_path), origin="found")["reason"]
    assert "must declare" in add(a, "z", 3, root=str(tmp_path), origin="evolved")["reason"]
    r = add(a, "z", 3, root=str(tmp_path), origin="evolved", updates=5000, side=30)
    assert r["ok"] and json.loads(open(r["recorded"]).read().splitlines()[-1])["side"] == 30


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


# theone 99870: the rebuild-digest contract
import copy
from world_digest import compare


def _epoch_like(parasites=False):
    w = World(side=10, seed=3, parasites=parasites)
    w.inject(ANCESTOR, "a", cell=0)
    for _ in range(30):
        w.run_update()
    return w


def test_digest_reset_flag_only_is_whole_state_change_but_excepted_when_parasites_off():
    a = _epoch_like(); b = copy.deepcopy(a); b.reset_failed_inject = not a.reset_failed_inject
    v = compare(a, b)
    assert not v["whole_state_equal"] and v["differs"] == ["reset_failed_inject"]
    assert v["accept"] and v["excepted"] == ["reset_failed_inject"]


def test_digest_rejects_engine_setting_change_with_same_cells_and_rng():
    a = _epoch_like()
    for field, val in (("slice", a.slice + 1), ("copy_mut", a.copy_mut * 2)):
        b = copy.deepcopy(a); setattr(b, field, val)
        v = compare(a, b)
        assert not v["accept"] and v["differs"] == [field]


def test_digest_exception_off_when_parasites_on():
    a = _epoch_like(parasites=True); b = copy.deepcopy(a); b.reset_failed_inject = not a.reset_failed_inject
    v = compare(a, b)
    assert not v["accept"] and v["differs"] == ["reset_failed_inject"] and v["excepted"] == []


def test_digest_identical_rebuild_accepts_and_names_revisions():
    a = _epoch_like(); v = compare(a, copy.deepcopy(a))
    assert v["accept"] and v["whole_state_equal"] and v["differs"] == []
    assert set(v["revisions"]) == {"petri.py", "world_digest.py"}


def test_least_odd_j_matches_theone_fixtures_and_enumeration():
    from static_lap import least_odd_j
    fx = {(95, 4, 0): None, (95, 4, 1): 3, (95, 4, 2): None, (95, 4, 3): 1, (98, 4, 0): None, (98, 4, 2): 1, (96, 4, 0): 1}
    for k, v in fx.items():
        assert least_odd_j(*k) == v, (k, least_odd_j(*k), v)
    n = none = 0
    for L in range(1, 101):
        for p in range(1, 33):
            for e in range(p):
                brute = next((j for j in range(1, 2 * p + 1, 2) if (j * L - e) % p == 0), None)
                assert least_odd_j(L, p, e) == brute, (L, p, e)
                n += 1
                none += brute is None
    assert n == 52800
    assert none == 20694, none  # zenith's independent total (#101425): 20,694 none, 32,106 with a solution


def test_scoring_table_total_and_strict():
    from scoring import table, score_static, score_arith, arith_premise, TRUTH
    allowed = {"hit", "miss", "abstain", "out-of-scope", "not-scored"}
    rows = table()
    assert all(c in allowed for _, _, cells in rows for c in cells)
    assert sum(len(cells) for _, _, cells in rows) == 12 * len(TRUTH)
    assert score_static(("rotated", 7), ("rotated", 8)) == "miss"            # parameter must match
    assert score_static(("other-birth", 40), ("other-birth", 40)) == "abstain"  # reported, not scored
    assert score_static(("exact", 1), ("exact", 1), ("exact", 3)) == "miss"    # seed-dependent truth
    assert score_static(("exact", 1), ("exact", 1), ("unresolved", "c")) == "out-of-scope"  # either seed unresolved
    assert score_arith(("never", 4, 2), ("exact", 3)) == "miss"
    assert score_arith(("exact", 1, 3, 0), ("rotated", 7)) == "not-scored"
    assert score_arith(("exact", 1, 3, 0), ("other-birth", 40), ("other-birth", 23)) == "not-scored"
    assert score_arith(("exact", 1, 3, 0), ("exact", 1), ("other-birth", 23)) == "hit"   # other seed -> premise
    assert score_arith(("exact", 1, 3, 0), ("exact", 1), ("exact", 3)) == "miss"
    assert score_arith(("never", 4, 2), ("other-birth", 40), ("exact", 5)) == "miss"
    assert arith_premise(("exact", 1, 3, 0), ("other-birth", 40), ("other-birth", 41)) is False
    assert arith_premise(("exact", 1, 3, 0), ("exact", 1), ("other-birth", 41)) is False
    assert arith_premise(("exact", 1, 3, 0), ("rotated", 7)) is False
    assert arith_premise(("never", 4, 2), ("never", "x")) is True


if __name__ == "__main__":
    n = 0
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
            n += 1
    print(n, "tests passed")
    # the count is enforced, not just printed: tests defined in this file's text, counted without the loop above
    import re, sys
    defined = len(re.findall(r"^def test_", open(__file__).read(), re.M))
    if n != defined:
        print(f"FAIL: {defined} tests defined, {n} ran"); sys.exit(1)
