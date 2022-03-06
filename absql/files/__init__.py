import os
import inspect
from absql.files.loader import generate_loader
from absql.files.parsers import parse_generic, parse_sql

default_parsers = {
    ".yml": parse_generic,
    ".yaml": parse_generic,
    ".sql": parse_sql,
}


def parse(file_path, parse_dict=default_parsers, loader=None):
    """
    Load a file.
    """

    if loader is None:
        loader = generate_loader()

    path, extension = os.path.splitext(file_path)

    parser = parse_dict[extension]

    if "loader" in inspect.signature(parser).parameters.keys():
        file_parsed = parser(file_path, loader=loader)
    else:
        file_parsed = parser(file_path)

    return file_parsed
