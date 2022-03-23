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
