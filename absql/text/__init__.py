import re
from flatdict import FlatDict
from sql_metadata import Parser
from colorama import Fore


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


def pretty_encode_sql(query, keyword_color=Fore.LIGHTCYAN_EX):
    p = Parser(query)

    keywords = list(set([t.value for t in p.tokens if t.is_keyword]))

    bold_start = "\033[1m"
    bold_end = "\033[0m"

    replacements = {k: bold_start + keyword_color + k + bold_end for k in keywords}

    for keyword, formatted_keyword in replacements.items():
        query = re.sub(r"\b{k}\b".format(k=keyword), formatted_keyword, query)

    return query
