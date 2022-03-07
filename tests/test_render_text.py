from absql import Runner as r


def test_render_text():
    template = "SELECT * FROM {{my_table_placeholder}}"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table"


def test_leave_unknown_vars_alone():
    template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{ds}}'"
    result = r.render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table WHERE date = '{{ ds }}'"


# https://stackoverflow.com/questions/71374498/ignore-unknown-functions-in-jinja2

# def test_leave_unknown_macros_alone():
#     template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{get_ds()}}'"
#     table_name = "my_table"
#     result = r.render_text(template, my_table_placeholder="my_table")
#     assert result == "SELECT * FROM my_table WHERE date = '{{ get_ds() }}'"
