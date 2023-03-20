from absql.utils import (
    nested_apply,
    get_function_arg_names,
    partialize_function,
    load_body,
)


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


def test_partialize_function():
    def simple_func(a, engine):
        return a + engine

    simple_func = partialize_function(simple_func, engine=7)
    got = simple_func(3)
    want = 10
    assert got == want


def test_load_body_frontmatter():
    assert (
        load_body("tests/files/simple.sql")
        == "\nSELECT * FROM {{my_table_placeholder}}\n"
    )


def test_load_body_no_frontmatter():
    assert (
        load_body("tests/files/no_frontmatter.sql")
        == "{% set cols='*' %}\n\nSELECT {{cols}} FROM {{greeting}}\n"
    )
