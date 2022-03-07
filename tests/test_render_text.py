from absql import Runner as r


def test_render_text():
    template = "SELECT * FROM {{my_table_placeholder}}"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table"


def test_leave_unknown_vars_alone():
    template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{my_date}}'"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table WHERE date = '{{ my_date }}'"


# https://stackoverflow.com/questions/71374498/ignore-unknown-functions-in-jinja2
# Below is a workaround for a function that you don't want to run immediately
def test_leave_unknown_functions_alone():
    template = (
        "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{'{{ get_date() }}'}}'"
    )
    # The true test
    # template = (
    #     "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{ get_ds() }}'"
    # )
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table WHERE date = '{{ get_date() }}'"
