import pytest
import mock
import os
from absql import Runner as r


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"name": "Bob"}):
        yield


@pytest.fixture
def extra_sql_path():
    return "tests/files/extra.sql"


@pytest.fixture
def simple_sql_path():
    return "tests/files/simple.sql"


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


@pytest.fixture
def constructor_sql_path():
    return "tests/files/constructor.sql"


@pytest.fixture
def constructor_plus_function_sql_path():
    return "tests/files/constructors_plus_functions.sql"


@pytest.fixture
def jinja_frontmatter_path():
    return "tests/files/jinja_frontmatter.sql"


def test_render_simple_sql(simple_sql_path):
    sql = r.render_file(simple_sql_path)
    assert sql == "SELECT * FROM my_table"


def test_render_simple_yml(simple_yml_path):
    sql = r.render_file(simple_yml_path)
    assert sql == "SELECT * FROM my_table"


def test_render_additional_sql(extra_sql_path):
    sql = r.render_file(extra_sql_path, extra="my_extra_context")
    assert sql == "SELECT * FROM my_table WHERE my_extra_context"


def test_render_constructor_sql(constructor_sql_path):
    def add(*nums):
        x = 0
        for n in nums:
            x += n
        return x

    def first(**kwargs):
        for i in range(len(kwargs)):
            if i == 0:
                return kwargs[list(kwargs.keys())[0]]

    def get_table():
        return "my_constructor_table"

    runner = r(extra_constructors=[get_table, add, first])
    sql = runner.render(constructor_sql_path)
    assert sql == "SELECT * FROM my_constructor_table WHERE '6' and 'this'"


def test_render_jinja_frontmatter(jinja_frontmatter_path):
    def provide_table():
        return "my_func_table"

    sql = r.render_file(jinja_frontmatter_path, get_table=provide_table)
    assert sql == "SELECT * FROM my_func_table WHERE name = 'Bob'"


def test_render_jinja_frontmatter_instantiated(jinja_frontmatter_path):
    def provide_table():
        return "my_func_table"

    runner = r(get_table=provide_table)
    sql = runner.render(jinja_frontmatter_path)
    assert sql == "SELECT * FROM my_func_table WHERE name = 'Bob'"


def test_var_dict(extra_sql_path):
    want = "SELECT * FROM my_table WHERE something different!"
    got = r.render_file(extra_sql_path, file_context_from="my_var_dict")
    assert got == want
    runner = r(file_context_from="my_var_dict")
    got = runner.render(extra_sql_path)
    assert got == want


def test_constructor_plus_function(constructor_plus_function_sql_path):
    got = r.render_file(constructor_plus_function_sql_path)
    want = "SELECT * FROM somewhere_else"
    assert got == want
