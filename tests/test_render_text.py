from absql import render_text


def test_render_text():
    template = "SELECT * FROM {{my_table_placeholder}}"
    result = render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table"


def test_leave_unknown_vars_alone():
    template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{ds}}'"
    result = render_text(template, my_table_placeholder="my_table")
    assert result == "SELECT * FROM my_table WHERE date = '{{ ds }}'"


# def test_leave_unknown_macros_alone():
#     template = "SELECT * FROM {{my_table_placeholder}} WHERE date = '{{get_ds()}}'"
#     table_name = "my_table"
#     result = render_text(template, my_table_placeholder="my_table")
#     assert result == "SELECT * FROM my_table WHERE date = '{{ get_ds() }}'"
