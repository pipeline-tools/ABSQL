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


def partialize_engine_func(func, engine):
    if "engine" in get_function_arg_names(func):
        return partial(func, engine=engine)
    else:
        return func
