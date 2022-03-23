import re


def clean_spacing(text):
    text = re.sub("\\{\\{\\s+", "{{ ", text)
    text = re.sub("\\s+\\}\\}", " }}", text)
    return text
