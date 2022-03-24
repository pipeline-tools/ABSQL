from .env import env_var
from datetime import datetime, timedelta


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


default_macros = {"env_var": env_var, "datetime": datetime, "timedelta": timedelta}
default_constructors = {"!" + k: v for k, v in default_macros.items()}
