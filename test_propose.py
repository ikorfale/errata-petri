import json, subprocess, sys, os, tempfile
H = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(H, "proposals/example-age-limit.json")))


def check(p):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(p, f)
    r = subprocess.run([sys.executable, os.path.join(H, "propose.py"), "check", f.name], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def test_example_passes_and_hash_is_order_free():
    rc, out = check(EX)
    rc2, out2 = check(dict(reversed(list(EX.items()))))
    assert rc == 0 and rc2 == 0 and out.split("sha256 ")[1][:64] == out2.split("sha256 ")[1][:64]


def test_rejections():
    for bad, word in [({**EX, "treatment": {"age_limit": "no"}}, "expected bool"),
                      ({**EX, "treatment": {"gravity": 1}}, "not a switch"),
                      ({**EX, "treatment": {}}, "same world"),
                      ({**EX, "held_if": 4}, "held_if"),
                      ({**EX, "seeds": 50}, "seeds must"),
                      ({**EX, "metric": "happiness"}, "metric"),
                      ({**EX, "note": "x"}, "unknown fields"),
                      ({**EX, "treatment": {"copy_mut": 0.5}}, "outside")]:
        rc, out = check(bad)
        assert rc != 0 and word in out, (bad, out)


if __name__ == "__main__":
    test_example_passes_and_hash_is_order_free(); test_rejections(); print("ok")
