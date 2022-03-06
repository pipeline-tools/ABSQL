import re
import yaml
from absql.files.loader import generate_loader


def frontmatter_load(file_path, loader=None):
    """
    Loads YAML frontmatter. Expects a YAML block at the top of the file
    that starts and ends with "---". In use in favor of frontmatter.load
    so that custom dag_constructors (via PyYaml) can be used uniformly across
    all file types.
    """
    if loader is None:
        loader = generate_loader()
    FM_BOUNDARY = re.compile(r"^-{3,}\s*$", re.MULTILINE)
    with open(file_path, "r") as file:
        text = "".join(file.readlines())
        if text.startswith("---"):
            _, metadata, content = FM_BOUNDARY.split(text, 2)
            metadata = yaml.load(metadata, Loader=loader)
            content = content.strip("\n")
        else:
            metadata = None
            content = yaml.load(text, Loader=loader)
    return {"metadata": metadata, "content": content}


def parse_generic(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    # Read either the frontmatter or the parsed yaml file (using "or" to coalesce them)
    file_contents = frontmatter_load(file_path)
    job_spec = file_contents["metadata"] or file_contents["content"]
    return job_spec


def parse_sql(file_path, loader=None):
    if loader is None:
        loader = generate_loader()
    file_contents = frontmatter_load(file_path, loader=loader)
    job_spec = file_contents["metadata"]
    job_spec["sql"] = file_contents["content"]
    return job_spec
