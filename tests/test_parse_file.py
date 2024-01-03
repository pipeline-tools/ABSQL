import pytest
from absql.files import parse


@pytest.fixture
def simple_sql_path():
    return "tests/files/simple.sql"


def test_simple_sql(simple_sql_path):
    res = parse(simple_sql_path)
    assert "sql" in res.keys()
    assert "my_table_placeholder" in res.keys()
    assert res["my_table_placeholder"] == "my_table"
    assert res["sql"] == "SELECT * FROM {{my_table_placeholder}}"


@pytest.mark.parametrize(
    argnames="yml_path",
    argvalues=[
        pytest.param("tests/files/simple.yml", id="simple_yml"),
        pytest.param(
            "tests/files/simple_with_doc_header.yml", id="simple_yml_with_doc_header"
        ),
    ],
)
def test_simple_yml(yml_path):
    res = parse(yml_path)
    assert "sql" in res.keys()
    assert "my_table_placeholder" in res.keys()
    assert res["my_table_placeholder"] == "my_table"
    assert res["sql"] == "SELECT * FROM {{my_table_placeholder}}"
