import os
import mock
import pytest
from absql import Runner


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"ENV": "test"}):
        yield


@pytest.fixture
def runner():
    return Runner()


def test_env_var(runner):
    got = runner.render("{{env_var('ENV')}}")
    want = "test"
    assert got == want


def test_env_switch(runner):
    got = runner.render("{{env_switch(default='my_default', test='my_test')}}")
    want = "my_test"
    assert got == want


def test_env_switch_default(runner):
    got = runner.render("{{env_switch(default='my_default', prod='my_prod')}}")
    want = "my_default"
    assert got == want


def test_env_switch_unspecified(runner):
    got = runner.render("{{env_switch(prod='my_prod')}}")
    want = "value_unspecified"
    assert got == want
