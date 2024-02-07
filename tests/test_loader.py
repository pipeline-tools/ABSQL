import pytest
from pathlib import Path

from absql import Runner


@pytest.mark.parametrize(
    argnames="sql_file",
    argvalues=[str(f) for f in Path("tests/files/").rglob("loader_test*.sql")],
)
def test_loader_always_new(sql_file):
    runner_a = Runner(extra_constructors={"f": lambda: "a"})
    runner_a_want = "SELECT * FROM a"
    render_a_got_1 = runner_a.render(sql_file)
    assert render_a_got_1 == runner_a_want

    runner_b = Runner(extra_constructors={"f": lambda: "b"})
    runner_b_want = "SELECT * FROM b"
    runner_b_got = runner_b.render(sql_file)
    assert runner_b_got == runner_b_want

    render_a_got_2 = runner_a.render(sql_file)
    assert render_a_got_2 == runner_a_want
