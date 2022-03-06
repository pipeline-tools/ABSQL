import pytest
from absql import render_file


@pytest.fixture
def simple_sql_path():
    return "tests/files/simple.sql"


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


def test_render_simple_sql(simple_sql_path):
    sql = render_file(simple_sql_path)
    assert sql == "SELECT * FROM my_table"


def test_render_simple_yml(simple_yml_path):
    sql = render_file(simple_yml_path)
    assert sql == "SELECT * FROM my_table"
