import yaml
from absql.functions import default_constructors


def scalar_to_value(scalar, constructor_dict):
    """
    Converts a YAML ScalarNode to its underlying Python value
    """
    type = scalar.tag.split(":")[-1]
    val = scalar.value
    if isinstance(scalar, yaml.MappingNode):
        val = node_converter(scalar, constructor_dict)
        func = constructor_dict.get(type)
        return func(**val)
    if isinstance(scalar, yaml.SequenceNode):
        val = node_converter(scalar, constructor_dict)
        func = constructor_dict.get(type)
        return func(*val)
    if type.startswith("!"):
        func = constructor_dict.get(type)
        return func(val)
    # Handle null type - https://yaml.org/type/null.html
    if type == "null":
        return None
    return eval('{type}("""{val}""")'.format(type=type, val=val))


def node_converter(x, constructor_dict):
    """
    Converts YAML nodes of varying types into Python values,
    lists, and dictionaries
    """
    if isinstance(x, yaml.ScalarNode):
        # "I am an atomic value"
        return yaml.load(x.value, yaml.SafeLoader)
    if isinstance(x, yaml.SequenceNode):
        # "I am a list"
        return [scalar_to_value(v, constructor_dict) for v in x.value]
    if isinstance(x, yaml.MappingNode):
        # "I am a dict"
        return {
            scalar_to_value(v[0], constructor_dict): scalar_to_value(
                v[1], constructor_dict
            )
            for v in x.value
        }


def wrap_yaml(func, constructor_dict):
    """Turn a function into one that can be run on a YAML input"""

    def ret(loader, x):
        value = node_converter(x, constructor_dict)

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

    class Loader(yaml.SafeLoader):
        # ensures a new Loader is returned
        # every time the function is called
        pass

    extra_constructors = extra_constructors or []
    unchecked_constructors = default_constructors.copy()

    if isinstance(extra_constructors, list) and len(extra_constructors) > 0:
        extra_constructors = {
            ("!" + func.__name__): func for func in extra_constructors
        }

    if len(extra_constructors) > 0:
        unchecked_constructors.update(extra_constructors)

    # Ensure all tags start with "!"
    checked_constructors = {}
    for tag, func in unchecked_constructors.items():
        if not tag.startswith("!"):
            tag = "!" + tag
        checked_constructors[tag] = func

    for tag, func in checked_constructors.items():
        Loader.add_constructor(tag, wrap_yaml(func, checked_constructors))
    return Loader
