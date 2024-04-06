import os
from absql.utils import get_function_arg_names
from absql.files.loader import generate_loader
from absql.files.parsers import parse_yml, parse_sql, parse_js, parse_py

default_parsers = {
    ".yml": parse_yml,
    ".yaml": parse_yml,
    ".js": parse_js,
    ".py": parse_py,
    ".sql": parse_sql,
}

accepted_file_types = tuple(default_parsers.keys())


def parse(file_path, parse_dict=default_parsers, loader=None):
    """
    Load a file.
    """

    if loader is None:
        loader = generate_loader()

    path, extension = os.path.splitext(file_path)

    parser = parse_dict[extension]

    if "loader" in get_function_arg_names(parser):
        file_parsed = parser(file_path, loader=loader)
    else:
        file_parsed = parser(file_path)

    return file_parsed
