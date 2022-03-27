import pytest
from absql import Runner


@pytest.fixture()
def runner():
    return Runner(greeting="Hello")


def test_set_context(runner):
    assert runner.extra_context["greeting"] == "Hello"
    runner.set_context(greeting="Hey")
    assert runner.extra_context["greeting"] == "Hey"
