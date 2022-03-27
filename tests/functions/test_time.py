import pytest
from absql import Runner
from pendulum import now
from datetime import timedelta


@pytest.fixture
def runner():
    return Runner()


@pytest.fixture
def yesterdate():
    return (now(tz="utc") - timedelta(days=1)).to_date_string()


@pytest.fixture
def yesterhour():
    return (
        (now(tz="utc") - timedelta(hours=1, days=0))
        .replace(minute=0, second=0)
        .to_datetime_string()
    )


def test_previous_date(runner, yesterdate):
    assert runner.render("{{previous_date()}}") == yesterdate


def test_previous_hour(runner, yesterhour):
    assert runner.render("{{previous_hour()}}") == yesterhour
