import pytest
from absql import Runner as r


@pytest.fixture
def simple_yml_path():
    return "tests/files/simple.yml"


def test_render_file_return_dict(simple_yml_path):
    file_as_dict = r.render_file(simple_yml_path, return_dict=True)
    print(file_as_dict)
    assert file_as_dict["my_table_placeholder"] == "my_table"
    assert file_as_dict["sql"] == "SELECT * FROM my_table"


def test_runner_return_dict(simple_yml_path):
    runner = r()
    file_as_dict = runner.render(simple_yml_path, return_dict=True)
    assert file_as_dict["my_table_placeholder"] == "my_table"
    assert file_as_dict["sql"] == "SELECT * FROM my_table"
