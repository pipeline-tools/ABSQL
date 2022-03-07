from absql.files import parse
from absql.files.loader import generate_loader
from jinja2 import Environment, BaseLoader, DebugUndefined


class Runner:
    def __init__(self, extra_context={}, extra_constructors=[], **kwargs):
        self.extra_context = extra_context
        self.loader = generate_loader(extra_constructors)

    @staticmethod
    def render_text(text, **vars):
        """
        Given some text, render the template with the vars.
        If a templated variable is unknown, leave it alone.
        """
        template = Environment(loader=BaseLoader, undefined=DebugUndefined).from_string(
            text
        )
        return template.render(**vars)

    @staticmethod
    def render_file(file_path, extra_context={}, extra_constructors=[], loader=None):
        """
        Given a file, render SQL with the a combination of
        the vars in the file and any extras passed to extra_context.
        """
        if loader is None:
            loader = generate_loader(extra_constructors)

        file_contents = parse(file_path, loader=loader)

        sql = file_contents["sql"]
        file_contents.pop("sql")
        file_contents.update(**extra_context)
        return Runner().render_text(sql, **file_contents)

    def render(self, file_path, extra_context={}):
        """
        Given a file, render SQL with the a combination of
        the vars in the file and any extras passed to extra_context.
        """
        return self.render_file(file_path, extra_context, loader=self.loader)
