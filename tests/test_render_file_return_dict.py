import pytest
from absql import Runner as r


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


@pytest.fixture
def simple_js_path():
    return "tests/files/simple.js"


@pytest.fixture
def simple_py_path():
    return "tests/files/simple.py"


def test_render_file_return_dict(simple_yml_path):
    file_as_dict = r.render_file(simple_yml_path, return_dict=True)
    print(file_as_dict)
    assert file_as_dict["my_table_placeholder"] == "my_table"
    assert file_as_dict["sql"] == "SELECT * FROM my_table"
    assert file_as_dict["absql_body"] == "SELECT * FROM my_table"


def test_runner_return_dict(simple_yml_path):
    runner = r()
    file_as_dict = runner.render(simple_yml_path, return_dict=True)
    assert file_as_dict["my_table_placeholder"] == "my_table"
    assert file_as_dict["sql"] == "SELECT * FROM my_table"
    assert file_as_dict["absql_body"] == "SELECT * FROM my_table"


def test_render_file_return_dict_js(simple_js_path):
    file_as_dict = r.render_file(simple_js_path, return_dict=True)
    assert file_as_dict["foo"] == "bar"
    assert file_as_dict["absql_body"] == "console.log('hello')"


def test_render_file_return_dict_py(simple_py_path):
    file_as_dict = r.render_file(simple_py_path, return_dict=True)
    print(file_as_dict)
    assert file_as_dict["foo"] == "bar"
    assert file_as_dict["absql_body"] == 'print("hello")'
