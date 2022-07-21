from inspect import cleandoc
from absql.files import parse, accepted_file_types
from absql.files.loader import generate_loader
from jinja2 import Template, DebugUndefined
from absql.functions import default_functions
from absql.text import (
    clean_spacing,
    create_replacements,
    flatten_inputs,
    pretty_encode_sql,
)
from absql.utils import nested_apply, get_function_arg_names, partialize_engine_func


class Runner:
    def __init__(
        self,
        extra_constructors=None,
        replace_only=False,
        file_context_from=None,
        **extra_context,
    ):
        self.extra_context = dict(extra_context)
        self.loader = generate_loader(extra_constructors or [])
        self.replace_only = replace_only
        self.file_context_from = file_context_from

    @staticmethod
    def render_text(text, replace_only=False, pretty_encode=False, **vars):
        """
        Given some text, render the template with the vars.
        If a templated variable is unknown, leave it alone.
        """

        # Allows an instantiated SQLAlchemy engine to be utilized
        # in any function with a engine argument, without the user needing
        # to specify the engine in the function call.
        engine = vars.get("engine", None)
        for k, v in vars.items():
            if v.__class__.__name__ == "function":
                if "engine" in get_function_arg_names(v):
                    vars[k] = partialize_engine_func(v, engine=engine)

        if replace_only:
            text = clean_spacing(text)
            flat_vars = flatten_inputs(**vars)
            replacements = create_replacements(**flat_vars)
            for k, v in replacements.items():
                text = text.replace(k, str(v))
            text = cleandoc(text)
        else:
            template = Template(text, undefined=DebugUndefined)
            text = cleandoc(template.render(**vars))
        if pretty_encode:
            return pretty_encode_sql(text)
        else:
            return text

    @staticmethod
    def render_context(extra_context=None, file_contents=None):
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
            lambda x: Runner.render_text(x, **rendered_context),
        )
        return rendered_context

    @staticmethod
    def render_file(
        file_path,
        loader=None,
        replace_only=False,
        extra_constructors=None,
        file_context_from=None,
        pretty_encode=False,
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

        rendered_context = Runner.render_context(extra_context, file_contents)

        rendered = Runner.render_text(
            text=sql,
            replace_only=replace_only,
            pretty_encode=pretty_encode,
            **rendered_context,
        )

        return rendered

    def render(self, text, pretty_encode=False, replace_only=None):
        """
        Given text or a file path, render SQL with the a combination of
        the vars in the file and any extras passed to extra_context during
        the instantiation of the runner.
        """
        if text.endswith(accepted_file_types):
            rendered = self.render_file(
                file_path=text,
                loader=self.loader,
                replace_only=replace_only or self.replace_only,
                file_context_from=self.file_context_from,
                pretty_encode=pretty_encode,
                **self.extra_context,
            )
        else:
            rendered = self.render_text(
                text=text,
                replace_only=replace_only or self.replace_only,
                pretty_encode=pretty_encode,
                **self.render_context(self.extra_context),
            )
        return rendered

    def set_context(self, **context):
        self.extra_context.update(context)
