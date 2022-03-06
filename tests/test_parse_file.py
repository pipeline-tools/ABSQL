import pytest
from absql.files import parse


@pytest.fixture
def simple_sql_path():
    return "tests/files/simple.sql"


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


def test_simple_sql(simple_sql_path):
    res = parse(simple_sql_path)
    assert "sql" in res.keys()
    assert "my_table_placeholder" in res.keys()
    assert res["my_table_placeholder"] == "my_table"
    assert res["sql"] == "SELECT * FROM {{my_table_placeholder}}"


def test_simple_yml(simple_yml_path):
    res = parse(simple_yml_path)
    assert "sql" in res.keys()
    assert "my_table_placeholder" in res.keys()
    assert res["my_table_placeholder"] == "my_table"
    assert res["sql"] == "SELECT * FROM {{my_table_placeholder}}"
