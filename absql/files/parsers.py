import re
import yaml
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
        else:
            metadata = {}
            content = yaml.load(text, Loader=loader)
    return {"metadata": metadata, "content": content}


def parse_generic(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = frontmatter_load(file_path, loader=loader)
    file_content = raw_content["metadata"] or raw_content["content"]
    return file_content


def parse_sql(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    raw_content = frontmatter_load(file_path, loader=loader)
    file_content = raw_content["metadata"]
    file_content["sql"] = raw_content["content"]
    return file_content
