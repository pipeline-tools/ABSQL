from absql import Runner as r


def test_render_text():
    template = "SELECT * FROM {{my_table_placeholder}}"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table"


def test_leave_unknown_vars_alone():
    template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{my_date}}'"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table WHERE date = '{{ my_date }}'"


# Would be nice to just use jinja for this
# https://stackoverflow.com/questions/71374498/ignore-unknown-functions-in-jinja2
def test_leave_unknown_functions_alone():
    template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{ get_date() }}'"
    result = r.render_text(template, my_table_placeholder="my_table", replace_only=True)
    assert result == "SELECT * FROM my_table WHERE date = '{{ get_date() }}'"


def test_nested_replace():
    context = {"params": {"foo": "bar", "biz": "baz"}}
    template = "{{ params.foo }} and {{  params.biz  }}"
    got = r.render_text(template, replace_only=True, **context)
    want = "bar and baz"
    assert got == want


def test_pretty_encode():
    got = r.render_text(
        """SELECT * FROM "my_schema"."my_table" WHERE my_col = 'my_value'""",
        pretty_encode=True,
    )
    want = """\x1b[1m\x1b[96mSELECT\x1b[0m * \x1b[1m\x1b[96mFROM\x1b[0m \x1b[95m"my_schema"\x1b[39m.\x1b[95m"my_table"\x1b[39m \x1b[1m\x1b[96mWHERE\x1b[0m my_col = \x1b[95m\'my_value\'\x1b[39m"""  # noqa
    assert got == want


def test_filters():
    def alter_text(x, upper=True):
        if upper:
            return x.upper()
        return x.lower()

    you = "yOu"

    upper_want = "hey YOU"
    upper_got = r.render_text(
        "hey {{person | case_it}}", person=you, case_it=alter_text
    )
    assert upper_got == upper_want

    lower_want = "hey you"
    lower_got = r.render_text(
        "hey {{person | case_it(upper=False)}}", person=you, case_it=alter_text
    )
    assert lower_want == lower_got

    partial_want = "hey you"
    partial_got = r.render_text(
        "hey {{person | case_it}}",
        person=you,
        case_it=alter_text,
        upper=False,
        partial_kwargs=["upper"],
    )
    assert partial_want == partial_got

    pipeline_want = "hey YOU"
    pipeline_got = r.render_text(
        "hey {{person | case_it(upper=False) | case_it}}",
        person=you,
        case_it=alter_text,
    )
    assert pipeline_want == pipeline_got
