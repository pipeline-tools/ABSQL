import yaml
from absql.functions import default_constructors


def scalar_to_value(scalar):
    """
    Converts a YAML ScalarNode to its underlying Python value
    """
    type = scalar.tag.split(":")[-1]
    val = scalar.value
    return eval('{type}("""{val}""")'.format(type=type, val=val))


def node_converter(x):
    """
    Converts YAML nodes of varying types into Python values,
    lists, and dictionaries
    """
    if isinstance(x, yaml.ScalarNode):
        # "I am an atomic value"
        return yaml.load(x.value, yaml.SafeLoader)
    if isinstance(x, yaml.SequenceNode):
        # "I am a list"
        return [scalar_to_value(v) for v in x.value]
    if isinstance(x, yaml.MappingNode):
        # "I am a dict"
        return {scalar_to_value(v[0]): scalar_to_value(v[1]) for v in x.value}


def wrap_yaml(func):
    """Turn a function into one that can be run on a YAML input"""

    def ret(loader, x):
        value = node_converter(x)

        if value is not None:

            if isinstance(value, list):
                return func(*value)

            if isinstance(value, dict):
                return func(**value)

            return func(value)

        else:
            return func()

    return ret


def generate_loader(extra_constructors=None):
    """Generates a SafeLoader with both default and custom constructors"""
    loader = yaml.SafeLoader
    extra_constructors = extra_constructors or []
    default_constructor_dict = default_constructors.copy()

    if isinstance(extra_constructors, list) and len(extra_constructors) > 0:
        extra_constructors = {
            ("!" + func.__name__): func for func in extra_constructors
        }

    if len(extra_constructors) > 0:
        default_constructor_dict.update(extra_constructors)
    for tag, func in default_constructor_dict.items():
        loader.add_constructor(tag, wrap_yaml(func))
    return loader
