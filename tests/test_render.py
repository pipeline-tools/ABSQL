import pytest
import mock
import os
from absql import Runner


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"name": "Bob"}):
        yield


@pytest.fixture()
def runner():
    return Runner(greeting="Hello")


@pytest.fixture
def simple_sql_path():
    return "tests/files/simple.sql"


def test_render_simple_sql(runner, simple_sql_path):
    sql = runner.render(simple_sql_path)
    assert sql == "SELECT * FROM my_table"


def test_render_text_only(runner):
    got = runner.render("{{greeting}}, {{env_var('name')}}!")
    want = "Hello, Bob!"
    assert got == want
