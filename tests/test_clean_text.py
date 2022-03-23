from absql.text import clean_spacing, create_replacements


def test_clean_spaces():
    text = "{{   hello  }}   world"
    got = clean_spacing(text)
    want = "{{ hello }}   world"
    assert got == want


def test_clean_tabs():
    text = "{{  hello   }}   world"
    got = clean_spacing(text)
    want = "{{ hello }}   world"
    assert got == want


def test_replacements():
    got = create_replacements(foo="bar")
    want = {"{{foo}}": "bar", "{{ foo }}": "bar"}
    assert got == want
