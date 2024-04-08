import re
import yaml
import jupytext
from absql.files.loader import generate_loader

FM_BOUNDARY = re.compile(r"^-{3,}\s*$", re.MULTILINE)


def frontmatter_load(file_path, loader=None):
    """
    Loads YAML frontmatter. Expects a YAML block at the top of the file
    that starts and ends with "---" (for non-YAML files). In use in favor of
    frontmatter.load so that custom dag_constructors (via PyYaml) can be used uniformly
    across all file types.
    """
    if loader is None:
        loader = generate_loader()
    with open(file_path, "r") as file:
        text = "".join(file.readlines())
        # Valid YAML files can begin with a document header (i.e. '---') and doesn't
        # require a terminating marker; therefore, the "frontmatter" doesn't necessarily
        # need to begin and end with this string.
        if text.startswith("---") and not file_path.endswith((".yml", ".yaml")):
            _, metadata, content = FM_BOUNDARY.split(text, 2)
            metadata = yaml.load(metadata, Loader=loader)
            content = content.strip("\n")
        elif text.startswith("{"):
            tmp_header = "/*ABSQLQSBA*/ "
            text = tmp_header + text
            metadata = {}
            content = yaml.load(text, Loader=loader)
            content = content.replace(tmp_header, "")
        elif text.startswith("/*") and file_path.endswith((".sql", "js")):
            # Retrieve the first matched set of text within a block comment
            # (i.e. /* ... */).
            metadata = (
                re.compile(r"^\/\*([\S\s]*?)\*\/$", re.MULTILINE).match(text).group(1)
            )
            # Text after the first block-comment end is considered the content of the
            # SQL file. This will handle block comments within the contents as well.
            _, _, content = text.partition("*/")

            metadata = yaml.load(metadata, Loader=loader)
            content = content.strip("\n")
        else:
            metadata = {}
            content = yaml.load(text, Loader=loader)
    return {"metadata": metadata, "content": content}


def parse_yml(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = frontmatter_load(file_path, loader=loader)
    file_content = raw_content["metadata"] or raw_content["content"]
    file_content["absql_body"] = file_content.get("sql", "")
    return file_content


def parse_sql(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = frontmatter_load(file_path, loader=loader)
    file_content = raw_content["metadata"]
    file_content["absql_body"] = raw_content["content"]
    return file_content


def parse_js(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = frontmatter_load(file_path, loader=loader)
    file_content = raw_content["metadata"]
    file_content["absql_body"] = raw_content["content"]
    return file_content


def parse_py(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = jupytext.read(file_path)["cells"]
    file_content = yaml.load(raw_content[0]["source"].replace("---", ""), Loader=loader)
    file_content["absql_body"] = raw_content[1]["source"]
    return file_content
