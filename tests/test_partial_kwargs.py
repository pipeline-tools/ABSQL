import pytest
from absql import Runner


def test_render_text_extra_partial():
    def planet(planet_name):
        return planet_name

    got = Runner.render_text(
        "Hello {{planet()}}",
        planet=planet,
        planet_name="Earth",
        partial_kwargs=["planet_name"],
    )
    want = "Hello Earth"
    assert got == want


def test_default_render_text_extra_partial_fails():
    def planet(planet_name):
        return planet_name

    with pytest.raises(TypeError):
        Runner.render_text("Hello {{planet()}}", planet=planet, planet_name="Earth")
