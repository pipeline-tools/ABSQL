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
    def double_it(x):
        return x + x

    return Runner(extra_constructors={"double_it": double_it}, greeting="Hello")


@pytest.fixture()
def contextless_runner():
    return Runner()


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


def test_render_extra_context(runner):
    got = runner.render("{{new_greeting}}, {{env_var('name')}}!", new_greeting="Hey")
    want = "Hey, Bob!"
    assert got == want


def test_contextless_runner(contextless_runner):
    got = contextless_runner.render("{{no_greeting}}, Bill!")
    want = "{{ no_greeting }}, Bill!"
    assert got == want


def test_replace_only_changes(runner):
    original = runner.render("{{env_switch(foo='address')}} and {{greeting}}")
    assert original == "value_unspecified and Hello"

    replaced_only = runner.render(
        "{{env_switch(foo='address')}} and {{greeting}}", replace_only=True
    )
    assert replaced_only == "{{ env_switch(foo='address') }} and Hello"

    original_2 = runner.render("{{env_switch(foo='address')}} and {{greeting}}")
    assert original_2 == "value_unspecified and Hello"


def test_runner_renders_yaml(runner):
    got = runner.render("tests/files/constructor.yml")
    want = "SELECT * FROM tabletable"
    assert got == want
