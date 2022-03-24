from absql.utils import nested_apply


def test_simple_apply():
    d = {"a": "a", "b": "b", "c": 5}
    got = nested_apply(d, lambda x: x + "zzz")
    want = {"a": "azzz", "b": "bzzz", "c": 5}
    assert got == want


def test_nested_list():
    d = {"a": "a", "b": "b", "c": [5, "d"]}
    got = nested_apply(d, lambda x: x + "zzz")
    want = {"a": "azzz", "b": "bzzz", "c": [5, "dzzz"]}
    assert got == want


def test_nested_dict():
    d = {"a": "a", "b": "b", "c": {5: "d"}}
    got = nested_apply(d, lambda x: x + "zzz")
    want = {"a": "azzz", "b": "bzzz", "c": {5: "dzzz"}}
    assert got == want
