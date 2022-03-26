from absql.utils import nested_apply, get_function_arg_names, partialize_engine_func


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


def test_get_function_arg_names():
    def func(a, b):
        return a + b

    got = get_function_arg_names(func)
    want = ["a", "b"]
    assert got == want


def test_partialize_engine_func():
    def simple_func(a, engine):
        return a + engine

    simple_func = partialize_engine_func(simple_func, 7)
    got = simple_func(3)
    want = 10
    assert got == want
