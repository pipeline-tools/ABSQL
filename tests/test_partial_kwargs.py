import pytest
from absql import Runner


@pytest.fixture()
def planet():
    def planet(planet_name):
        return planet_name

    return planet


def test_render_text_extra_partial(planet):

    got = Runner.render_text(
        "Hello {{planet()}}",
        planet=planet,
        planet_name="Earth",
        partial_kwargs=["planet_name"],
    )
    want = "Hello Earth"
    assert got == want


def test_default_render_text_extra_partial_fails(planet):
    with pytest.raises(TypeError):
        Runner.render_text("Hello {{planet()}}", planet=planet, planet_name="Earth")


def test_render_file_extra_partial(planet):
    got = Runner.render_file(
        "tests/files/partial_planet.sql",
        planet=planet,
        planet_name="Earth",
        partial_kwargs=["planet_name"],
    )
    want = "Hello Earth, Goodbye Earth"
    assert got == want
