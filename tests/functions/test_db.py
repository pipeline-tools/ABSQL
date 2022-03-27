import os
import mock
import pytest
from pandas import DataFrame
from sqlalchemy import create_engine
from absql.functions.db import table_exists, query_db, get_max_value
from absql import Runner


@pytest.fixture(scope="module")
def engine():
    engine = create_engine("duckdb:///:memory:")
    engine.execute(
        "register",
        (
            "my_table",
            DataFrame.from_dict(
                {
                    "name": ["Thelma", "Bonnie"],
                    "friend": ["Louise", "Clyde"],
                    "empty": [None, None],
                }
            ),
        ),
    )
    return engine


def test_table_exists(engine):
    exists_true = table_exists("my_table", engine=engine)
    exists_false = table_exists("nonexistent_table", engine=engine)
    assert exists_true
    assert exists_false is False


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"AB__URI": "sqlite:///:memory:"}):
        yield


def test_ab_uri():
    exists_false = table_exists("some_table")
    assert exists_false is False


def test_query_db(engine):
    res = query_db(
        "SELECT name, friend FROM my_table WHERE friend = 'Clyde'", engine=engine
    )
    assert len(res) == 1
    assert res[0].name == "Bonnie"
    assert res[0].friend == "Clyde"


def test_db_functions_in_runner(engine):
    runner = Runner(engine=engine)
    got = runner.render(
        "{{query_db('SELECT COUNT(*) n FROM my_table') | first | attr('n')}}"
    )
    want = "2"
    assert got == want


def test_get_max_value(engine):
    got = get_max_value("my_table.name", engine=engine)
    want = "Thelma"
    assert got == want


def test_get_max_value_null(engine):
    got = get_max_value("my_table.empty", engine=engine)
    want = None
    assert got == want
