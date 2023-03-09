from absql.files import accepted_file_types
from absql.files.loader import generate_loader
from absql.render import render_text, render_context, render_file


class Runner:
    def __init__(
        self,
        extra_constructors=None,
        replace_only=False,
        file_context_from=None,
        partial_kwargs=None,
        **extra_context,
    ):
        self.extra_context = dict(extra_context)
        self.loader = generate_loader(extra_constructors or [])
        self.replace_only = replace_only
        self.file_context_from = file_context_from
        self.partial_kwargs = partial_kwargs or ["engine"]

    @staticmethod
    def render_text(
        text, replace_only=False, pretty_encode=False, partial_kwargs=None, **vars
    ):
        return render_text(
            text=text,
            replace_only=replace_only,
            pretty_encode=pretty_encode,
            partial_kwargs=partial_kwargs,
            **vars,
        )

    @staticmethod
    def render_context(extra_context=None, file_contents=None, partial_kwargs=None):
        return render_context(
            extra_context=extra_context,
            file_contents=file_contents,
            partial_kwargs=partial_kwargs,
        )

    @staticmethod
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
        return render_file(
            file_path=file_path,
            loader=loader,
            replace_only=replace_only,
            extra_constructors=extra_constructors,
            file_context_from=file_context_from,
            pretty_encode=pretty_encode,
            partial_kwargs=partial_kwargs,
            **extra_context,
        )

    def render(self, text, pretty_encode=False, replace_only=None, **extra_context):
        """
        Given text or a file path, render SQL with the a combination of
        the vars in the file and any extras passed to extra_context during
        the instantiation of the runner.
        """

        current_context = self.extra_context.copy()
        current_context.update(extra_context)

        if text.endswith(accepted_file_types):
            rendered = render_file(
                file_path=text,
                loader=self.loader,
                replace_only=replace_only or self.replace_only,
                file_context_from=self.file_context_from,
                pretty_encode=pretty_encode,
                partial_kwargs=self.partial_kwargs,
                **current_context,
            )
        else:
            rendered = render_text(
                text=text,
                replace_only=replace_only or self.replace_only,
                pretty_encode=pretty_encode,
                partial_kwargs=self.partial_kwargs,
                **render_context(current_context, partial_kwargs=self.partial_kwargs),
            )
        return rendered

    def set_context(self, **context):
        self.extra_context = self.extra_context.copy()
        self.extra_context.update(context)
