from inspect import cleandoc
from jinja2 import Environment, DebugUndefined
from absql.text import (
    clean_spacing,
    create_replacements,
    flatten_inputs,
    pretty_encode_sql,
)
from absql.files import parse
from absql.files.loader import generate_loader
from absql.functions import default_functions
from absql.utils import nested_apply, partialize_function


def render_text(
    text, replace_only=False, pretty_encode=False, partial_kwargs=None, **vars
):
    """
    Given some text, render the template with the vars.
    If a templated variable is unknown, leave it alone.
    """
    if replace_only:
        text = clean_spacing(text)
        flat_vars = flatten_inputs(**vars)
        replacements = create_replacements(**flat_vars)
        for k, v in replacements.items():
            text = text.replace(k, str(v))
        text = cleandoc(text)

    else:
        env = Environment(undefined=DebugUndefined)

        for k, v in vars.items():
            if v.__class__.__name__ == "function":
                vars[k] = partialize_function(v, partial_kwargs=partial_kwargs, **vars)
                env.filters[k] = vars[k]

        template = env.from_string(text)
        text = cleandoc(template.render(**vars))

    if pretty_encode:
        return pretty_encode_sql(text)
    else:
        return text


def render_context(extra_context=None, file_contents=None, partial_kwargs=None):
    """
    Render context dictionaries passed through a function call or
    file frontmatter (file_contents), with file_contents taking
    precedence over other all other provided context.
    """
    rendered_context = default_functions.copy()
    if extra_context:
        rendered_context.update(**extra_context)
    if file_contents:
        rendered_context.update(**file_contents)
    rendered_context = nested_apply(
        rendered_context,
        lambda x: render_text(x, partial_kwargs=partial_kwargs, **rendered_context),
    )
    return rendered_context


def render_file(
    file_path,
    loader=None,
    replace_only=False,
    extra_constructors=None,
    file_context_from=None,
    pretty_encode=False,
    partial_kwargs=None,
    **extra_context,
):
    """
    Given a file path, render SQL with a combination of
    the vars in the file and any extras passed to extra_context.
    """
    if loader is None:
        loader = generate_loader(extra_constructors or [])

    file_contents = parse(file_path, loader=loader)

    sql = file_contents["sql"]
    file_contents.pop("sql")

    if file_context_from:
        file_contents.update(file_contents.get(file_context_from, {}))
        file_contents.pop(file_context_from, {})

    rendered_context = render_context(extra_context, file_contents, partial_kwargs)

    rendered = render_text(
        text=sql,
        replace_only=replace_only,
        pretty_encode=pretty_encode,
        partial_kwargs=partial_kwargs,
        **rendered_context,
    )

    return rendered
