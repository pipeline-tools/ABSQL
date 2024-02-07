import pytest
import mock
import os
from pathlib import Path
from absql import Runner as r
from absql.functions.time import previous_date


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {"name": "Bob", "ENV": "dev", "my_env_var": "foo", "my_timezone": "EST"},
    ):
        yield


@pytest.fixture
def multi_block_comment_sql_path():
    return "tests/files/multi_block_comment.sql"


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("nested_constructors*.sql")],
)
def test_nested_constructors(sql_file):
    sql = r.render_file(sql_file)
    assert sql == "SELECT * FROM foo WHERE bar AND {previous}".format(
        previous=previous_date("EST")
    )


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("simple*.sql")],
)
def test_render_simple_sql(sql_file):
    sql = r.render_file(sql_file)
    assert sql == "SELECT * FROM my_table"


def test_render_simple_sql_with_multiple_block_comments(multi_block_comment_sql_path):
    sql = r.render_file(multi_block_comment_sql_path)
    assert sql == (
        "/*\nThis is a block comment in the SQL file contents.\n*/\n"
        "SELECT * FROM my_table"
    )


def test_render_simple_yml(simple_yml_path):
    sql = r.render_file(simple_yml_path)
    assert sql == "SELECT * FROM my_table"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("extra*.sql")],
)
def test_render_additional_sql(sql_file):
    sql = r.render_file(sql_file, extra="my_extra_context")
    assert sql == "SELECT * FROM my_table WHERE my_extra_context"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[
        pytest.param("tests/files/constructor.sql"),
        pytest.param("tests/files/constructor_block_comment_fm.sql"),
    ],
)
def test_render_constructor_sql(sql_file):
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
    sql = runner.render(sql_file)
    assert sql == "SELECT * FROM my_constructor_table WHERE '6' and 'this'"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("jinja_frontmatter*.sql")],
)
def test_render_jinja_frontmatter(sql_file):
    def provide_table():
        return "my_func_table"

    sql = r.render_file(sql_file, get_table=provide_table)
    assert sql == "SELECT * FROM my_func_table WHERE name = 'Bob'"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("jinja_frontmatter*.sql")],
)
def test_render_jinja_frontmatter_instantiated(sql_file):
    def provide_table():
        return "my_func_table"

    runner = r(get_table=provide_table)
    sql = runner.render(sql_file)
    assert sql == "SELECT * FROM my_func_table WHERE name = 'Bob'"


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("extra*.sql")],
)
def test_var_dict(sql_file):
    want = "SELECT * FROM my_table WHERE something different!"
    got = r.render_file(sql_file, file_context_from="my_var_dict")
    assert got == want
    runner = r(file_context_from="my_var_dict")
    got = runner.render(sql_file)
    assert got == want


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[
        str(f) for f in Path("tests/files/").rglob("constructors_plus_functions*.sql")
    ],
)
def test_constructor_plus_function(sql_file):
    got = r.render_file(sql_file)
    want = "SELECT * FROM somewhere_else"
    assert got == want
