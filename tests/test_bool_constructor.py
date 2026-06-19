import os
from unittest import mock

import pytest
import yaml
from absql import Runner
from absql.files.loader import scalar_to_value


@pytest.fixture(autouse=True)
def mock_env_dev():
    with mock.patch.dict(os.environ, {"ENV": "dev"}):
        yield


def test_yaml_false_resolves_to_python_false():
    """bool(\"false\") is True in Python — verify the loader does not hit that trap."""
    runner = Runner()
    result = runner.render("tests/files/bool_constructor.yml", return_dict=True)
    assert result["flag_true"] is True
    assert result["flag_false"] is False


def test_yaml_false_renders_correctly():
    runner = Runner()
    got = runner.render("tests/files/bool_constructor.yml")
    assert got == "SELECT 'True' AS flag_true, 'False' AS flag_false"


def test_scalar_to_value_bool():
    """scalar_to_value must return Python bool, not bool-of-string."""
    for truthy in ("true", "True", "TRUE", "yes", "Yes", "YES", "y", "Y", "on", "On", "ON"):
        node = yaml.ScalarNode(tag="tag:yaml.org,2002:bool", value=truthy)
        assert scalar_to_value(node, {}) is True, f"expected True for {truthy!r}"
    for falsy in ("false", "False", "FALSE", "no", "No", "NO", "n", "N", "off", "Off", "OFF"):
        node = yaml.ScalarNode(tag="tag:yaml.org,2002:bool", value=falsy)
        assert scalar_to_value(node, {}) is False, f"expected False for {falsy!r}"


def test_scalar_to_value_int():
    node = yaml.ScalarNode(tag="tag:yaml.org,2002:int", value="42")
    assert scalar_to_value(node, {}) == 42


def test_scalar_to_value_float():
    node = yaml.ScalarNode(tag="tag:yaml.org,2002:float", value="3.14")
    assert abs(scalar_to_value(node, {}) - 3.14) < 1e-9


def test_scalar_to_value_str():
    node = yaml.ScalarNode(tag="tag:yaml.org,2002:str", value="hello")
    assert scalar_to_value(node, {}) == "hello"
