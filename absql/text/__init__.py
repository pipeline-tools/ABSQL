import re
from flatdict import FlatDict


def clean_spacing(text):
    text = re.sub("\\{\\{\\s+", "{{ ", text)
    text = re.sub("\\s+\\}\\}", " }}", text)
    return text


def create_replacements(**kwargs):
    replacements = {}
    for k, v in kwargs.items():
        replacement = {"{{{{{k}}}}}".format(k=k): v, "{{{{ {k} }}}}".format(k=k): v}
        replacements.update(replacement)
    return replacements


def flatten_inputs(**kwargs):
    flattened = FlatDict(kwargs, delimiter=".")
    return flattened
