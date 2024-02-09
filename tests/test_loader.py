from absql import Runner


def test_loader_always_new():
    runner_a = Runner(extra_constructors={"f": lambda: "a"})
    runner_a_want = "SELECT * FROM a"
    render_a_got_1 = runner_a.render("tests/files/loader_test.sql")
    assert render_a_got_1 == runner_a_want

    runner_b = Runner(extra_constructors={"f": lambda: "b"})
    runner_b_want = "SELECT * FROM b"
    runner_b_got = runner_b.render("tests/files/loader_test.sql")
    assert runner_b_got == runner_b_want

    render_a_got_2 = runner_a.render("tests/files/loader_test.sql")
    assert render_a_got_2 == runner_a_want
