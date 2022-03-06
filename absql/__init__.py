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
