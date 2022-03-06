from absql.files import parse
from jinja2 import Environment, BaseLoader, DebugUndefined


def render_text(text, **vars):
    """
    Given some text, render the template with the vars.
    If a templated variable is unknown, leave it alone.
    """
    template = Environment(loader=BaseLoader, undefined=DebugUndefined).from_string(
        text
    )
    return template.render(**vars)


def render_file(file_path):
    """
    Given a file path, render sql.
    """

    file_contents = parse(file_path)
    sql = file_contents["sql"]
    file_contents.pop("sql")
    return render_text(sql, **file_contents)
