from absql.files.parsers import FM_BOUNDARY
from inspect import signature
from functools import partial


def nested_apply(x, f):
    if x.__class__.__name__ in ["dict", "list", "str"]:
        if isinstance(x, str):
            x = f(x)
        elif isinstance(x, list):
            x = [nested_apply(i, f) for i in x]
        elif isinstance(x, dict):
            for k in x:
                x[k] = nested_apply(x[k], f)
    else:
        return x
    return x


def get_function_arg_names(func):
    return list(signature(func).parameters.keys())


def partialize_function(func, partial_kwargs=None, **kwargs):
    partial_kwargs = partial_kwargs or ["engine"]
    function_args = get_function_arg_names(func)

    kwargs_to_partialize = {
        k: v for k, v in kwargs.items() if k in function_args and k in partial_kwargs
    }

    if kwargs_to_partialize:
        return partial(func, **kwargs_to_partialize)
    else:
        return func


def load_body(file_path):
    with open(file_path, "r") as file:
        text = "".join(file.readlines())
        if text.startswith("---"):
            _, metadata, content = FM_BOUNDARY.split(text, 2)
            return content
        else:
            return text
