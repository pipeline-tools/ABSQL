import pytest
import datetime
from absql import Runner
from copy import copy


@pytest.fixture(scope="function")
def r_original():
    # dt because I am scared to copy modules
    return Runner(f="foo", dt=datetime)


@pytest.fixture(scope="function")
def r_copy(r_original):
    return copy(r_original)


def test_copy_set_context(r_original, r_copy):
    r_copy.set_context(f="bar")
    assert r_original.render("{{f}}") == "foo"
    assert r_copy.render("{{f}}") == "bar"


def test_copy_set_attr(r_original, r_copy):
    r_original.partial_kwargs = ["a"]
    r_copy.partial_kwargs = ["b"]
    assert r_original.partial_kwargs == ["a"]
    assert r_copy.partial_kwargs == ["b"]

    r_copy.extra_context = {"f": "buzz"}
    assert r_original.render("{{f}}") == "foo"
    assert r_copy.render("{{f}}") == "buzz"
