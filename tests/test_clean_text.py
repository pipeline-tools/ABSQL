from absql.text import clean_spacing


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
