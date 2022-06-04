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


@pytest.fixture
def no_frontmatter_path():
    return "tests/files/no_frontmatter.sql"


def test_render_simple_sql(runner, simple_sql_path):
    sql = runner.render(simple_sql_path)
    assert sql == "SELECT * FROM my_table"


def test_render_no_frontmatter(runner, no_frontmatter_path):
    sql = runner.render(no_frontmatter_path)
    assert sql == "SELECT * FROM Hello"


def test_render_text_only(runner):
    got = runner.render("{{greeting}}, {{env_var('name')}}!")
    want = "Hello, Bob!"
    assert got == want


def test_replace_only_changes(runner):
    original = runner.render("{{env_switch(foo='address')}} and {{greeting}}")
    assert original == "value_unspecified and Hello"

    replaced_only = runner.render(
        "{{env_switch(foo='address')}} and {{greeting}}", replace_only=True
    )
    assert replaced_only == "{{env_switch(foo='address')}} and Hello"

    original_2 = runner.render("{{env_switch(foo='address')}} and {{greeting}}")
    assert original_2 == "value_unspecified and Hello"
